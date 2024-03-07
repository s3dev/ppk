/**
    Purpose:    This module provides generalised utility-based functions
                for use throughout the project.

    Developer:  J Berendt
    Email:      jeremy.berendt@rolls-royce.com

    Comments:   n/a

    Copyright (C) 2023 Rolls-Royce, plc.
    This file is part of the ppk project's upack program.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "base.h"
#include "ui.h"

// Function prototypes
void reporterror(const char *msg, bool show_usage, bool fatal);
void usage(bool notice, bool exit_zero);

/**
    Display an error message and exit the program if instructed.

    @param[in] msg          Message to be displayed.
                            The message is prepended with a red "[ERROR]: "
                            string.
    @param[in] show_usage   If true, the program's usage message is 
                            displayed after the error message.
    @param[in] fatal        If true, the program is exited with exit
                            code 1, and an exiting statement is printed in
                            yellow.
    @return                 Void.
*/
void reporterror(const char *msg, bool show_usage, bool fatal) {
    fprintf(stderr, "\n" ANSI_B_RED "[ERROR]: " ANSI_RST "%s\n", msg);
    if ( show_usage ) usage(false, false);
    if ( fatal ) {
        fprintf(stderr, "\n" ANSI_B_YLW "Fatal error, exiting." ANSI_RST "\n\n");
        exit(EXIT_FAILURE);
    }
}

/**
    Display the program's usage statement.

    @param[in]  notice      Display the license notice.
    @param[in]  exit_zero   If true, exit the program after the usage is 
                            displayed, with exit code 0.

    @return                 Void.
*/
void usage(bool notice, bool exit_zero) {
    printf(
           "\n%s - v%s\n"
           "%s\n"
           "\n"
           "Usage: %s [--help] [FILE]\n",
           _APP_LONG_NAME,
           _VERSION,
           _APP_DESC,
           _APP_NAME
    );
    printf(
           "\n"
           "Required positional arguments:\n"
           "  FILE          The .zip file archive (as created by ppk) to be verified\n"
           "                and unpacked into the pip repository.\n"
           "\n"
           "Optional arguments:\n"
           "  -h, --help    Display this help and exit.\n"
           "\n"
           "Example: To verify and unpack a .zip file archive:\n"
           "  $ %s /path/to/things/library-0.0.7-cp311-cp311-manylinux2014_x86_64.zip\n"
           "\n",
           _APP_NAME
    );
    if ( notice ) print_notice();
    if ( exit_zero ) exit(0);
}

