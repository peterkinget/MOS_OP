#!/usr/bin/env python3
# coding: utf-8
#
# MOS_OP2.py for MOS Operating Point
# 
# Peter Kinget
#
# Dec. 2023  v0.1d
# Feb. 2024  v0.2 --> published on GitHub
# Feb. 2024  v0.3 --> switching to slimmer interface
# May  2024  v0.4 --> adding model_type support for BSIM3/BSIM4 compatibility
# May  2024  v0.5 --> refactored for pip installation
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
pd.set_eng_float_format(accuracy=1, use_eng_prefix=True)
import json
import argparse
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

def do_conversion_to_ascii(file):
    if os.path.isfile(file+'.ascii'):
        print(f"Using available ascii {file}.ascii")
    else:
        if os.path.isfile(file):
            print(f"Converting {file} to ascii")
            os.system(f"psf {file} {file}.ascii")
        else:
            raise SystemExit(f"{file} does not exist")

def psf_list_signals(psf, beginning=""):
    for signal in psf.all_signals():
        # print(signal.name[0:len(beginning)])
        if (signal.name[0:len(beginning)]==beginning):
            print(signal.name, signal.units)

def collect_transistors_data(psf, transistors, signal_names, model_type="bsim3", tor_signal_separator = '.'): 
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

def parse_args():
    parser = argparse.ArgumentParser(description='Process MOS operating point simulation data using a config file')
    parser.add_argument('config_file', help='JSON config file with transistor names and simulation directory')
    return parser.parse_args()

def main():
    ################################################################################
    # get the commandline parameters
    args = parse_args()
    devicefile = args.config_file

    # read the config file
    with open(devicefile) as f:
        json_data = f.read()

    config_data = json.loads(json_data)

    # Get model type with fallback to "bsim3" as default
    model_type = config_data.get('model_type', 'bsim3')
    print(f"Using model type: {model_type}")

    # Get abs_ids_min cutoff with fallback to previous hardcoded value as default
    abs_ids_min = config_data.get('abs_ids_min', 0)
    print(f"Using minimum absolute current cutoff: {abs_ids_min} A")

    filepath = os.path.join(config_data['simulation_dir'], config_data['design_name'])

    dcopfile = os.path.join(filepath, "dcOpInfo.info")
    do_conversion_to_ascii(dcopfile)
    dcopfile = dcopfile + '.ascii'

    elementinfofile = os.path.join(filepath,"element.info")
    do_conversion_to_ascii(elementinfofile)
    elementinfofile = elementinfofile + '.ascii'

    # read the psf dcop file
    print(f"Reading {dcopfile}")
    psf = PSF(dcopfile)
    print(f"Reading {elementinfofile}")
    psf_element = PSF(elementinfofile)

    # for debugging
    # psf_list_signals(psf)

    # create transistor name dictionaries to go from netlist names to shortcuts and back
    transistor_names_shortcut_to_netlist = config_data['transistor_names']
    transistor_names_shortcuts = transistor_names_shortcut_to_netlist.keys()
    transistor_names_netlist = transistor_names_shortcut_to_netlist.values()
    transistor_names_netlist_to_shortcut = dict(zip(transistor_names_netlist,transistor_names_shortcuts))

    # parameters to read from the dcop file (using internal BSIM3 names)
    signal_names_op = [ 'ids', 'vgs', 'vds', 'vdsat', 'region',
                        'vbs', 'vth', 'vgsteff',  # Using BSIM3 name (was vgt)
                        'gm', 'gds', 'gmb', 'gmoverid', 'self_gain', 
                        'cgg', 'cgs', 'cgd', 'cgb',
                        'csg', 'css', 'csd', 'csb', 
                        'cdg', 'cds', 'cdd', 'cdb', 
                        'cbg', 'cbs', 'cbd', 'cbb',
                        'cjd', 'cjs', 
                        'cgsovl', 'cgdovl', 'cgbovl',  # Using BSIM3 names
                        'fug']

    # get the data from the psf file and put in a dataframe
    # columns are the parameters
    # rows are the transistors
    print("Processing transistor data")
    transistors_data = collect_transistors_data(psf, transistor_names_netlist_to_shortcut.keys(), signal_names_op, model_type=model_type)
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
                            'vbs', 'vth', 'vgsteff',  # Using BSIM3 name
                            'gm', 'gds', 'gmb', 'gmoverid', 'self_gain', 
                            'cgs', 'cgsovl', 'cgb', 'cgbovl', 'cgd', 'cgdovl',  # Using BSIM3 names
                            'cbd', 'cjd', 'cbs', 'cjs',
                            'csd', 'cm', 'cmb', 'cmx','fug']

    # print to the console
    df_to_print = df[[*element_info_print, *signal_names_op_print]]

    # Filter devices based on current threshold and report those being filtered out
    current_mask = abs(df['ids']) > abs_ids_min
    filtered_devices = df.index[~current_mask].tolist()

    if filtered_devices:
        print(f"\nThe following devices were excluded (|Ids| < {abs_ids_min} A):")
        for device in filtered_devices:
            print(f"  - {device}: Ids = {df.loc[device, 'ids']:.3e} A")
        print()

    df_to_print = df_to_print[current_mask]
    print(df_to_print.T)

    # write to csv file
    csv_filename = "operating_point.csv"
    print(f"Writing {csv_filename}")
    df_to_print.T.to_csv(csv_filename)

    text_filename = "operating_point.txt"
    print(f"Writing {text_filename}")
    with open(text_filename, 'w') as f:
        f.write(df_to_print.T.to_string())

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
