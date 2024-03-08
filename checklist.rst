=================
Release Checklist
=================

#. Verify the version number has been updated.
    - _version.py
    - base.h

#. Run test cases (if applicable) on a new branch.

#. Run pylintr on a new branch.
   - **Reminder:** Remove the `./dist` `./build` and `./<pkg>.egg-info` 
     directories first.

#. Rebase and add final commit message.

#. Update documentation (if applicable) on a new branch and rebase.

#. Tag the commit.

#. Push to the remote master.

