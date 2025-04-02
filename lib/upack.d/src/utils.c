/**
    Purpose:    This module provides generalised utility-based functions
                for use throughout the project.

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

#include <openssl/sha.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/base.h"
#include "../include/ui.h"

// Function prototypes
bool is7zip(const char *path);
void reporterror(const char *msg, bool show_usage, bool fatal);
char *sha256_digest(const char *string);
void usage(bool notice, bool exit_zero);

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
bool
is7zip(const char *path) {

    char msgbuf[256];
    size_t bytes;
    unsigned char buf[6];
    FILE *fp;

    if ( (fp = fopen(path, "rb")) == NULL ) {
        perror("Error opening archive for file type testing");
        return false;
    }
    if ( (bytes = fread(buf, 1, 6, fp)) != 6 ) {
        fclose(fp);
        sprintf(msgbuf, "Expecting a 6-byte read, got %ld\n", bytes);
        reporterror(msgbuf, false, true);
        return false;
    }
    fclose(fp);
    if ( !(   buf[0] == 0x37 
           && buf[1] == 0x7a 
           && buf[2] == 0xbc 
           && buf[3] == 0xaf 
           && buf[4] == 0x27 
           && buf[5] == 0x1c) ) {
        return false;
    }
    return true;
}

/**
    Display an error message (to stderr) and exit the program if instructed.

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
    Calculate and return the SHA256 hash for a given string.

    Note: The returned pointer **must** be free'd by the caller.

    @param[in] string   Pointer to a character array to be hashed.

    @return             A pointer to the SHA256 hash string, as a 
                        hexidecimal digest.

*/
char *sha256_digest(const char *string) {

    char            *digest;    // malloc 65 bytes (hex + NULL)
    unsigned char   *hash;      // malloc 32 bytes
    SHA256_CTX      ctx;

    if ( (hash = malloc(SHA256_DIGEST_LENGTH)) == NULL ) {
        reporterror("Error occurred while allocating memory for the hash.", false, true);
    }
    if ( (digest = malloc(SHA256_DIGEST_LENGTH * 2 + 1)) == NULL ) {
        reporterror("Error occurred while allocating memory for the hex digest.", false, true);
    }
    // Calculate the hash.
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, string, strlen(string));
    SHA256_Final(hash, &ctx);
    // Convert the hash bytes into a hex digest string.
    for ( int i = 0; i < SHA256_DIGEST_LENGTH; ++i ) {
        sprintf(digest + (i * 2), "%02x", hash[i]);
    }
    digest[SHA256_DIGEST_LENGTH * 2] = '\0';
    free(hash);
    return digest;
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
           "  FILE          The encrypted .7z file archive (as created by ppk) to be\n"
           "                verified and unpacked into the pip repository.\n"
           "\n"
           "Optional arguments:\n"
           "  -h, --help    Display this help and exit.\n"
           "\n"
           "Example: To verify and unpack a .7z file archive:\n"
           "  $ %s /path/to/things/library-0.0.7-cp311-cp311-manylinux2014_x86_64.7z\n"
           "\n",
           _APP_NAME
    );
    if ( notice ) print_notice();
    if ( exit_zero ) exit(0);
}

