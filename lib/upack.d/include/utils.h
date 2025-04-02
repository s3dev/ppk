/**
    Header file for the utils.c module.
*/

#ifndef _UTILS_H
#define _UTILS_H

#include <stdbool.h>

/**
    Verify a file is a 7zip archive.

    Notes:
        A file is tested to be a 7zip archive by checking the first six
        bytes of the file itself, *not* using the file extension.

    @param path Pointer to the full path of the file to be tested.
    @return Returns true if the first six bytes of the file match the
            expected file signature for a 7zip archive, namely:

            - 0x37 0x7A 0xBC 0xAF 0x27 0x1C
*/
bool is7zip(const char *path);

/**
    Display an error message (to stderr) and exit the program if instructed.

    @param[in] msg          Message to be displayed.
                            The message is prepended with a red "[ERROR]: "
                            string.
    @param[in] show_usage   If non-zero, The program's usage message is
                            displayed after the error message.
    @param[in] fatal        If non-zero, the program is exited with exit
                            code 1, and an exiting statement is printed in
                            yellow.
    @return                 Void.
*/
void reporterror(const char *msg, int show_usage, int fatal);

/**
    Calculate and return the SHA256 hash for a given string.

    Note: The returned pointer **must** be free'd by the caller.

    @param[in] string   Pointer to a character array to be hashed.

    @return             A pointer to the SHA256 hash string, as a 
                        hexidecimal digest.

*/
char *sha256_digest(const char *string);

/**
    Display the program's usage statement.

    @param[in]  notice      Display the license notice.
    @param[in]  exit_zero   If true, exit the program after the usage is 
                            displayed, with exit code 0.

    @return                 Void.
*/
void usage(bool notice, bool exit_zero);

#endif /* _UTILS_H */

