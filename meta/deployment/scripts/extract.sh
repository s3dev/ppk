#!/usr/bin/env bash

pkg="ppk"

# Extract the archive into the local ./ directory.
tar -zxvf ${pkg}-*.tar.gz -C ./ --strip-components=1

# Remove unneeded files.
printf "\nRemoving unnecessary files ...\n"
rm ./setup.cfg PKG-INFO
rm -rf ./"${pkg}.egg-info"
printf "Done.\n\n"

printf "Extraction complete.\n\n"

