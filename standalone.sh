#!/bin/bash

python2 setup.py build
mv build/exe* build/wpasetup
wget http://www.siue.edu/its/wireless/programs/oitca.cer
mv oitca.cer build/
makeself --xz --complevel 9 --nox11 $(pwd)/build/ wpasetup "Unofficial SIUE WPA SETUP" wpasetup/siuewpasetup