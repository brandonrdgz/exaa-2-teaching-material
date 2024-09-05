#!/bin/bash

if ! $(which pip3 &> /dev/null); then
   echo -e "\npip3 is not installed"
   exit
fi

python3 -m pip install beautifulsoup4