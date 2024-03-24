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
pipreqs . --force

printf "\nBuilding wheel ...\n"
./.setup.py sdist

mv {,.}install.sh

printf "\nSetup complete.\n\n"
