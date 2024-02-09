#!/usr/bin/env python
# coding: utf-8
#
# # MOS Operating Point
# Peter Kinget
# December 2023
# 
# Reading PSF files from cadence dc operating point simulation
# 
# Using psf-utils from K. Kundert at https://github.com/KenKundert/psf_utils/tree/master
# 
# Install psf-utils with pip3
################################################################################
import sys
import os
import numpy as np
import pandas as pd
pd.set_eng_float_format(accuracy=1, use_eng_prefix=True)
import json
#
from psf_utils import PSF
from inform import Error, display
################################################################################
def psf_list_signals(psf, beginning=""):
    for signal in psf.all_signals():
        # print(signal.name[0:len(beginning)])
        if (signal.name[0:len(beginning)]==beginning):
            print(signal.name, signal.units)

def collect_transistors_data(psf, transistors, signal_names, tor_signal_separator = '.'): 
    transistors_data = {}
    for transistor in transistors:
        transistors_data[transistor] = {}
        for signal in signal_names_op:
            tor_signal_name = transistor + tor_signal_separator + signal
            transistors_data[transistor][signal] = float(psf.get_signal(tor_signal_name).ordinate)
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
# get the commandline parameters
try:
    dcopfile = sys.argv[1]
    devicefile = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name log file to process> <json file with device names>")

# read the psf dcop file
psf = PSF(dcopfile)

# for debugging
# psf_list_signals(psf)

# read the transistor name file
with open(devicefile) as f:
    json_data = f.read()
    
# create transistor name dictionaries to go from netlist names to shortcuts and back
transistor_names_shortcut_to_netlist = json.loads(json_data)
transistor_names_shortcuts = transistor_names_shortcut_to_netlist.keys()
transistor_names_netlist = transistor_names_shortcut_to_netlist.values()
transistor_names_netlist_to_shortcut = dict(zip(transistor_names_netlist,transistor_names_shortcuts))

# parameters to read from the dcop file
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
transistors_data = collect_transistors_data(psf, transistor_names_netlist_to_shortcut.keys(), signal_names_op)
df = pd.DataFrame(transistors_data).T

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
signal_names_op_print = [ 'ids', 'vgs', 'vds', 'vdsat', 'region',
                          'vbs', 'vth', 'vgsteff', 
                          'gm', 'gds', 'gmb', 'gmoverid', 'self_gain', 
                          'cgs', 'cgsovl', 'cgb', 'cgbovl', 'cgd', 'cgdovl',
                          'cbd', 'cjd', 'cbs' , 'cjs',
                          'csd', 'cm', 'cmb', 'cmx','fug']

# print to the console
print(df[signal_names_op_print].T)
# df[signal_names_op_print].loc[["M1", "M1b"]].T
# df[signal_names_op_print].T

# write to csv file
csv_filename = "operating_point.csv"
df[signal_names_op_print].T.to_csv(csv_filename)

