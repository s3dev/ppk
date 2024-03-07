/**
    Purpose:    This module contains the tests (or checks) which are run 
                against the PyPI library file archive, before they are 
                moved to the secured (or secured)  environment.
    
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

#include <openssl/sha.h>
#include "base.h"
#include "filesys.h"
#include "ui.h"
#include "utils.h"

// Function prototypes
int run_tests(void);
int test_key(const char *fpath_key, const char *fpath_log);
int test_log(const char *fpath);

/**
    Run the archive verification tests.

    :Tests:
        - Verify the log has not been tampered with.
        - Verify the Snyk library vulnerability checks pass for all 
          libraries.

    @return     0 if all tests pass successfully, otherwise 1.
*/
int run_tests(void) {

    char    *path_key;
    char    *path_log;
    bool    passed = true;

    // Obtain the paths to the log and key files.
    path_key = findfile(PATH_TMP_PPK, ".key");
    path_log = findfile(PATH_TMP_PPK, ".log");
    // Run the tests.
    print_start("\nVerifying the integrity of the archive ..."); 
    if ( test_key(path_key, path_log) ) {
        print_warning("-- [TEST FAILURE]: The log file has been altered and is no longer reliable.");
        passed = false;
    }
    if ( test_log(path_log) ) {
        print_warning("-- [TEST FAILURE]: Snyk vulnerability checks failed.");
        passed = false;
    }
    if ( passed ) {
        print_done(0);
    } else {
        print_alert("Verification failures found. Libraries will *not* be transferred.");
    }
    free(path_key);
    free(path_log);
    return ( passed ) ? EXIT_SUCCESS : EXIT_FAILURE;
}

/**
    Test the log file key matches that of the log file.

    :Test:
        - A SHA256 hash is calculated against the log file and compared
          to the *.key file present in the archive. If the hashes match,
          the test passes. Otherwise the test fails.

    @param[in]  fpath_key   Explicit path to the key file.
    @param[in]  fpath_log   Explicit path to the log file.

    @return                 0 if the hashes match, otherwise 1.
*/
int test_key(const char *fpath_key, const char *fpath_log) {

    int             buffsz = 1024;
    int             bytes;
    int             hash_size = SHA256_DIGEST_LENGTH*2;
    char            key[hash_size + 1];
    char            hexdigest[hash_size + 1];
    char            msgbuff[127];
    unsigned char   _hash[SHA256_DIGEST_LENGTH];
    unsigned char   *buff = malloc(buffsz);
    FILE            *fp;
    SHA256_CTX      ctx;
    
    // Read the key file.
    if ( (fp = fopen(fpath_key, "r")) == NULL ) {
        reporterror("Key file not found.", false, false);
        return EXIT_FAILURE;
    }
    bytes = fread(key, sizeof(char), hash_size, fp);
    if ( bytes != hash_size ) {
        sprintf(msgbuff, "%d bytes read from key file, expected %d", bytes, SHA256_DIGEST_LENGTH*2);
        reporterror(msgbuff, false, false);
        return EXIT_FAILURE;
    }
    key[hash_size] = '\0';
    fclose(fp);
    // Read and hash the log file.
    if ( (fp = fopen(fpath_log, "r")) == NULL ) {
        reporterror("The log file cannot be found.", false, false);
        return EXIT_FAILURE;
    }
    SHA256_Init(&ctx);
    while ( (bytes = fread(buff, sizeof(char), buffsz, fp)) ) {
        SHA256_Update(&ctx, buff, bytes);
    }
    SHA256_Final(_hash, &ctx);
    for ( int i = 0; i < SHA256_DIGEST_LENGTH; ++i ) {
        sprintf(hexdigest + (i * 2), "%02x", _hash[i]);
    }
    hexdigest[hash_size] = '\0';
    fclose(fp);
    free(buff);
    // Compare the log file's hex digest with the key.
    return strcmp(hexdigest, key);
}

/**
    Test the verification log results.

    :Test:
        - If the 'Results:' tag in the file is PASS, the test will pass,
          otherwise the test will fail.

    @param[in]  fpath   Explicit path to the log file to be tested.

    @return             0 if the log file passes validation, otherwise 1.
*/
int test_log(const char *fpath) {

    int     bytes;
    int     size = 4;
    char    buff[size+1];
    char    msgbuff[127];
    FILE    *fp;

    if ( (fp = fopen(fpath, "r")) == NULL ) {
        reporterror("Log file not found.", false, false);
        return EXIT_FAILURE;
    }
    fseek(fp, -size-1, SEEK_END);  // End and back 5 chars (four+EOF)
    memset(buff, 0, sizeof(buff));  // Initialise he array to NULL.
    if ( (bytes = fread(buff, sizeof(char), size, fp)) != size ) {
        sprintf(msgbuff, "Expected %d bytes read, got %d.", size, bytes);
        reporterror(msgbuff, false, false);
        return EXIT_FAILURE;
    }
    fclose(fp);
    return strcmp(buff, "PASS") ? EXIT_FAILURE : EXIT_SUCCESS;
}

