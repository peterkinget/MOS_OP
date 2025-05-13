#!/usr/bin/env python3
# coding: utf-8
#
# MOS_OP.py for MOS Operating Point
# 
# Peter Kinget
#
# Dec. 2023  v0.1d
# Feb. 2024  v0.2 --> published on GitHub
# May  2024  v0.3 --> added model_type support, multiple output formats, and current thresholding
# 
# Reading PSF files from cadence dc operating point simulation
# 
# Using psf-utils from K. Kundert at https://github.com/KenKundert/psf_utils/tree/master
# or https://pypl.org/psf-utils/
# 
# Install psf-utils with pip3
#
# Requires the latest psf_utils version 1.7 or higher that can read info files
#
# NO Warranty, use at your own risk!!
#
################################################################################
import sys
import os
import numpy as np
import pandas as pd
import json
import argparse
pd.set_eng_float_format(accuracy=1, use_eng_prefix=True)
#
from psf_utils import PSF
from inform import Error, display
################################################################################
# Define mapping from internal BSIM3 names to external model-specific names
SIGNAL_NAME_MAPPINGS = {
    "bsim3": {
        "vgsteff": "vgsteff",
        "cgsovl": "cgsovl", 
        "cgdovl": "cgdovl", 
        "cgbovl": "cgbovl"
    },
    "bsim4": {
        "vgsteff": "vgt",
        "cgsovl": "covlgs", 
        "cgdovl": "covlgd", 
        "cgbovl": "covlgb"
    }
}

def parse_args():
    parser = argparse.ArgumentParser(description='Process MOS operating point simulation data')
    parser.add_argument('dcop_file', help='dcOpInfo.info ascii file to process')
    parser.add_argument('element_file', help='element.info ascii file to process')
    parser.add_argument('device_file', help='JSON file with device names')
    parser.add_argument('--model', default='bsim3', choices=['bsim3', 'bsim4'], 
                        help='MOS model type (default: bsim3)')
    parser.add_argument('--abs_ids_min', type=float, default=0,
                        help='Minimum absolute drain current threshold (in A) for including transistors (default: 0)')
    return parser.parse_args()

def psf_list_signals(psf, beginning=""):
    for signal in psf.all_signals():
        if (signal.name[0:len(beginning)]==beginning):
            print(signal.name, signal.units)

def collect_transistors_data(psf, transistors, signal_names, model_type="bsim3", tor_signal_separator='.'):
    transistors_data = {}
    for transistor in transistors:
        transistors_data[transistor] = {}
        for internal_name in signal_names:
            # Map internal name to model-specific external name
            external_name = internal_name
            
            # For the special mapped signals, use the model-specific naming
            if internal_name in SIGNAL_NAME_MAPPINGS.get("bsim3", {}):
                external_name = SIGNAL_NAME_MAPPINGS[model_type].get(internal_name, internal_name)
            
            tor_signal_name = transistor + tor_signal_separator + external_name
            try:
                transistors_data[transistor][internal_name] = float(psf.get_signal(tor_signal_name).ordinate)
            except Exception as e:
                print(f"Warning: Could not read signal {tor_signal_name}: {e}")
                transistors_data[transistor][internal_name] = float('nan')
    
    return transistors_data

# convert signs of transcapacitance to Tsividis convention
# Cxx = dQx/dVx and Cxy = -dQx/dVy with x <> y
def cap_sign(cap):
    if cap[1] == cap[2]:
        cap_sign = 1
    else:
        cap_sign = -1
    return cap_sign

################################################################################
# Main script
################################################################################
def main():
    # Parse command-line arguments
    args = parse_args()
    
    # Print model type information
    print(f"Using model type: {args.model}")
    if args.abs_ids_min > 0:
        print(f"Using minimum absolute current cutoff: {args.abs_ids_min} A")
    
    # read the psf dcop file
    print(f"Reading {args.dcop_file}")
    psf = PSF(args.dcop_file)
    print(f"Reading {args.element_file}")
    psf_element = PSF(args.element_file)
    
    # read the transistor name file
    with open(args.device_file) as f:
        json_data = f.read()
        
    # create transistor name dictionaries to go from netlist names to shortcuts and back
    transistor_names_shortcut_to_netlist = json.loads(json_data)
    transistor_names_shortcuts = transistor_names_shortcut_to_netlist.keys()
    transistor_names_netlist = transistor_names_shortcut_to_netlist.values()
    transistor_names_netlist_to_shortcut = dict(zip(transistor_names_netlist,transistor_names_shortcuts))
    
    # parameters to read from the dcop file (using internal BSIM3 names)
    signal_names_op = [ 'ids', 'vgs', 'vds', 'vdsat', 'region',
                        'vbs', 'vth', 'vgsteff', 
                        'gm', 'gds', 'gmb', 'gmoverid', 'self_gain', 
                        'cgg', 'cgs', 'cgd', 'cgb',
                        'csg', 'css', 'csd', 'csb', 
                        'cdg', 'cds', 'cdd', 'cdb', 
                        'cbg', 'cbs', 'cbd', 'cbb',
                        'cjd', 'cjs', 'cgsovl', 'cgdovl', 'cgbovl',
                        'fug']
    
    # get the data from the psf file and put in a dataframe
    # columns are the parameters
    # rows are the transistors
    print("Processing transistor data")
    transistors_data = collect_transistors_data(psf, transistor_names_netlist_to_shortcut.keys(), 
                                               signal_names_op, model_type=args.model)
    df = pd.DataFrame(transistors_data).T
    
    # get the data from the psf file and put in a dataframe
    # columns are the sizing data
    # rows are the transistors
    sizing_names = [ 'w', 'l', 'm', 'as', 'ad', 'ps', 'pd']
    transistors_sizing = collect_transistors_data(psf_element, transistor_names_netlist_to_shortcut.keys(), sizing_names)
    df_element = pd.DataFrame(transistors_sizing).T
    
    # merge the dataframes
    df_merged = pd.concat([df_element.T, df.T]).T
    df = df_merged
    
    # replace transistor netlist names with shortcuts
    new_names = [ transistor_names_netlist_to_shortcut[label] for label in df.index]
    df.index = new_names
    
    # convert region to words
    df['region'] = df['region'].map({0.0:'off', 1.0:'linear', 2.0:'saturation'})
    
    # convert signs of transcapacitance to Tsividis convention
    # Cxx = dQx/dVx and Cxy = -dQx/dVy with x <> y
    trans_capacitor_names = [ 'cgs', 'cgd', 'cgb', 'csg', 'csd', 'csb', 'cdg', 'cds', 'cdb',
                              'cbg', 'cbs', 'cbd' ]
    for capacitor in trans_capacitor_names:
        df[capacitor] = (-1)*df[capacitor]
    
    # calculate the transcapacitances for the small-signal model (Tsividis Fig. 8.5)
    df['cm'] = df['cdg']-df['cgd']
    df['cmb'] = df['cdb']-df['cbd']
    df['cmx'] = df['cbg']-df['cgb']
    
    # make a list for the desired printing order of the parameters
    element_info_print = ['w', 'l', 'm', 'as', 'ad', 'ps', 'pd']
    signal_names_op_print = [ 'ids', 'vgs', 'vds', 'vdsat', 'region',
                              'vbs', 'vth', 'vgsteff', 
                              'gm', 'gds', 'gmb', 'gmoverid', 'self_gain', 
                              'cgs', 'cgsovl', 'cgb', 'cgbovl', 'cgd', 'cgdovl',
                              'cbd', 'cjd', 'cbs', 'cjs',
                              'csd', 'cm', 'cmb', 'cmx','fug']
    
    # Create dataframe for printing
    df_to_print = df[[*element_info_print, *signal_names_op_print]]
    
    # Filter devices based on current threshold
    if args.abs_ids_min > 0:
        current_mask = abs(df['ids']) > args.abs_ids_min
        filtered_devices = df.index[~current_mask].tolist()
        
        if filtered_devices:
            print(f"\nThe following devices were excluded (|Ids| < {args.abs_ids_min} A):")
            for device in filtered_devices:
                print(f"  - {device}: Ids = {df.loc[device, 'ids']:.3e} A")
            print()
        
        df_to_print = df_to_print[current_mask]
    
    # print to the console
    print(df_to_print.T)
    
    # write to csv file
    csv_filename = "operating_point.csv"
    print(f"Writing {csv_filename}")
    df_to_print.T.to_csv(csv_filename)
    
    # write to text file
    text_filename = "operating_point.txt"
    print(f"Writing {text_filename}")
    with open(text_filename, 'w') as f:
        f.write(df_to_print.T.to_string())
    
    # write to markdown file
    md_filename = "operating_point.md"
    print(f"Writing {md_filename}")
    
    from pandas.io.formats.format import EngFormatter
    fmt = EngFormatter(accuracy=1, use_eng_prefix=True)
    # apply only to numeric cells
    df_to_print_str = df_to_print.T.map(
        lambda x: fmt(x) if isinstance(x, (int, float)) else x
    )
    df_to_print_str.to_markdown(md_filename)

if __name__ == "__main__":
    main()

