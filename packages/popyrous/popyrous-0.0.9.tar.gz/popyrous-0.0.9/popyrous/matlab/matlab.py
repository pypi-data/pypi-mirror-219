import scipy.io as sio
import numpy as np

def type_compatible(typ):
    """

    Boolean determining if a data type is compatible for writing into .mat files.

    Parameters
    ----------
    typ : type
        Type object returned by type(.)

    Returns
    -------
    Boolean value of whether the type can directly be written into a .mat file.

    """
    x = typ.__name__
    return 'int' in x or 'float' in x or 'bool' in x or 'str' in x or 'numpy' in x or 'ndarray' in x


def save_workspace(filename='backup.mat', masterdict={}):
    """

    Save a given workspace dictionary into a .mat file.

    Parameters
    ----------
    filename : str, optional
        Path to the file including or not including the .mat extension. The default is 'backup.mat'.

    masterdict : dict, optional
        Dictionary of variables where the keys are strigns representing name of variable and values are values
        of variables. The default is {}. The global workspace in Python is always globals().

    Returns
    -------
    None.

    """
    savedict = {}
    for variable in masterdict:
        tp = type(masterdict[variable])
        if variable[0] == '_':
            continue
        if type_compatible(tp):
            savedict[variable] = masterdict[variable]
        elif 'list' in tp.__name__:
            if len([str(type(element)) for element in masterdict[variable]
                    if type_compatible(type(element))]) == \
                    len(masterdict[variable]):
                templist = masterdict[variable]
                varname = variable + '_array'
                temparray = np.empty((len(templist),), dtype=np.object)
                for i in range(len(templist)):
                    temparray[i] = templist[i]
                savedict[varname] = temparray
            else:
                continue
        else:
            continue
    sio.savemat(filename, savedict, long_field_names=True)


def load_workspace(filename, dictname=None):
    """

    Load variables from .mat file and store them in a dictionary

    Parameters
    ----------
    filename : str
        path to .mat file, with or without the .mat extension.

    dictname : dict, optional
        Dictionary in which to insert variables. The default is None.

    Returns
    -------
    dict
        Dictoinary in which variables of the .mat file will be inserted

    """
    return sio.loadmat(filename, mdict=dictname, appendmat=True)