#!/bin/bash

rm ./source/url2features.rst
rm ./source/modules.rst

make clean
sphinx-apidoc -o ./source ../projit
make html


