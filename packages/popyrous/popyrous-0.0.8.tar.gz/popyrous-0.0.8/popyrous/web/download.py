
import io, json, requests, gdown
import pandas as pd
import numpy as np

def parse_string(string=None, filename=None, dtype='string', delimiter=',', header=None):
    """
    Process a string for meaningful numerical output.

    ### Params

    - `string` (str, optional): The string to be processed. If it is None, will look for a file to read
    - `filename` (str, optional): The path to the file to read to extract data, if the string is unavailable.
    - `dtype` (str, optional): type of output returned by the function, depending on the data downloaded. options are:
        - 'string': The string will be returned without change, or will be extracted from the file.
        - 'stringlist': Output will be a list of items, using the delimiter argument for separating content
        - 'numlist': Output will be a list of numbers, using the delimiter argument for separating content
        - 'numpy': Output will be a numpy array. New line will be used for separating rows
        - 'json': Output will be a json object, parsed directly from the string.
        - 'text': Output will be in text format, using only the new line character as the delimiter.
        - 'csv': Output will be treated like a csv file, returned by a pandas dataframe; delimiter will be used as provided.
    - `delimiter` (str, optional): delimiting character, if data includes list/array. Default is ','
    - `header` (num, optional): The 'header' input of the pandas.read_csv function. Default is None; This input is only useful if dtype=='csv'
                                        
    ### Returns

    An object of the type specified

    ### Example 
    
        ```python
        
        s_numpy = "[[1,2,3,4],\n[5,6,7,8]]"
        data_numpy = parse_string(s_numpy, dtype="numpy", delimiter=",")
        din = {"name":"Pouya", "sex":"M", "age":26, "isMarried":False, "work_experience":None, 
            "unis":["tabrizu.ac.ir","ku.edu.tr"]}
        s_json = json.dumps(din, indent=4)
        data_json = parse_string(s_json, dtype="json")
        s_numlist = "[1,2,3,4,5,6]"
        data_numlist = parse_string(s_numlist, dtype="numlist")
        
        ```

    """
    
    if string is None:
        if filename is None:
            raise ValueError("filename parameter cannot be empty when no string is supplied as the first argument.")
        with open(filename, 'r') as f:
            s = f.read()
    else:
        s = string
        
    if dtype == 'string':
        return s
    elif dtype == 'json':
        return json.loads(s)
    elif dtype == 'text':
        return s.strip().split('\n')
    else:
        s = s.replace('[','').replace(']','')
        if dtype == 'stringlist':
            return s.strip().split(delimiter)
        elif dtype == 'numlist':
            return [float(str_) for str_ in s.strip().split(delimiter)]
        elif dtype == 'numpy':
            return np.fromstring(s, sep=delimiter)
        elif dtype == 'csv':
            df = pd.read_csv(io.StringIO(s), sep=delimiter, header=header)
            return df
        else:
            raise ValueError("The specified dtype argument is not supported.")





# Function for downloading a file at a shareable link. Note that the link should be available to "anyone with the link".
def download_google_drive_file(shareable_link, output_file):
    """Download file from Google drive, provided that the link is available for "anyone with the link" in the permissions.

    Args:
        :param shareable_link (str): Shareable link of the file, gotten directly form Google drive.
        :param output_file (str): Path to the file to which the contents of the file will be downloaded, including any extension
    """
    fid = shareable_link[32:-17]
    url = 'https://drive.google.com/uc?id=' + fid
    gdown.download(url, output_file, quiet=False)





def download(url, filename=None, dtype='binary', delimiter=',', header=None):
    """
    Download contents from the internet, then use or store it in a file. The function automatically detects whether or 
    not the url is the shareable link of a google drive file, in which case it automatically downlaods the contents 
    of the Google Drive file.
    
    ### Inputs:
    
        :param `url` (str): url from which to download
        :param `filename` (str, optional): path to file in which the contents will be written. Default is None. No file will be written.
        :param `dtype` (str, optional): type of output returned by the function, depending on the data downloaded. options are:
        
        - 'binary' [default]: originally returned by the requests module, it is only binary data
        - 'string': The binary output will be decoded using UTF-8 into a string
        - 'stringlist': Output will be a list of items, using the delimiter argument for separating content
        - 'numlist': Output will be a list of numbers, using the delimiter argument for separating content
        - 'numpy': Output will be a numpy array. New line will be used for separating rows
        - 'json': Output will be a json object, parsed directly from the string.
        - 'text': Output will be in text format, using only the new line character as the delimiter.
        - 'csv': Output will be treated like a csv file, returned by a pandas dataframe;
            delimiter will be used as provided.
        - None: The function will not return anything.
        
        :param `delimiter` (str, optional): delimiting character, if data includes list/array. Default is ','
        :param `header` (num, optional): The 'header' input of the pandas.read_csv function. Default is None; This input is only useful if dtype=='csv'
        
    ### Returns:
    
        :return object of specified dtype, or nothing, if dtype=='none'
    
    ### Example:
    
    ```python
    
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    data_csv = download(url, filename="iris.csv", dtype="csv", delimiter=',', header=None)
    data_binary = download(url, dtype="binary")
    data_string = download(url, dtype="string")
    data_text = download(url, dtype="text")
    data_stringlist = download(url, dtype="stringlist")
    # Trying with a Google Drive shareable link
    url2 = 'https://drive.google.com/file/d/15V3R3cleRwfQbO9TAoy0R0KpxAWzDUZc/view?usp=sharing'
    data_csv_gdrive = download(url2, filename='iris_1.csv', dtype='csv')
    
    ```
    
    """
    
    if "drive.google.com" in url:
        googledrive = True
        if filename is None:
            raise ValueError("Filename parameter cannot be None if the link is a Google drive link.")
        fid = url[32:-17]
        link = 'https://drive.google.com/uc?id=' + fid
        gdown.download(link, filename, quiet=False)
        with open(filename, "r") as f:
            s = f.read()
    else:
        googledrive = False
        r = requests.get(url, allow_redirects=True)
        s = r.content.decode('UTF-8')
        if filename is not None:
            with open(filename, 'wb') as f:
                f.write(r.content)
    
    if dtype is None:
        pass
    elif dtype == 'binary':
        if googledrive:
            print("WARNING: Binary output unavailable with Google drive links. Nothing was returned by download().")
        else:
            return r.content
    else:
        return parse_string(s, dtype=dtype, delimiter=delimiter, header=header)
            
            
            
            
            
if __name__ == '__main__':
    
    # Now we will try this out
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    data_csv = download(url, filename="iris.csv", dtype="csv", delimiter=',', header=None)
    data_binary = download(url, dtype="binary")
    data_string = download(url, dtype="string")
    data_text = download(url, dtype="text")
    data_stringlist = download(url, dtype="stringlist")
    s_numpy = "[[1,2,3,4],\n[5,6,7,8]]"
    data_numpy = parse_string(s_numpy, dtype="numpy", delimiter=",")
    din = {"name":"Pouya", "sex":"M", "age":26, "isMarried":False, "work_experience":None, "unis":["tabrizu.ac.ir","ku.edu.tr"]}
    s_json = json.dumps(din, indent=4)
    data_json = parse_string(s_json, dtype="json")
    s_numlist = "[1,2,3,4,5,6]"
    data_numlist = parse_string(s_numlist, dtype="numlist")
    # Trying with a Google Drive shareable link
    url2 = 'https://drive.google.com/file/d/15V3R3cleRwfQbO9TAoy0R0KpxAWzDUZc/view?usp=sharing'
    data_csv_gdrive = download(url2, filename='iris_1.csv', dtype='csv')


