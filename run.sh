#!/bin/bash

python $1.py
cd lilypond
lilypond ../$1.ly
cp $1.pdf ../
rm $1.pdf
cd ..
rm $1.ly
