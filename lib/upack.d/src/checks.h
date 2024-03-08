/**
    Header file for the checks.c module.
*/

#ifndef _CHECKS_H
#define _CHECKS_H

/**
    Run the archive verification tests.

    :Tests:
        - Verify the log has not been tampered with.
        - Verify the Snyk library vulnerability checks pass for all 
          libraries.

    @return     0 if all tests pass successfully, otherwise 1.
*/
int run_tests(void);

/**
    Test the log file key matches that of the log file.

    :Test:
        - A SHA256 hash is calculated against the log file and compared
          to the *.key file present in the archive. If the hashes match,
          the test passes. Otherwise the test fails.

    @param[in]  fpath_key   Explicit path to the key file.
    @param[in]  fpath_log   Explicit path to the log file.

    @return                 0 if the log file passes validation.
                            Otherwise, -1 if the file was not found, -2 for
                            a read failure, or -3 if the log file was not 
                            found. Any non-zero positive integer for a 
                            validation failure.
*/
int test_key(const char *fpath_key, const char *fpath_log);

/**
    Test the verification log results.

    :Test:
        - If the 'Results:' tag in the file is PASS, the test will pass,
          otherwise the test will fail.

    @param[in]  fpath   Explicit path to the log file to be tested.

    @return             0 if the log file passes validation.
                        Otherwise, -1 if the file was not found or -2 for a
                        read failure. Any non-zero positive integer for a 
                        validation failure.
*/
int test_log(const char *fpath);

#endif /* _CHECKS_H */

