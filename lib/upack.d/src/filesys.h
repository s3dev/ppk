/**
    Header file for the filesys.c module.
*/

#ifndef _FILESYS_H
#define _FILESYS_H

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
int copyfile(const char *src, const char *dst);

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
char *findfile(const char *dpath, const char *pattern);

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
int makedir(const char *dpath, mode_t mode, bool verbose);

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
int moveall(const char *src, const char *dst, bool verbose);

/**
    Remove all files under the given path, including subdirectories.

    @param[in]  fpath   Pointer to a string containing the explicit path
                        to be removed.
    @param[in]  rmvdir  Remove the directory once empty.
    @param[in]  verbose Display the filenames are they are deleted.

    @return             Number of files successfully removed, or -1 if 
                        the function ended in error.
*/
int removeall(const char *dpath, bool rmvdir, bool verbose);

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
int unzip(const char *fpath, const char *opath);

#endif /* _FILESYS_H */

