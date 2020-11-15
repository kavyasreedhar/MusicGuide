#!/bin/bash

cd ../examples
rm $1.pdf
rm $1.ly
python3 $1.py
/home/users/sophliu/bin/lilypond $1.ly
evince $1.pdf
cd ../scripts
