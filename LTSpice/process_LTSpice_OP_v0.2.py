#!/usr/bin/env python3
#
# Peter Kinget
#
# December 2022
# v0   processing all devices from log file
# v0.1 adding a list of device name mappings and selection
#        --> needs to be a json file with "device label" "device name" pairs where "device name" is the
#            actual name in the log file and schematic
#
# May 2024
# v0.2 upgraded to spicelib; PyLTSpice was upgraded and does not have the SemiDevOpReader in the same place anymore
#

import sys
import math
import json
#from PyLTSpice import LTSpice_SemiDevOpReader
from spicelib.log import semi_dev_op_reader as LTSpice_SemiDevOpReader
import pandas as pd
pd.set_eng_float_format(accuracy=1, use_eng_prefix=True)

# configuration
# logfile = './MobiusChip_v3_OTA_two_stage_4312_tb.log'
try:
    logfile = sys.argv[1]
    devicefile = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <name log file to process> <json file with device names>")

device_type = 'BSIM3 MOSFETS'

# Read all the device operating points from the log file
devices = LTSpice_SemiDevOpReader.opLogReader(logfile)

# devices is a dictionary with as keys the device types
# now we pick up the devices of interest
MOS_devices = devices[device_type]

# MOS_devices is a dictionary with as key the device names

# read the names and the tags of the devices of interest into a dictionary
with open(devicefile) as f:
    json_data = f.read()
name_dict = json.loads(json_data)
# reverse mapping
name2_dict=dict(zip(name_dict.values(),name_dict.keys()))

# Let's make a dataframe of the operating point information of the MOS devices
df = pd.DataFrame(MOS_devices)

# df.index --> are the rows
#       ['Model', 'Id', 'Vgs', 'Vds', 'Vbs', 'Vth', 'Vdsat', 'Gm', 'Gds', 'Gmb',
#        'Cbd', 'Cbs', 'Cgsov', 'Cgdov', 'Cgbov', 'dQgdVgb', 'dQgdVdb',
#        'dQgdVsb', 'dQddVgb', 'dQddVdb', 'dQddVsb', 'dQbdVgb', 'dQbdVdb',
#        'dQbdVsb']
#
# df.columns --> are the columns
#        these are the device names
#       ['m:x1:x11:m2:p', 'm:x1:x11:m1:p', 'm:x1:x9:m1:p', 'm:x23:x11:m2:p',
#        'm:x23:x11:m1:p', 'm:x23:x9:m1:p', 'm:x1:x8:m7:n', 'm:x1:x8:m6:n',
#        'm:x1:x8:m5:n', 'm:x1:x8:m4:n', 'm:x1:x8:m3:n', 'm:x1:x8:m2:n',
#        'm:x1:x8:m1:n', 'm:x1:x5:m1:n', 'm:x1:x4:m1:n', 'm:x23:x8:m7:n',
#        'm:x23:x8:m6:n', 'm:x23:x8:m5:n', 'm:x23:x8:m4:n', 'm:x23:x8:m3:n',
#        'm:x23:x8:m2:n', 'm:x23:x8:m1:n', 'm:x23:x5:m1:n', 'm:x23:x4:m1:n']

# select only the devices of interest 
df_s=df[name_dict.values()]
# relabel the columns
new_names = [name2_dict[label] for label in df_s.columns]
df_s.columns = new_names

# relabel the rows
new_labels = ['Model', 'Id', 'Vgs', 'Vds', 'Vbs', 'Vth', 'Vdsat', 'Gm', 'Gds', 'Gmb',
       'Cbdj', 'Cbsj', 'Cgsov', 'Cgdov', 'Cgbov', 'Cgg', '_Cgd',
       '_Cgs', '_Cdg', 'Cdd', '_Cds', '_Cbg', '_Cbd',
       '_Cbs']
df_s.index = new_labels

# transpose the dataframe --> the rows are the devices, the columns are the small-signal parameters
df_sT = df_s.T

# compute some additional parameters
# note some type casting needs to be done to avoid divide by zero errors
df_sT['Vov']=df_sT['Vgs']-df_sT['Vth']
df_sT['gm/Id']=df_sT['Gm'].astype('float64')/df_sT['Id'].astype('float64')
df_sT['selfgain']=df_sT['Gm'].astype('float64')/df_sT['Gds'].astype('float64')
df_sT['Va']=df_sT['Id'].astype('float64')/df_sT['Gds'].astype('float64')
df_sT['Cbdtot']=df_sT['Cbdj']-df_sT['_Cbd']
df_sT['Cbstot']=df_sT['Cbsj']-df_sT['_Cbs']
df_sT['Cgstot']=df_sT['Cgsov']-df_sT['_Cgs']
df_sT['Cgdtot']=df_sT['Cgdov']-df_sT['_Cgd']
df_sT['fT']=df_sT['Gm']/2/math.pi/(df_sT['Cgstot']+df_sT['Cgdtot'])
df_sT['fD']=df_sT['Gm']/2/math.pi/(df_sT['Cgstot']+df_sT['Cbdtot'])

# reorder the parameters
new_order = ['Model', 'Id', 'Vgs', 'Vds', 'Vbs', 'Vth', 'Vdsat', 'Vov',
             'Gm', 'Gds', 'Gmb', 'gm/Id', 'Va', 'selfgain',
             'Cgstot', 'Cgdtot', 'Cbdtot', 'Cbstot', 
             'Cbdj', 'Cbsj', 'Cgsov', 'Cgdov', 'Cgbov', 'Cgg', '_Cgd',
             '_Cgs', '_Cdg', 'Cdd', '_Cds', '_Cbg', '_Cbd', '_Cbs',
             'fT', 'fD' ]

df_2 = df_sT[new_order]

# print the results but with the rows the parameters and the columns the devices
print(df_2.T)

# write to CSV file
df_2.to_csv('operating_point.csv')
print("Wrote CSV file")



