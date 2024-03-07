# ppk - Python Package Check

A Python library download and vulnerability-check tool used to help safely transfer libraries to secured environments.

## What Is it?
The `ppk` utility is, at its very core, a wrapper around the `pip download`command - with added security checking functionality.

Using the supplied arguments, a Python library (and its dependencies) are downloaded from [PyPI](https://pypi.org/) using a subprocess call to `pip download`. Once the download has completed, a series of vulnerability checks are conducted on *each* downloaded file to help ensure the code contained within is not reported to be malicious.

The following vulnerability tests are conducted on *each* downloaded file:
 - **MD5 checksum:** The hash of the downloaded file is compared with the hash for the same file, as stored by PyPI.
 - **Security vulnerabilities:** The [Snyk security database](https://security.snyk.io/) is searched to determine if any vulnerabilities have been discovered and reported in the specific library.

If all security checks pass, a `.zip` file archive is created on your desktop containing the downloaded libraries. 

Finally, the `ppk` utility is used to unpack this archive into the cluster's secured local pip repository; where they can be installed using a standard `pip install <package-name>` command from the terminal.

## Getting Started
This section provides a quick-start guide to getting up and running.

The `ppk` utility is deployed on the AI cluster in `/mnt/core/usr/local/bin`, and can be accessed at any time by simply typing `ppk` into the terminal.

For example, the help menu can be displayed at any point by providing the `--help` argument:

``` bash
$ ppk --help
``` 

### Downloading `ppk`
There are times when you'll need to run `ppk` from your local (internet attached) PC. To obtain a copy of the utility, `ppk` can be [download](http://rrai01git01:3000/Insight/ppk/archive/master.tar.gz) from the cluster's local Gogs repository.

Download and extract the archive to a location of your choice.

**Note:** The commands shown in the examples throughout this documentation demonstrate use *from the cluster*. When running from your local PC, the commands look look like:

``` bash
$ cd /path/to/ppk
$ python3 ppk.py <argument>
```


## Using `ppk` to download from PyPI
The following headings demonstrate how `ppk` can be used to download a Python library from PyPI.

**Notes:** All of the following examples:
- should be run on an PC *with internet access*
- assume the directory path to `ppk` is in `$PATH` and, `ppk` is a symlink to the location of `ppk.py`; as this is the setup on the cluster  

#### Simplest
The following example demonstrates a simplified use of the utility to download the `pandas` library:

``` bash
# Download pandas
$ ppk pandas 
```

#### Specifying the library version
The following example demonstrates how a *specific version* of the `pandas` library can be downloaded:

``` bash
# Download pandas version 2.0.1
$ ppk pandas==2.0.1
```
If the library version is not specified, the download will default to the latest version available.

#### Specifying the Python version
The following example demonstrates how a specific version of the `pandas` library can be downloaded, for a *specific version of Python*; in this case Python 3.11:

``` bash
# Download pandas version 2.0.1 for Python 3.11
$ ppk pandas==2.0.1 --python_version 311
```
If the Python version is not specified, the download will default to the Python version of the current interpreter.

#### Specifying the platform
There are times when a platform (or system architecture) will need to be supplied. For example, you are working on an amd64 architecture, but need a library compiled for a Linux aarch64 architecture - however the aarch64 PC is not connected to the internet.

The following example demonstrates how a specific version of the `pandas` library can be downloaded, for a specific version of Python; in this case Python 3.11 - and compiled for an aarch64 architecture:

``` bash
# Download pandas version 2.0.1 for Python 3.11, and an aarch64 CPU architecture
$ ppk pandas==2.0.1 --python_version 311 --platform manylinux2014_aarch64
```
If the platform is not specified, the download will default to the platform of the current interpreter.

#### Using a `requirements.txt` file
When needing to download several Python libraries (and their dependencies) at once, a `requirements.txt` file can be used. Within this file are specified the target libraries (and their version) to be downloaded.

For example, a sample file may look like:

```bash
numpy==1.26.1
pandas==2.0.1
python-dateutil==2.8.2
pytz==2023.3.post1
six==1.16.0
tzdata==2023.3
``` 
The following example demonstrates how to pass a `requirements.txt` file to `ppk`:

``` bash
# Download all libraries (and dependencies) in the specified file
$ ppk /path/to/requirements.txt
```

## Transferring a Downloaded Archive to the Cluster
Once the Python libraries have been downloaded and tested, they are archived into a `.zip` file on your local desktop. However, if the security checks fail, an archive is *not* created. The `ppk` utility is then used to *transfer* the downloaded libraries onto the cluster's secured local pip repository.

### Verify and Transfer an Archive
To verify and transfer a *clean* archive, simply pass the `.zip` file into `ppk`. For example, to transfer an archive (created by the commands above) for `pandas` 2.0.1, from an archive on your desktop to the cluster's local pip repository:

``` bash
$ ppk ~/Desktop/pandas-2.0.1-cp311-cp311-manylinux2014_x86_64.zip
```
