/**
    Purpose:    This module provides file system based functionality to
                to the unpacker program.
    
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

#include <dirent.h>
#include <errno.h>
#include <libgen.h>
#include <sys/stat.h>
#include <unistd.h>
#include "base.h"
#include "ui.h"
#include "utils.h"

/**
    Copy a single file from the source directory to the destination.

    Note: The destination directory *must* exist, otherwise file creation
          process the write will fail, and the function will return an 
          error code.

    @param[in]  src     Pointer to a string containing the full path of
                        the source file to be copied.
    @param[in]  dst     Pointer to a string containing the full path of
                        the destination of the copied file.

    @return             0 if the copy completes successfully, otherwise 1.
*/
int copyfile(const char *src, const char *dst) {

    int     sz = 1024*1024;  // 1 Mb
    char    buff[sz];
    char    msgbuff[256];
    size_t  bytes;
    FILE    *fpi, *fpo;

    if ( (fpi = fopen(src, "rb")) == NULL ) {
        // Note: The basename function expects 'char *', so casting as such to drop the 'const' 
        //       qualifier.
        sprintf(msgbuff, "An error occured while reading source file: %s", basename((char *)src));
        reporterror(msgbuff, false, false);
        return EXIT_FAILURE;
    }
    if ( (fpo = fopen(dst, "wb")) == NULL ) {
        sprintf(msgbuff, 
                "An error occured creating the destination file: %s\n"
                "\t - %s", dst, strerror(errno));
        reporterror(msgbuff, false, false);
        return EXIT_FAILURE;
    }
    while ( (bytes = fread(buff, sizeof(char), sz, fpi)) != 0 ) {
        if ( (fwrite(buff, sizeof(char), bytes, fpo)) != bytes ) {
            // Note: The basename function expects 'char *', so casting as such to drop the 'const' 
            //       qualifier.
            sprintf(msgbuff, "An error occurred while copying: %s -> %s", basename((char *)src), dst);
            reporterror(msgbuff, false, false);
            return EXIT_FAILURE;
        }
    }
    fclose(fpi);
    fclose(fpo);
    return EXIT_SUCCESS;
}

/**
    Search a directory for a given pattern.

    This function returns the path to the *first* file matching the given
    ipattern.

    @param[in]  dpath   Explicit path to the directory to be searched.
    @param[in]  pattern A string pattern to search.
                        If the pattern begins with a '.', this is 
                        interpreted as an *extension* search. Otherwise.
                        the string is searched using the strstr() function
                        with the *first* hit being returned.

    @return             If found, the full path to the *first* match is
                        returned.

    Example:

        char *file;

        file = findfile("/path/to/directory", ".log");
        free(file);

    Reminder: The memory allocated by this function **must be freed** by 
              the caller.

*/
char *findfile(const char *dpath, const char *pattern) {

    bool    found = false;
    char    *ext;
    char    *outpath = (char *)calloc(sizeof(char), PATH_MAX + 1);
    int     use_ext = ( pattern[0] == '.' );
    struct  dirent *ep;
    DIR     *dp;
    
    if ( (dp = opendir(dpath)) == NULL ) {
        reporterror("The provided directory does not exist", false, false);
        return NULL;
    }
    while ( (ep = readdir(dp)) ) {
        if ( ep->d_type == DT_REG ) {
            if ( use_ext ) {
                if ( (ext = strrchr(ep->d_name, '.')) && !(strcmp(ext, pattern)) ) {
                    found = true;
                    break;
                } 
            } else {
                if ( strstr(ep->d_name, pattern) ) {
                    found = true;
                    break;
                }
            }
        }
    }
    closedir(dp);
    // Build complete file path for return.
    if ( found )
        sprintf(outpath, "%s/%s", dpath, ep->d_name);
    return outpath;
}

/**
    Create a directory. 

    Note: All parent directories must apready exist.

    @param[in]  dpath   Path to the directory, for which the right-most 
                        child will be created.
    @param[in]  mode    Permissions mode assigned to the directory.
    @param[in]  verbose Pass true to display error messages relating
                        to the directory creation, error messages will be 
                        suppressed.

    @return             The exit code from the mkdir function. 
*/
int makedir(const char *dpath, mode_t mode, bool verbose) {

    int excode;

    if ( ((excode = mkdir(dpath, mode)) != 0) && (verbose) ) {
        reporterror(strerror(errno), false, false);
    }
    return excode;
}

/**
    Move *all* files from the source directory to the destination.

    First, the move attempts to use rename(2). If this fails for 
    EXDEV (18) (cannot move across file systems) a copy and delete are 
    attempted.

    Note: If either directory does not exist, the function will exit in 
          error.

    @param[in] src      Pointer to a string containing the full path to
                        the source directory.
    @param[in] dst      Pointer to a string containing the full path to 
                        the destination directory.
    @param[in] verbose  If true, a 'Moving src -> dst' message is 
                        displayed to the terminal.

    @return             - 0 if the number of files moved equals the number
                          of files found in the directory.
                        - -1 if the number of encountered files is not 
                          equal to the number of files moved.
                        - -2 if opening either directory fails.
*/
int moveall(const char *src, const char *dst, bool verbose) {

    char    fnbuff_src[PATH_MAX];
    char    fnbuff_dst[PATH_MAX];
    char    msgbuff[PATH_MAX + 256];
    int     count_act = 0;  // Actual count of files encountered.
    int     count_mov = 0;  // Count of files successfully moved.
    struct  dirent *ep;
    DIR     *dp;

    if ( (dp = opendir(dst)) == NULL ) {
        sprintf(msgbuff, "%s: %s", strerror(errno), dst);
        reporterror(msgbuff, false, false);
        return -2;
    } else {
        closedir(dp);
    }
    if ( (dp = opendir(src)) == NULL ) {
        reporterror("The provided source directory does not exist.", false, false);
        return -2;
    }
    print_start("\nMoving files to the pip repo ...");
    while ( (ep = readdir(dp)) ) {
        if ( ep->d_type == DT_REG ) {
            ++count_act;
            sprintf(fnbuff_src, "%s/%s", src, ep->d_name);
            sprintf(fnbuff_dst, "%s/%s", dst, ep->d_name);
            if ( verbose ) printf("Moving: %s -> %s\n", fnbuff_src, fnbuff_dst);
            if ( rename(fnbuff_src, fnbuff_dst) ) {
                /* rename(2) does not work across file systems, EXDEV (18) is thrown.
                   In this case, perform a copy / unlink to 'move' the file. */
                if ( errno == 18 ) {
                    if ( !copyfile(fnbuff_src, fnbuff_dst) ) {
                        // Delete the file to simulate a move.
                        unlink(fnbuff_src);
                        ++count_mov;
                    }
                } else {
                    sprintf(msgbuff, "An error occurred while moving: %s to %s", fnbuff_src, dst);
                    reporterror(msgbuff, false, false);
                }
            } else {
                ++count_mov;
            }
        }
    }
    closedir(dp);
    if ( count_act != count_mov ) {
        return -1;
    }
    print_done(false);
    return EXIT_SUCCESS;
}

/**
    Remove all files under the given path, including subdirectories.

    @param[in]  fpath   Pointer to a string containing the explicit path
                        to be removed.
    @param[in]  rmvdir  Remove the directory once empty.
    @param[in]  verbose Display the filenames are they are deleted.

    @return             Number of files successfully removed, or -1 if 
                        the function ended in error.
*/
int removeall(const char *dpath, bool rmvdir, bool verbose) {
    
    char    msgbuff[PATH_MAX + 256];
    char    fpath[PATH_MAX+1];
    int     i = 0;
    struct  dirent *ep;
    DIR     *dp;

    if ( (dp = opendir(dpath)) == NULL ) {
        reporterror("Error opening directory, does not exist.", false, false);
        return -1;
    }
    while ( (ep = readdir(dp)) ) {
        sprintf(fpath, "%s/%s", dpath, ep->d_name);
        if ( ep->d_type == DT_REG ) {
            if ( verbose ) printf("  - Deleting: %s\n", ep->d_name);
            if ( remove(fpath) ) {
                sprintf(msgbuff, "Error occurred while removing: %s", fpath);
                reporterror(msgbuff, false, false);
            } else {
                ++i;
            }
        } else if ( (ep->d_type == DT_DIR) && ( (strcmp(ep->d_name, ".")) && (strcmp(ep->d_name, "..")) ) ) {
            // A sub-directory was found. Remove it.
            i += removeall(fpath, 1, 0);
        }
    }
    closedir(dp);
    if ( rmvdir ) rmdir(dpath);
    return i;
}

/**
    Unzip the archive file pointed to by fpath, into the directory pointed
    to by opath.

    If the o(ut)path directory does not exist, its right-most directory is
    created. However, all parent directories must already exist.

    Note: If the same filename already exists in the extraction location,
          **it will be overwritten**.

    @param[in]  fpath   Explicit file path to the .7z file to be tested 
                        and unpacked.
    @param[in]  opath   Output directory into which the archive is 
                        unpacked.

    @return             0 if the archive is tested and unpacked 
                        successfully, otherwise 1.
*/
int unzip(const char *fpath, const char *opath) {

    char cmd_ext[256];
    char cmd_tst[256];
    char *hash = sha256_digest(basename((char *)fpath));

    sprintf(cmd_tst, "7z t %s -p%s > /dev/null", fpath, hash);
    sprintf(cmd_ext, "7z e %s -p%s -y -o%s > /dev/null", fpath, hash, opath);
    print_start("Preparing the archive for verification ...");
    if ( (system(cmd_tst) == 0) ) {
        makedir(opath, 0700, 0);
        //print_start("Unpacking the archive for verification ...");
        if ( (system(cmd_ext)) == 0 ) {
            //print_ok("Archive unpacked successfully.");
        } else {
            reporterror("An error occurred while unpacking the .7z file.", false, true);
        }
    } else {
        reporterror("The archive test has failed.", false, true);
    }
    print_done(0);
    free(hash);
    return EXIT_SUCCESS;
}

