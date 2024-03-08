/**
    App:        upack
    Purpose:    The upack program provides the Python library bundle
                verification and u(n)pack(ing) functionality, to the ppk
                project.

                Specifically, upack is responsible for verifying the
                integrity of the Python library bundle (encrypted .7z file)
                which was created by ppk's 'pack' program. Once the
                integrity of the .7z file is verified, the contents of the
                archive are transferred into the local pip repository.
                If the contents of the archive fails verification, the
                user is alerted and the archive is destroyed.

    Developer:  J Berendt
    Email:      development@s3dev.uk

    Comments:   To enhance the security of transferring Python libraries
                into a secured environment, the decision was made that
                this unpacking program should be a *compiled* program,
                so it was designed and written in C. The rationale behind
                this descision is to discourage code modification
                (hacking), thus allowing unvalidated (and potentially
                malicious) libraries to be transferred into a secured or
                sensitive environment.

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

#include "base.h"
#include "checks.h"
#include "filesys.h"
#include "ui.h"
#include "utils.h"

/**
    Verify the command line argument(s) are as required.

    If *any* test fails, this is considered a fatal error, thus exiting
    the program. The error reporting and exiting is handled by the
    reporterror function.

    :Tests:
        - Number of arguments (aside from the program itself), is 1.
        - The file must have a .7z extension.
        - The file must exist.

    @param[in] argc     Number of arguments passed.
    @param[in] argv     Array of command line argument strings.

    @return             0, if the arguments are found as expected.
*/
int verify_args(int argc, const char *argv[]) {

    char    msgbuff[256];
    char    *ext;
    FILE    *fp;

    // Test argument count.
    if ( argc != 2 ) {
        reporterror("Invalid number of arguments. Please refer to the program usage.", true, true);
    }
    // Test for --help argument.
    if ( (!strcmp(argv[1], "-h" )) || (!strcmp(argv[1], "--help")) ) {
        usage(true, true);
    }
    // Verify the passed file exists.
    if ( (fp = fopen(argv[1], "r")) == NULL ){
        sprintf(msgbuff, "%s: %s", strerror(errno), argv[1]);
        reporterror(msgbuff, false, true);
    }
    fclose(fp);

    // Verify the file has a .7z extension.
    if ( ((ext = strrchr(argv[1], '.')) == NULL) || (strcmp(ext, ".7z")) ) {
        reporterror("A .7z file is required, please refer to the program usage.", true, true);
    }
    return EXIT_SUCCESS;
}

/**
    Program entry point and primary process controller.

    The program's flow control logic works on the basis of a running
    'boolean', in the form of *exit codes*. A zero exit code signals a
    successful completion, whereas a non-zero exit code signals an error.

    More specifically, if any step in the process fails, all subsequent
    processes are aborted, as each step requires the successful completion
    of the previous step.

    @param[in] argc     Number of arguments passed.
    @param[in] argv     Array of command line argument strings.

    @return             0, if the program completes successfully,
                        otherwise 1.
*/
int main(int argc, const char *argv[]) {

    int excode;

    excode = verify_args(argc, argv);
    if ( !excode ) excode = unzip(argv[1], PATH_TMP_PPK);
    if ( !excode ) excode = run_tests();
    if ( !excode ) excode = moveall(PATH_TMP_PPK, PATH_REPO, false);
    // Delete the unpacking area regardless of the outcome.
    removeall(PATH_TMP_PPK, 1, 0);
    if ( excode != 0 ) {
        print_warning("\nDone. Ended in error.");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
