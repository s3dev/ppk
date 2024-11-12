#!/usr/bin/env bash

# Remove old stuff.
printf "\nRemoving old build ...\n"
rm -rf ./build ./dist ./ppk.egg-info ./requirements.txt

printf "\nBuilding the unpacker ...\n"
pushd ./lib/upack.d/src
make
popd

printf "\nIncluding the installer ...\n"
mv {.,}install.sh

printf "\nUpdating requirements.txt file ...\n"
preqs . --replace

printf "\nBuilding source distribution ...\n"
python -m build --sdist

mv {,.}install.sh

printf "\nSetup complete.\n\n"
