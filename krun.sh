#!/bin/bash

python $1.py
cd lilypond
lilypond ../$1.ly
cp $1.pdf ../
cp $1.midi ../
rm $1.pdf
rm $1.midi
cd ..
#rm $1.ly
cp $1.pdf /mnt/c/Users/kavya/Downloads
cp $1.midi /mnt/c/Users/kavya/Downloads
