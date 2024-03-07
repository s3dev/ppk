/**
    Header file for the ui.c module.
*/

#ifndef _UI_H
#define _UI_H

/**
    Display an alert message (msg) in red.

    @param[in]  msg     Message to be displayed.
*/
void print_alert(const char *msg);

/**
    Display a 'Done.' message in green.

    @param[in]  add_newline     Insert a blank line above the message.
*/
void print_done(bool add_newline);

/** 
    Print the copyright notice. 
*/
void print_notice(void);

/**
    Display an OK (msg) in green.

    @param[in]  msg     Message to be displayed.
*/
void print_ok(const char *msg);

/**
    Display a start-of-procesing message (msg) in cyan.

    @param[in]  msg     Message to be displayed.
*/
void print_start(const char *msg);

/**
    Display a warning message (msg) in yellow.

    @param[in]  msg     Message to be displayed.
*/
void print_warning(const char *msg);

#endif /* _UI_H */

