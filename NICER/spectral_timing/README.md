In this tutorial, we will run a quicklook spectrotemporal analysis of a NICER observation of one epoch of the 2018 outburst of the accreting black hole MAXI 1820+070, largely reproducing the results from, e.g., [Wang et al. 2021](https://ui.adsabs.harvard.edu/abs/2021ApJ...910L...3W/abstract), [De Marco et al. 2021](https://ui.adsabs.harvard.edu/abs/2021A%26A...654A..14D/abstract). We will not give a scientific interpretation, just pure exploration.

The dataset used for the analysis can be downloaded [on Zenodo](https://zenodo.org/records/13149195). There are three versions of the file:

+ the original ~2.4GB FITS file (ni1200120106_0mpu7_cl_bary.evt.gz)
+ a reduced ~720MB HDF5 file containing only part of the data, to help with slow connections (data_small.hdf5)
+ a further reduced ~370MB HDF5 file, containing even less data but still adequate for most purposes in the tutorial (data_smaller.hdf5).

DISCLAIMER: this dataset was downloaded from the NICER archive and only run through `barycorr` to refer the photon arrival times to the solar system barycenter. We did not run the official NICER pipeline on these data, and some of the features appearing in the power spectrum are instrumental artifacts. Data are not science-ready and only good for demonstration purposes. For more information (thanks Paul Ray and Sara Motta for discussion): 

+ [Some Notes on Timing Analyses and NICER Data (using also MAXI J1820+070 as an example)](https://heasarc.gsfc.nasa.gov/docs/nicer/data_analysis/workshops/nicer_wkshp_timing_5_4_21.pdf)
+ [NICER Analysis Threads](https://heasarc.gsfc.nasa.gov/docs/nicer/analysis_threads/)

See [Uttley et al. 2014](https://ui.adsabs.harvard.edu/abs/2014A%26ARv..22...72U/abstract), [Bachetti & Huppenkothen 2022](https://ui.adsabs.harvard.edu/abs/2022arXiv220907954B/abstract) for reviews on most statistical concepts and terminology used here.
