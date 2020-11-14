#!/bin/bash

python birthday.py
cd lilypond
lilypond birthday.ly
cp birthday.pdf ../
rm birthday.pdf
cd ..
