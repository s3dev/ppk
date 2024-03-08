#!/usr/bin/env bash
#-------------------------------------------------------------------------
# Prog:     install.sh
# Version:  0.1.0
# Desc:     Primary installer script for the ppk project.
#
#           Using the inputs from the user, this script generates the 
#           ./bin/_ppk.sh script, which is a virtual environment specific
#           wrapper around ppk.py. Once that script is created, this 
#           script calls `make` to carry out the deployment.
#
# Use:      $ ./install.sh
#           
#           Follow the prompts ...
#
# Updates:
# 12.03.24  J. Berendt  Written
#-------------------------------------------------------------------------

# Initialise variables.
_dst=
_venv=
_dst_default="/usr/local/bin/"

#
# Create the _ppk.sh wrapper script, and make it executable.
#
# Note: Some of the variables being redirected into the file must remain
# unexpanded, as they are required by the script.
#
function create_wrapper {

    # Determine the explicit path to the venv's python executable.
    local path="$( find "${_venv}/bin" -name python )"

    # Create wrapper script.
    cat <<- EOF > ./bin/_ppk.sh
	#!/usr/bin/env bash

	_dir="\$( dirname "\$( realpath "\$0" )" )"
	"${path}" "\${_dir}/ppk.py" "\$@"

	EOF

    # Make the script executable.
    chmod 755 ./bin/_ppk.sh
}

#
# Prompt the user for ppk's deployment path.
#
# If a path does not exist, the user is re-prompted until a path which
# does exist is received. If the path is left blank, the default will be 
# used.
#
function get_deploy_path {
 
    local dst=
    printf "\nWhere will ppk be deployed? Leave blank to accept the default.\n"
    printf "  -- The default path is: %s\n" $_dst_default
    read -p "Enter the path: " dst
    if [ -z $dst ]; then
        _dst=$_dst_default
    elif [ ! -d $dst ]; then 
        printf "  -- Directory not found: (%s). Please try again.\n" "$dst"
        get_deploy_path
    else
        _dst=$dst
    fi
}

#
# Prompt the user for the path to the Python venv to be used.
#
# If a path does not exist, the user is re-prompted until a path which
# does exist is received.
#
function get_venv_path {
 
    local venv=
    read -p "Path to the Python virtual environment to be used: " venv
    if [ ! -d $venv ]; then
        printf "  -- Directory not found: (%s). Please try again.\n" "$venv"
        get_venv_path
    else
        _venv=$venv
    fi
}

#
# Print the installer's startup message.
#
# Note: This message in this block uses *tab* characters.
#
function startup {

    cat <<- EOF

	-------------------
	   ppk Installer
	-------------------

	EOF
}

#
# Call make to complete the installation, with the user-provided
# installation directory.
#
function call_make {
    make dst="${_dst}"
}

# Primary controller and entry point.
function main {
    [ $? -eq 0 ] && startup
    [ $? -eq 0 ] && get_venv_path
    [ $? -eq 0 ] && get_deploy_path
    [ $? -eq 0 ] && create_wrapper
    [ $? -eq 0 ] && call_make
}

main

