/**
    Base header file for the ppk project's upack program.

    Updates:

    v0.2.0.dev1: Removed the explicit definition of __DEV_MODE as this is
    now invoked in the Makefile as: $ make MODE=dev

    v0.2.0.dev2: Updated the default production repo path to 
    /tmp/pip/repo.

    v0.2.1: See changelog.
*/


#ifndef _BASE_H

    #define _BASE_H
    // Include statements
    #include <errno.h>
    #include <stdbool.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    // Colours
    #define ANSI_B_CYN "\033[96m"
    #define ANSI_B_GRN "\033[92m"
    #define ANSI_B_RED "\033[91m"
    #define ANSI_B_YLW "\033[93m"
    #define ANSI_CYN "\033[36m"
    #define ANSI_GRN "\033[32m"
    #define ANSI_RED "\033[31m"
    #define ANSI_RST "\033[0m"
    // Paths
    #define PATH_TMP "/tmp/"
    #define PATH_TMP_PPK PATH_TMP ".ppk"
    #ifdef __DEV_MODE
        // Development paths
        #define PATH_REPO PATH_TMP "pip/repo"
    #else
        // Production paths
        #define PATH_REPO "/tmp/pip/repo"
    #endif /* __DEV_MODE */
    // Constants
    static const char *_APP_DESC = "PyPI library archive validation and unpacking utility.";
    static const char *_APP_LONG_NAME = "PPK: Archive Unpacker";
    static const char *_APP_NAME = "upack";
    static const char *_VERSION = "0.2.1";

#endif /* _BASE_H  */

