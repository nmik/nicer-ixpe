# Background rejection

Introduction
------------

The Jupyter notebook in this folder will run the filter_background.py script, and then visualize the results using the xpbin tool in ixpeobssim. 

If you do not wish to run the entire notebook, and instead want to simply apply the background rejection script, please follow the instructions below. 

Instructions
------------

- Download the root folder for one of the IXPE observations. For example you can download "02009701/" from https://heasarc.gsfc.nasa.gov/FTP/ixpe/data/obs/01/. This can be as heavy as 10 GB!

- unzip the all the files in *event_l1* and *event_l2* folders.
- run the script with

       python filter_background.py --pathtolevel2file --pathtolevel1file --output rej
  
where pathtolevel2file and pathtolevel1file are the paths to the root folder with unzipped level2 and level 1 data. This will produce _rej-tagged fits files containing a list of X-ray only events.



    
