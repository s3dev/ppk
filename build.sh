#!/usr/bin/env bash

# Remove old stuff.
printf "\nRemoving old build ...\n"
rm -rf ./build ./dist ./ppk.egg-info ./requirements.txt

printf "\nBuilding the unpacker ...\n"
pushd ./ppk/libs/upack.d
make clean
make
popd

printf "\nInstalling required Python libraries ...\n"
python3 -m pip install build ppklib preqs utils4

printf "\nIncluding the installer ...\n"
mv {.,}install.sh

printf "\nUpdating requirements.txt file ...\n"
preqs . --replace

# The included files are controlled by MANIFEST.in
printf "\nBuilding source distribution ...\n"
python -m build --sdist

mv {,.}install.sh

printf "\nSetup complete.\n\n"
