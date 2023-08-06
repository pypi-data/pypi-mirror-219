import zipfile, warnings


try:
    import lzma
except Exception as e:
    warnings.warn("Cannot import lzma. Therefore, working with LZMA while compressing/decompressing zip files will not be possible.", UserWarning)
    print(e)



def extract_files(fileName):
    """Parse and extract ZIP file in the given path.
    :param fileName: path to the ZIP file, including the extension.
    :return list of files within the archive.
    """
    print("Parsing {} ...".format(fileName))
    with zipfile.ZipFile(fileName, mode='r') as zipobj:
        fl = zipobj.namelist()
        print("List of files in {} is:".format(fileName))
        for f in fl: print(f)
        print("Extracting {} ...".format(fileName))
        zipobj.extractall()
    return fl



def compress_files(file_name, file_list, compression=zipfile.ZIP_LZMA, compresslevel=9):
    """Compress list of given files into an archive

    
    :param file_name (str): Name of the archive file, with extension
    :param file_list (list): List of paths to files that will be compressed into the archive
    :param compression (int, optional): Compression type. Defaults to zipfile.ZIP_LZMA.
    :param compresslevel (int, optional): Compression level, between 1 and 9. Defaults to 9;
           Only applicable for zipfile.ZIP_DEFLATED and zipfile.ZIP_BZIP2 compression types.
    """

    print("Adding given files to archive {}...".format(file_name))
    with zipfile.ZipFile(file_name, mode='a', compression=compression, compresslevel=compresslevel, allowZip64=True) as zipobj:
        for f in file_list:
            try:
                zipobj.write(f)
            except:
                print("WARNING: File {} could not be added to the archive.".format(f))
    print("Done.")
