# OP_Sandbox

## Quick Start
- clone the repository
- start a terminal
- install `psf_utils` with `pip3 install psf_utils`
- go into the example files of the repository: `cd example_files_presized_OTA_tb`
- execute the script with the example files: `../MOS_Operating_Point_v0.1d.py dcOpInfo.info.ascii
  element.info.ascii device_names_all.json`
- check out your terminal  and `operating_point.csv`
- execute the script with another shorter example: `../MOS_Operating_Point_v0.1d.py dcOpInfo.info.ascii
  element.info.ascii device_names_I0.json`
- This is the [output](img/example_output.md) you should obtain. 
  
## Basic Usage
The python script `MOS_Operating_Point.py` takes in simulation results from a spectre operating point simulation and tabulates them nicely on the terminal and saves them in a csv file.

Usage: 

`MOS_Operating_Point.py <name dcOPInfo.info ascii file> <name
element.info ascii file> <json file with device name dictionary>`

After a spectre *DC Analysis* with *Save Operating Point*, spectre will
save the operating point information in the `dcOPInfo.info` file and the
transistor sizing information in the `element.info` file in the folder
with the simulation results; that folder is typically located in `<simulation results folder>/<name of the cell>/spectre/schematic/psf/`. So if you are simulating
`presized_OTA_tb`  and you save your simulation results in `~/simulation`,
you should look in `~/simulation/presized_OTA_tb/spectre/schematic/psf/`
after completing the simulation.

These files are typically in binary format. You can convert them to ascii with the `psf` command from cadence; run:
```
psf dcOPInfo.info dcOPInfo.info.ascii
psf element.info element.info.ascii
```
Those ascii files can be read by the script. There are example files in the [example\_files\_presized\_OTA\_tb](example_files_presized_OTA_tb) folder. 

You further need to make a dictionary of the devices in a json file you want the script to display the operating point. The format is:

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
There is are examples in the
[example\_files\_presized\_OTA\_tb](example_files_presized_OTA_tb) folder:
e.g., [devices.json](example_files_presized_OTA_tb/devices_all.json) 

## Tools Needed
- `python 3`
- `numpy`
- `pandas`
- `psf_utils` is a library for python that enables reading the ascii psf
  files available from <https://pypi.org/project/psf-utils/>  and can be
  installed with:
  
  `pip install psf-utils` or `pip3 install psf-utils` 

## Example Circuit

![alt text](https://github.com/peterkinget/OP_Sandbox/blob/main/img/presized_OTA.png?raw=true)

