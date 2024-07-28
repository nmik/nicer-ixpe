# Livetime calculation

Introduction
------------

When you select in time bins on the IXPE level2 data, the "LIVETIME" keyword in the headers of th efits files is not updated. This is because a correct calculation of the livetime can only be done on the level1 data. The LIVETIME keyword is propagqated to the PHA files and read by spectral fitting tools (e.g., XSPEC) to compute the flux in physical units. An incorrect LIVETIME will results in an incorrect flux estimation. Note that polarization parameters (Q/I and U/I, PD and PA) are not affected by this.

In this example script we provide the code to perfome a time selection of the level1 data and produce level2 data with the correct LIVETIME keyword. 

Instructions
------------

- Download the following files form the archive at this link: https://heasarc.gsfc.nasa.gov/FTP/ixpe/data/obs/01/01003199/event_l1/

    - ixpe01003102_det1_evt1_v03.fits.gz
    - ixpe01003102_det3_evt1_v03.fits.gz
    - ixpe01003102_det2_evt1_v03.fits.gz

- unzip the files
- un

