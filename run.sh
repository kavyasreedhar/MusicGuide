#!/bin/bash

python birthday.py
cd lilypond
lilypond ../birthday.ly
cp birthday.pdf ../
rm birthday.pdf
cd ..
rm birthday.ly
evince birthday.pdf &
