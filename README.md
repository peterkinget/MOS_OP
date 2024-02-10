# MOS_OP

## Quick Demo
- clone the repository
- start a terminal on a computer with `python3`, `numpy` and `pandas`
- install `psf_utils` with `pip3 install psf_utils`
- go into the example files of the repository: `cd example_files_presized_OTA_tb`
- execute the script with the example files: `python3 ../MOS_OP.py dcOpInfo.info.ascii  element.info.ascii device_names_all.json`
- output displayed on your terminal  and saved in `operating_point.csv`
- execute the script with another shorter example: `../MOS_OP.py dcOpInfo.info.ascii
  element.info.ascii device_names_I0.json` producing the following output:
```
                  M1b         M2b         M3b         M4b         M5b         M6b         M7b         M8b
w                8.0u        8.0u       24.0u       24.0u       96.0u       32.0u       16.0u        8.0u
l              500.0n      500.0n      500.0n      500.0n      500.0n      500.0n      500.0n      500.0n
m                 1.0         1.0         1.0         1.0         1.0         1.0         1.0         1.0
as               4.0p        4.0p        8.0p        8.0p       26.0p       10.0p        6.0p        4.0p
ad               2.0p        2.0p        6.0p        6.0p       24.0p        8.0p        4.0p        2.0p
ps               9.0u        9.0u       27.0u       27.0u      108.0u       36.0u       18.0u        9.0u
pd               8.0p        8.0p       16.0p       16.0p       52.0p       20.0p       12.0p        8.0p
ids             99.5u       99.6u      -99.5u      -99.6u     -453.9u      453.9u      199.2u      100.0u
vgs            736.2m      736.5m     -722.3m     -722.3m     -730.5m      644.9m      644.9m      644.9m
vds               1.3         1.3     -722.3m     -730.5m        -1.3         1.2      513.5m      644.9m
vdsat          218.6m      218.7m     -258.5m     -258.5m     -267.6m      228.2m      218.7m      218.5m
region     saturation  saturation  saturation  saturation  saturation  saturation  saturation  saturation
vbs           -513.5m     -513.5m         0.0         0.0         0.0         0.0         0.0         0.0
vth            512.9m      513.0m     -479.6m     -479.6m     -479.3m      398.1m      412.0m      412.8m
vgsteff        223.2m      223.3m      243.7m      243.7m      252.0m      246.0m      232.1m      231.4m
gm             771.2u      771.5u      688.4u      688.9u        3.0m        3.3m        1.5m      755.2u
gds             14.2u       14.2u       11.1u       11.0u       36.6u       61.1u       45.9u       18.8u
gmb            140.7u      140.7u      226.0u      226.2u      997.0u      748.9u      343.7u      173.5u
gmoverid          7.7         7.7         6.9         6.9         6.7         7.2         7.5         7.6
self_gain        54.2        54.1        61.9        62.4        82.6        53.3        32.5        40.1
cgs             20.5f       20.5f       57.5f       57.5f      229.9f       82.8f       41.3f       20.6f
cgsovl           3.8f        3.8f       13.7f       13.7f       54.8f       15.4f        7.7f        3.8f
cgb              1.1f        1.1f        4.7f        4.7f       18.9f        4.7f        2.4f        1.2f
cgbovl         450.6z      450.6z      417.8z      417.8z      417.8z      450.6z      450.6z      450.6z
cgd              3.5f        3.5f       13.7f       13.7f       54.8f       14.2f        7.1f        3.6f
cgdovl           3.8f        3.8f       13.7f       13.7f       54.8f       15.4f        7.7f        3.8f
cbd              2.2f        2.2f        8.8f        8.8f       31.0f        9.9f        6.0f        2.9f
cjd              2.2f        2.2f        8.8f        8.8f       30.9f        9.7f        5.8f        2.8f
cbs              9.6f        9.6f       10.4f       10.4f       42.4f        7.4f        3.7f        1.9f
cjs              8.4f        8.4f         0.0         0.0         0.0         0.0         0.0         0.0
csd            122.0a      122.0a      -17.6a      -16.9a       -8.5a      496.5a      210.5a      116.0a
cm               7.7f        7.7f       20.6f       20.6f       82.4f       30.8f       15.4f        7.7f
cmb              1.4f        1.4f        6.6f        6.6f       26.4f        7.1f        3.5f        1.8f
cmx              1.6f        1.6f        2.7f        2.7f       10.4f        7.0f        3.4f        1.7f
fug              4.9G        4.9G        1.4G        1.4G        1.6G        5.1G        4.7G        4.7G
```

  
## Basic Usage
The python script `MOS_OP.py` takes in simulation results from a spectre
operating point simulation and tabulates them nicely on the terminal and
saves them in a csv file.

Usage: 

`python3 MOS_OP.py <name dcOPInfo.info ascii file> <name
element.info ascii file> <json file with device name dictionary>`

After a spectre *DC Analysis* with *Save Operating Point*, spectre saves
the operating point information in the `dcOPInfo.info` file and the
transistor sizing information in the `element.info` file in the folder
with the simulation results; that folder is typically located in
`<simulation results folder>/<name of the
cell>/spectre/schematic/psf/`. So if you are simulating
`presized_OTA_tb` and you ask ADE to save your simulation results in
`~/simulation`, you should look in
`~/simulation/presized_OTA_tb/spectre/schematic/psf/` after completing
the simulation.

These files are typically in binary format. You can convert them to
ascii with the `psf` command from cadence; on a workstation where you
can execute `virtuoso` you should be able to run:
```
psf dcOPInfo.info dcOPInfo.info.ascii
psf element.info element.info.ascii
```
Those ascii files can be read by `MOS_OP.py`. There are example files in the [example\_files\_presized\_OTA\_tb](example_files_presized_OTA_tb) folder. 

Next, you need to make a json dictionary of the (subset of the) devices
you want the script to display the operating point for. The format is:

```
{"device1_label_used_by_script": "spectre_reference_of_device1",
....
 "devicen_label_used_by_script": "spectre_reference_of_devicen"}
```

So, for example, the following dictionary names I7.M1, i.e. the M1 device in subcircuit I7, as "M1" in the print out and csv file:

```
{"M1": "I7.M1",
 "M2": "I7.M2",
 "M3": "I7.M3",
 "M4": "I7.M4",
 "M5": "I7.M5"}
```
There are examples in the
[example\_files\_presized\_OTA\_tb](example_files_presized_OTA_tb) folder:
e.g., [device_names_I0.json](example_files_presized_OTA_tb/device_names_I0.json) 

You do not need to include all devices, you can select devices of
interest only. 

## Tools Needed
- `python 3`
- `numpy`
- `pandas`
- `psf_utils` is a library for python that enables reading the ascii psf
  files available from <https://pypi.org/project/psf-utils/>  and can be
  installed with:  `pip install psf-utils` or `pip3 install
  psf-utils`. You need version 1.7 or later. 

## Example Circuit

The simulation example files provided in
[example\_files\_presized\_OTA\_tb](example_files_presized_OTA_tb) are
for this single-ended two-stage Miller OTA:

![OTASchematic](https://github.com/peterkinget/OP_Sandbox/blob/main/img/presized_OTA.png?raw=true)

Two OTAs have been placed in a testbench:

![TestBenchSchematic](https://github.com/peterkinget/OP_Sandbox/blob/main/img/tb_presized_OTA_black.png?raw=true)

The OTA instances are I0 and I7. Both have the same DC operating
point. The operating point for the transistors in the I0 instance can be
obtained with this [device names json
file](example_files_presized_OTA_tb/device_names_I0.json) with 
the following [output](img/example_output.md).

The 0.25um CMOS transistor models used for the simulation are available at [Nagendra
Krishnapura's CAD Tools
page](https://www.ee.iitm.ac.in/~nagendra/cadinfo.html). 

