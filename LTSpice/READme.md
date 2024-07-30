# LTSpice Example using the a Miller OTA built on the MOSbius chip

## Required
* [spicelib](https://pypi.org/project/spicelib/) 
* pandas

## Running the Script

This folder contains the necessary files to run the script:
```
python3 process_LTSpice_OP_v0.2.py Miller_OTA_pin_feedback_OP.log
name_dict.json `
```

This example is based on the included OTA schematic (see below). To run
the script you need to save the `.log` file from your LTSpice `.OP` simulation
and create a `.json` file with a list of the devices you want listed in
your table printout and their shortened name; see
[name_dict.json](./name_dict.json); you find the long device names in
your `.log` file. 

You should get the following output. 

```
              M1      M2      M3      M4     M5a     M5b     M5c     M5d      M6      M7      M8
Model      cmosp   cmosp   cmosn   cmosn   cmosn   cmosn   cmosn   cmosn   cmosp   cmosp   cmosp
Id        -94.9u  -94.9u   94.9u   94.9u  410.0u  410.0u  410.0u  410.0u   -1.6m -190.0u -100.0u
Vgs      -767.0m -767.0m  804.0m  804.0m  806.0m  806.0m  806.0m  806.0m -938.0m -938.0m -938.0m
Vds         -1.2    -1.2  804.0m  806.0m     1.2     1.2     1.2     1.2    -1.2 -483.0m -938.0m
Vbs          0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0     0.0
Vth      -663.0m -663.0m  577.0m  577.0m  569.0m  569.0m  569.0m  569.0m -663.0m -663.0m -663.0m
Vdsat    -140.0m -140.0m  208.0m  208.0m  214.0m  214.0m  214.0m  214.0m -270.0m -270.0m -270.0m
Vov      -104.0m -104.0m  227.0m  227.0m  237.0m  237.0m  237.0m  237.0m -275.0m -275.0m -275.0m
Gm          1.1m    1.1m  730.0u  730.0u    3.0m    3.0m    3.0m    3.0m   10.1m    1.2m  617.0u
Gds        10.5u   10.5u   15.9u   15.8u   57.7u   57.7u   57.7u   57.7u  125.0u   32.3u    8.8u
Gmb       482.0u  482.0u  229.0u  229.0u  956.0u  956.0u  956.0u  956.0u    4.4m  510.0u  270.0u
gm/Id      -11.8   -11.8     7.7     7.7     7.4     7.4     7.4     7.4    -6.2    -6.2    -6.2
Va          -9.0    -9.0     6.0     6.0     7.1     7.1     7.1     7.1   -13.1    -5.9   -11.4
selfgain   106.7   106.7    45.9    46.2    52.9    52.9    52.9    52.9    80.8    36.2    70.1
Cgstot    276.8f  276.8f   24.5f   24.5f   97.6f   97.6f   97.6f   97.6f    1.1p  142.4f   71.3f
Cgdtot    109.6f  109.6f    7.5f    7.5f   30.0f   30.0f   30.0f   30.0f  438.0f   55.0f   27.4f
Cbdtot    167.6f  167.8f   15.6f   15.6f   57.0f   57.0f   57.0f   57.0f  666.0f   99.9f   44.4f
Cbstot    294.0f  294.0f   23.4f   23.4f   93.7f   93.7f   93.7f   93.7f    1.2p  148.0f   74.0f
Cbdj       83.8f   83.9f    7.8f    7.8f   28.6f   28.6f   28.6f   28.6f  333.0f   49.9f   22.2f
Cbsj      119.0f  119.0f   10.1f   10.1f   40.4f   40.4f   40.4f   40.4f  475.0f   59.3f   29.7f
Cgsov      54.8f   54.8f    3.9f    3.9f   15.4f   15.4f   15.4f   15.4f  219.0f   27.4f   13.7f
Cgdov      54.8f   54.8f    3.9f    3.9f   15.4f   15.4f   15.4f   15.4f  219.0f   27.4f   13.7f
Cgbov      10.0a   10.0a  901.0z  901.0z    3.6a    3.6a    3.6a    3.6a   40.1a    5.0a    2.5a
Cgg       302.0f  302.0f   25.7f   25.7f  103.0f  103.0f  103.0f  103.0f    1.2p  154.0f   77.0f
_Cgd      -54.8f  -54.8f   -3.6f   -3.6f  -14.6f  -14.6f  -14.6f  -14.6f -219.0f  -27.6f  -13.7f
_Cgs     -222.0f -222.0f  -20.6f  -20.6f  -82.2f  -82.2f  -82.2f  -82.2f -921.0f -115.0f  -57.6f
_Cdg     -133.0f -133.0f  -11.3f  -11.3f  -45.0f  -45.0f  -45.0f  -45.0f -549.0f  -68.9f  -34.3f
Cdd       139.0f  139.0f   11.6f   11.6f   43.5f   43.5f   43.5f   43.5f  552.0f   77.5f   35.9f
_Cds      112.0f  112.0f   10.0f   10.0f   39.8f   39.8f   39.8f   39.8f  468.0f   58.6f   29.3f
_Cbg      -35.7f  -35.7f   -3.2f   -3.2f  -12.8f  -12.8f  -12.8f  -12.8f -134.0f  -16.6f   -8.4f
_Cbd      -83.8f  -83.9f   -7.8f   -7.8f  -28.4f  -28.4f  -28.4f  -28.4f -333.0f  -50.0f  -22.2f
_Cbs     -175.0f -175.0f  -13.3f  -13.3f  -53.3f  -53.3f  -53.3f  -53.3f -708.0f  -88.7f  -44.3f
fT        461.3M  461.3M    3.6G    3.6G    3.8G    3.8G    3.8G    3.8G    1.0G  943.3M  994.9M
fD        401.1M  400.9M    2.9G    2.9G    3.1G    3.1G    3.1G    3.1G  890.1M  768.5M  848.7M
Wrote CSV file
```

## Schematic and LTSpice Files for the Example

![Schematic](./test.png)

![Schematic](./MOSbius_Miller_OTA_pMOS_schematic_example/Miller_OTA_pin_feedback_OP.png) 

The LTspice schematic and model files are in the
[MOSbius_Miller_OTA_pMOS_schematic_example](./MOSbius_Miller_OTA_pMOS_schematic_example)
folder. For the operating point, use the `Miller_OTA_pin_feedback.asc`
schematic. There are other files for various other simulations as well,
you can ignore them for the purpose of the operating point. After
running the simulation, make sure to copy the `.log` file. If you close
LTSpice, the log file gets deleted. 

