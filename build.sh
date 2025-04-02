#!/usr/bin/env bash

# Remove old stuff.
printf "\nRemoving old build ...\n"
rm -rf ./build ./dist ./ppk.egg-info ./requirements.txt

printf "\nBuilding the unpacker ...\n"
pushd ./lib/upack.d
make
popd

printf "\nInstalling required Python libraries ...\n"
python3 -m pip install beautifulsoup4 build preqs requests utils4

printf "\nIncluding the installer ...\n"
mv {.,}install.sh

printf "\nUpdating requirements.txt file ...\n"
preqs . --replace

printf "\nBuilding source distribution ...\n"
python -m build --sdist

mv {,.}install.sh

printf "\nSetup complete.\n\n"
