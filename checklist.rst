=================
Release Checklist
=================

#. Verify the version number has been updated.
    - _version.py
    - base.h

#. Run test cases (if applicable) on a new branch.

#. Run pylintr on a new branch.
   - **Reminder:** Remove the `./dist` `./build` and `./<pkg>.egg-info` directories first.

#. Switch the __DEV_MODE flag in base.h and re-compile.

#. Rebase and add final commit message.

#. Update documentation (if applicable) on a new branch.

#. Run `build.sh` on a new branch.

#. Rebase again.

#. Tag the commit.

#. Push to the remote master.

