/**
    Header file for the config.c module.
*/

#ifndef _CONFIG_H
#define _CONFIG_H

/**
    Struct containing the config elements.

    These are set by the configload() function.
*/
typedef struct Config_ {
    char *dir_pip_repo;
    char *dir_ppk_tmp;
} Config;

/**
    Expose as external (global); *defined* in the config module.
    Can now be accessed by any module which #include(s) this header.
*/
extern Config *cfg;

/**
    Load the config file into a project's config struct.

    Note:
        The caller is responsible for freeing all character arrays and the
        struct itself.

        This can be done simply, by calling configfree(), as it has access
        to the global config struct.

    @param path Full path to the config file.
    @return Returns 0 for a successful config load. Otherwise, -1 for a
            failed file read, -2 for a failed file parse and -3 for all
            failed table loads, and -4 for failed memory allocation.
            All failures are accompanied by a relevant message.
*/
int
configload(const char *path);

/**
    Free the config's character arrays and the config struct.

    @return Void
*/
void
configfree(void);

#endif /* _CONFIG_H */

