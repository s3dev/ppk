/**
    Purpose:    This module provides user interface functionality for 
                easy terminal text colouring, via wrapped 'printf' calls.
    
    Developer:  J Berendt
    Email:      development@s3dev.uk

    Comments:   n/a

    Copyright (C) 73rd Street Development
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

#include <stdbool.h>
#include <stdio.h>
#include "../include/base.h"

/**
    Display an alert message (msg) in red, to stderr.

    @param[in]  msg     Message to be displayed.
*/
void print_alert(const char *msg) {
    fprintf(stderr, ANSI_B_RED "%s\n" ANSI_RST, msg);
}

/**
    Display a 'Done.' message in green, to stdout.

    @param[in]  add_newline     Insert a blank line above the message.
*/
void print_done(bool add_newline) {
    char *newline = ( add_newline ) ? "\n" : "";
    printf("%s" ANSI_B_GRN "Done.\n" ANSI_RST, newline);
}

/** 
    Print the copyright notice. 
*/
void print_notice(void) {
    printf("\n"
           "Copyright (C) 73rd Street Development\n"
           "\n"
           "This program is free software: you can redistribute it and/or modify\n"
           "it under the terms of the GNU General Public License as published by\n"
           "the Free Software Foundation, either version 3 of the License, or\n"
           "(at your option) any later version.\n"
           "\n"
           "This program is distributed in the hope that it will be useful,\n"
           "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
           "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
           "GNU General Public License for more details.\n"
           "\n"
           "You should have received a copy of the GNU General Public License\n"
           "along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n"
    );
}

/**
    Display an OK (msg) in green, to stdout.

    @param[in]  msg     Message to be displayed.
*/
void print_ok(const char *msg) {
    printf(ANSI_B_GRN "%s\n" ANSI_RST, msg);
}

/**
    Display a start-of-procesing message (msg) in cyan, to stdout.

    @param[in]  msg     Message to be displayed.
*/
void print_start(const char *msg) {
    printf(ANSI_B_CYN "%s\n" ANSI_RST, msg);
}

/**
    Display a warning message (msg) in yellow, to stderr.

    @param[in]  msg     Message to be displayed.
*/
void print_warning(const char *msg) {
    fprintf(stderr, ANSI_B_YLW "%s\n" ANSI_RST, msg);
}

