"""
Some functions and utilities for package management using Python code rather than interactive shell scripts.
These functions can be run any any Python environment, and do not require using '!' or '%' and a Jupyter notebook to install some packages you want.

Author: Pouya Niaz, pniaz20@ku.edu.tr
"""

import subprocess


def getpkg(lister:str='pip'):
    """
    Get the installed packages in the current Python environment using 'pip list' or 'conda list'.
    
    Argument `lister` is a string, default 'pip', for 'pip list'. 'conda' would execute 'conda list'.
    """
    process = subprocess.run(f"{lister} list", stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
        universal_newlines=True, shell=True)
    stdout_raw = process.stdout.strip().upper()
    stderr_raw = process.stderr
    if len(stderr_raw) > 0:
        print(stderr_raw)
        return None
    return stdout_raw



def get_package_list(lister:str='pip'):
    """Get a list of all packages, as an output of 'pip list' or 'conda list'
    Args:
        :param `lister` (str, optional): The lister used. Options are 'pip' for 'pip list' or 'conda' for 'conda list'. Defaults to 'pip'.

    Returns:
        dict: Dictionary containing keys as upper-case package names and values as upper-case version strings
    """
    idx0 = 2 if lister=='pip' else 3
    string_raw = getpkg()
    packages_dict = {}
    for line in string_raw.split("\n")[idx0:]:
        (pname, pvers) = line.split()[:2]
        packages_dict[pname]=pvers
    return packages_dict



def check_packages(pkglst:list, lister:str='pip', install_missing:bool=True, reinstall_wrong_versions:bool=True, overwrite_install_command:str=None):
    """Test to see if the Python environment includes certain packages. Optionally, install missing packages or packages with the wrong version.

    ### Args:
        :param `pkglst` (list-like): list of packages, in string format. Example: ['numpy','scipy','matplotlib','python==3.8.12']
        :param `lister` (str, optional): The lister used. Options are 'pip', for 'pip list', or 'conda', for 'conda list'. Defaults to 'pip'.
        :param `install_missing` (bool, optional): Install missing packages. Defaults to True.
        :param `reinstall_wrong_versions` (bool, optional): Reinstall packages that have wrong versions installed.
        :param `overwrite_install_command` (str, optional): If specified, this command alone will be used for installling all packages.
                This command string will be used only if `install_missing=True` and there are missing packages, or if `install_wrong_versions=True` and there are packages
                with the wrong versions. In any case, if we decide to install some packages, we will use this overwrite string as one command to install any packages.
                Defaults to None, in which case we will use our own command to install any missing packages.
                Example: "pip install --force-reinstall numpy scipy matplotlib python==3.8.12"
    
        **NOTE** This function will use pip for installing everything by default. Also, even if one of the packages are missing and/or (optionally) installed with
        the wrong version, this program will use a single pip command which is `pip install --no-input --force-reinstall --no-cache-dir <everything-missing>`.
        If this is not desired behavior, or if you don't want to use pip at all, please specify the `overwrite_install_command` string to whatever you want.
        In this case, tha command only will be used for installing everything that is required or requested to be installed.
    
    ### Throws
    
    - `RuntimeError` if the command that tried to install the packages could not be executed.
    - `ModuleNotFoundError` if any of the packages were missing or installed with the wrong version, and `install_missing` were `False`.
    """
    packages_list = get_package_list(lister)
    notfound = []
    wrongver = []
    for pkg in pkglst:
        if '=' in pkg:
            pkg_name = pkg.split("=")[0]
            pkg_vers = pkg.split("=")[-1]
        else:
            pkg_name = pkg
            pkg_vers = None
        if pkg_name.upper() not in packages_list:
            print("Package {} not found.".format(pkg_name))
            notfound.append(pkg)
        elif pkg_vers is not None and packages_list[pkg_name.upper()] != pkg_vers:
            exist_vers = packages_list[pkg_name.upper()]
            print(f"Package {pkg_name} is found with version {exist_vers} but requested with version {pkg_vers}.")
            wrongver.append(pkg)
    print("----------------")
    if len(notfound)==0 and len(wrongver)==0:
        print("All packages are installed.")
    elif overwrite_install_command:
        print("Installing packages as follows: ")
        print(overwrite_install_command)
        command = overwrite_install_command
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            universal_newlines=True, shell=True)
        stdout_raw = process.stdout.strip()
        stderr_raw = process.stderr.strip()
        if len(stderr_raw) > 0:
            print(stderr_raw)
            raise RuntimeError("ERROR: Could not execute shell command '{}'".format(command))
    else:
        if (len(notfound) > 0 and install_missing) or (len(wrongver) > 0 and reinstall_wrong_versions):    
            print("Installing requested packages as follows: ")            
            command = "pip install --no-input --force-reinstall --no-cache-dir "+" ".join((notfound+wrongver) if (reinstall_wrong_versions and len(wrongver) > 0) else notfound)
            print(command)
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                universal_newlines=True, shell=True)
            stdout_raw = process.stdout.strip()
            stderr_raw = process.stderr.strip()
            if len(stderr_raw) > 0:
                print(stderr_raw)
                raise RuntimeError("ERROR: Could not execute shell command '{}'".format(command))
        else:
            raise ModuleNotFoundError("Some necessary packages are not installed.")    