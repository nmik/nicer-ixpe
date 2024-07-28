# Livetime calculation

Introduction
------------

When you select in time bins on the IXPE level2 data, the "LIVETIME" keyword in the headers of th efits files is not updated. This is because a correct calculation of the livetime can only be done on the level1 data. The LIVETIME keyword is propagqated to the PHA files and read by spectral fitting tools (e.g., XSPEC) to compute the flux in physical units. An incorrect LIVETIME will results in an incorrect flux estimation. Note that polarization parameters (Q/I and U/I, PD and PA) are not affected by this.

In this example script we provide the code to perfome a time selection of the level1 data and produce level2 data with the correct LIVETIME keyword. 

Instructions
------------

- Download the root folder for one of the IXPE observations. For example you can download "01003199/" from https://heasarc.gsfc.nasa.gov/FTP/ixpe/data/obs/01/. This can be as heavy as 10 GB!

- unzip the all the files in *event_l1* and *event_l2* folders.
- run the script with

    python livetime_computation.py --path 01003199/ --duration 10000 

where path is the path to the root folder with unzipped level1 and leverl 2 data, and the duration is the tentative time bin size in seconds (it will be rounded to make identical bins)'

    

