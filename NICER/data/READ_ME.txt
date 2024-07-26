BEFORE USING THESE NOTEBOOKS PLEASE FOLLOW THESE STEPS:

1) Initialize Heasoft and CALDB

2)Set your GEOMAG path and run nigeodown:
export GEOMAG_PATH=/to/your/local/geomag/path
nigeodown

3)Run the two following commands in terminal/shell to allow notebooks to run:
export HEADASNOQUERY=
export HEADASPROMPT=/dev/null

4)Download the following datasets with wget using these commands:

(3C 273)
wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2018_07//1010100105/
wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2018_07//1010100104/

(Cas A)
wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/2023_09//6010080272/
