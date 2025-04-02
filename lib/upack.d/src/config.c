/**
    Config file reader implementation.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/config.h"
#include "../include/toml.h"
#include "../include/utils.h"

/*
    Expose as global for the project.

    The declaration is in this module to make porting the config.c/h files
    across projects easier and more contained.
*/
Config *cfg;

/* Prototypes */
static int _init(void);

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
configload(const char *path) {

    toml_table_t *config;
    toml_table_t *tbl_paths;
    toml_datum_t dir_pip_repo;
    toml_datum_t dir_ppk_tmp;
    FILE *fp;

    // Setup config struct.
    if ( _init() ) {
        return -1;
    }
    // Read, parse and extract.
    if ( !(fp = fopen(path, "r")) ) {
        perror("\nError reading the config file");
        fprintf(stderr, "-- Search path: %s\n", path);
        return -2;
    }
    if ( !(config = toml_parse_file(fp, NULL, 0)) ) {
        reporterror("Error parsing the config file.", 0, 0);
        fclose(fp);
        return -3;
    }
    if ( !(tbl_paths = toml_table_in(config, "paths")) ) {
        reporterror("Error extracting the table: paths", 0, 0);
        fclose(fp);
        toml_free(config);
        return -4;
    }
    // Extract [path] values.
    dir_pip_repo = toml_string_in(tbl_paths, "dir_pip_repo");
    dir_ppk_tmp = toml_string_in(tbl_paths, "dir_ppk_tmp");
    // Test and store path values.
    if ( dir_pip_repo.ok ) {
        cfg->dir_pip_repo = malloc(strlen(dir_pip_repo.u.s) + 1);
        strcpy(cfg->dir_pip_repo, dir_pip_repo.u.s);
    }
    if ( dir_ppk_tmp.ok ) {
        cfg->dir_ppk_tmp = malloc(strlen(dir_ppk_tmp.u.s) + 1);
        strcpy(cfg->dir_ppk_tmp, dir_ppk_tmp.u.s);
    }
    // TOML can be free'd as the config is now in a struct.
    free(dir_pip_repo.u.s);
    free(dir_ppk_tmp.u.s);
    toml_free(config);
    fclose(fp);
    return EXIT_SUCCESS;
}

/**
    Free the config's character arrays and the config struct.

    @return Void
*/
void
configfree(void) {
    free(cfg->dir_pip_repo);
    free(cfg->dir_ppk_tmp);
    free(cfg);
}

/**
    Initialise the config struct.

    @return Returns 0 on success, otherwise non-zero.
*/
static int
_init(void) {
    // Setup config struct.
    if ( (cfg = malloc(sizeof(Config))) == NULL ) {
        perror("Error allocating memory for the config struct");
        return EXIT_FAILURE;
    }
    // Initialise config values.
    cfg->dir_pip_repo = calloc(1, 1);
    cfg->dir_ppk_tmp = calloc(1, 1);
    return EXIT_SUCCESS;
}

