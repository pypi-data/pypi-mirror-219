SEED = 42

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import warnings

if __name__ == "popyrous.timeseries.experiment":
    from . datasets import make_squeezed_dataset, make_unsqueezed_dataset
    from . filt import butter_lowpass_filter_forward
    from . recipe_577504_1 import total_size
else:
    from datasets import make_squeezed_dataset, make_unsqueezed_dataset
    from filt import butter_lowpass_filter_forward
    from recipe_577504_1 import total_size



class TimeseriesExperiment:
    def __init__(self, dataframe, hparams, subjects_column:str=None, conditions_column:str=None, trials_column:str=None, input_cols:list=None, output_cols:list=None,
        input_preprocessor=None, input_postprocessor=None, output_preprocessor=None, output_postprocessor=None,
        specific_subjects:list=None, specific_conditions:list=None, specific_trials:list=None, num_subjects_for_testing:int=None, subjects_for_testing:list=None, 
        num_conditions_for_testing:int=None, conditions_for_testing:list=None, num_trials_for_testing:int=None, trials_for_testing:list=None,
        use_filtered_data:bool=False, lpcutoff:float=None, lporder:int=None, lpsamplfreq:float=None, data_squeezed:bool=True, 
        return_data_arrays_orig:bool=True, return_data_arrays_processed:bool=True, return_train_val_test_data:bool=True, return_train_val_test_arrays:bool=True):
        """
        Generates a time-series experiment dataset out of a dataframe of time-series data with many subjects doing the expriments under
        many conditions, with many trials (repetitions).
        
        Comes in handy when trying to separate the subjects, conditions, and trials of some timeseries experiments,
        and processing them separately such as scaling them, including or excluding some of them from training or
        testing, and trying to generate training, validation, and testing sets out of those experiments.
        
        In many occasions, because input data to models will be sequence data, data for trials need to be analyzed and 
        scanned via a sliding window separately. On the other hand, a single preprocessed, scaled dataset is required for
        training. Sometimes, differnet subjects or conditions need to be kept for testing, and only some of them are
        desired to be used for training. This function is useful for all of those cases.
        
        As a bonus, this function is also capable of rearranging and returning the original data, that can later be used 
        for plotting time plots, etc. It is also capable of preprocessing or postprocessing any sequential data before 
        or after processing with a sliding window.

        ### Args:
        
            - `dataframe` (`pd.DataFrame`): DataFrame holding all the raw timeseries data, all subjects and conditions.
            - `hparams` (dict): Dictionary to be used for extracting useful hyperparameters for the sliding window.
            
            This dicitonary will be sent to, and returned by, the `make_squeezed_dataset` or `make_unsqueezed_dataset`
            function, depending on whether or not squeezed or unsqueezed data is desired (see below).
            
            This dictionary should contain the following keys:
            
            * `in_seq_len_sec` (float): Length of the input sequence, in seconds (or units of time).
            * `out_seq_len_sec` (float): Length of the output sequence, in seconds (or units of time).
            * `data_downsampling` (int): Downsampling factor, i.e. one out of how many samples will be extracted.
            * `sequence_downsampling` (int): Downsampling factor for the sequences, AFTER data downsampling and generating the sequences.
            * `data_sampling_rate_Hz` (float): Sampling rate of the data, in Hz (or counts per unit time).
            * `validation_data` (float|tuple, optional): Portion of the data to be used for validation while training.
                These datapoints will be selected randomly out of all the data. The data will be shuffled.
                If this is a tuple, it should hold the portion, followed by which set it comes from, 
                'trainset' or 'testset'. If it is a float, it will by default come from test set, if any.
                If there is no test set applicable according to the settings, training set will be used.
                If this is a tuple, it should be e.g. [0.2, 'trainset'] or [0.1,'testset'].
            
            
            ** Description of data downsampling and sequence downsampling **
            
            The data downsampling rate downsamples the data when extracting it, so dataset size (number of samples) is divided by the downsampling rate.
            After the time series is downsampled by the `data_downsampling`, sequences are extracted from it using a sliding window. After the sequences are extracted, they can 
            still have too many time steps in them especially if the sampling rate was high to begin with. Then, the `sequence_downsampling` is applied, and all the extracted 
            sequences are downsampled. This does not change the dataset size; it only decreases the number of time steps in each sequence.
            
            Data downsampling is typically used when the sampling frequency is too high and there are too many time series or the series are too long. Sequence downsampling is 
            typically used when the sequence length (in units of time) needs to remain large enough to extract meaningful trends and information, but because the sampling 
            frequency is too high the sequences end up having too many time steps. Sequence downsampling makes sure the time-length of the sequences remains constant while the 
            number of time steps in each sequence is reduced.
            
            For example, let us assume 100 trials of a time-series experiment were performed, each lasting 100 seconds, with a sampling frequency of 1000 Hz. This means there are 
            a total of 100 K timesteps in each trial, amounting to 10 M time steps (training samples) in total. Let us assume that the sequences that you extract with a sliding 
            window need to be at least 2 seconds long to be able to extract meaningful information from them. There are two problems here. Firstly, there are too many data points 
            (10 M) in the training set. Secondly, the sequences will have too many time steps in them (2000) which will make training difficult and memory-intensive. To solve this 
            problem, we apply a `data_downsampling` rate of 4, reducing the effective sampling frequency to 250 Hz. This reduces the number of data points to 2.5 M.
            Also, this will mean that our 2-second sequences will have 500 time steps in them. Right now, 2.5 M dataset size is good, and we do not want to reduce it further. 
            However, especially if the data is smooth enough, 500 time steps in a sequence may be still too high. If we increase the `data_downsampling` rate, dataset size will 
            also decrease, and we do not want that. Therefore, we simply apply a `sequence_downsampling` rate of 10, which will reduce the number of time steps in each sequence to
            50, without touching the dataset size, affecting the rate of extracting sequences from the time series, or affecting the time length of the extracted sequences. 
            Assuming that the data is smooth and 50 timesteps forming a 2-second sequence are enough to extract meaningful information from the data, this is a good solution. 
            We will eventually have 2.5 M sequences with 50 time steps in each.
            
            Therefore, if the size and/or sampling frequency of the data is too high, data downsampling is preferred.
            However, if the dataset size is fine, but due to the long sequence length or high sampling rate, sequences
            hold too many data points in them and matrices end up being too large for the memory, sequence downsampling 
            is preferred. Sequence downsampling will not touch the size/sampling frequency of the data itself, 
            nor will it touch the true time length of the sequences. It will only make the sequences downsampled 
            and more coarse. Therefore, number of data points in the dataset will remain constant, as will the true 
            time length of the sequences. However, the number of time steps in the sequences will decrease.
            
            **IMPORTANT** 
            
            Depending on whether squeezed or unsqueezed data is required (see below), the passed hyperparameter 
            dictionary will be updated as follows:
            
             - If `data_squeezed` is True: The `input_size` and `output_size` hyperparameters will be updated as well as `in_seq_len` and `out_seq_len`.
            This is useful when, e.g., the data will be sent to an ANN that uses 2D tensors as inputs.
            
             - If `data_squeezed` is False: The `in_seq_len` and `out_seq_len` hyperparameters will be updated.
            This is useful when RNN-based or CNN-based models will be deployed, where inputs are 3D. In this case, at the end, `out_features` key will also be updated and
            multiplied by the `out_seq_len` to get the final output layer width. Thsi is because this class assumes that regardless of input shapes, outputs are always
            squeezed to 2D tensors. Therefore,  the final output layer width will be `out_features *= out_seq_len`.
            
            ** NOTE ** that in the case of unsqueezed data, the 3D tensors coming from the sliding windows will be of shape 
            (batch size, sequence length, features/channels) which is OK with Keras, but not OK with PyTorch, for instance.
            
            The rest of the arguments of this class are as follows:
                
            - `subjects_column` (str, optional): Column of the DataFrame holding subject numbers, if any. Defaults to None.
            - `conditions_column` (str, optional): Column of the DataFrame holding condition numbers. Defaults to None.
            - `trials_column` (str, optional): Column of the DataFrame holding trial numbers, if any. Defaults to None.
            
                **NOTE**: If any of the above arguments are None, it is assumed only one subject/condition/trial is
                involved in the timeseries experiments.
                
                **NOTE** Subjects, Conditions and Trials MUST be 1-indexed integers as in 1, 2, 3, ... otherwise this function will misbehave.
                
            - `input_cols` (list, optional): List of columns of input data. Defaults to None, meaning all data is input.
            - `output_cols` (list, optional): List of columns of output data. Defaults to None, meaning there is no output.
            - `input_preprocessor` (function, optional): Function to perform before processing. Defaults to None.
            
                **Note** This function should take in a DataFrame extracted from a specific subject/condition/trial holding only `input_cols`,
                and return a numpy array containing preprocessed input data of that trial.
                
            - `input_postprocessor` (function, optional): Function to perform after processing. Defaults to None.
            
                **Note** This function should take a numpy array which represents the processed tabulated data after 
                sliding window etc., and return a new numpy array with the same number of rows, containing the 
                postprocessed data.
                
                **Note** Scaling of inputs and outputs can be done automatically (see below) and do not need to be
                manually employed as pre/postprocessing steps.
                
            - `output_preprocessor` (function, optional): Same as the one for inputs. Defaults to None.
            - `output_postprocessor` (function, optional): Same as the one for inputs. Defaults to None.
            - `specific_subjects` (list, optional): List of 1-indexed subject numbers to use. Defaults to None.
            - `specific_conditions` (list, optional): List of 1-indexed condition numbers to use. Defaults to None.
            
                **Note** If any of the above arguments are given, the cell array will be complete, but the corresponding
                elements of the cell arrays to the subjects/conditions not included in the list will be empty lists, [].
                These data will also not be used for generating training or testing data for a model.
                 
            - `num_subjects_for_testing` (int, optional): Self-explanatory. Defaults to None. If provided, subjects will be chosen randomly from all subjects.
            - `num_conditions_for_testing` (int, optional): Conditions for testing will be chosen randomly.
            - `num_trials_for_testing` (int, optional): Trials for testing will be chosen randomly.
            - `subjects_for_testing` (list, optional): Self-explanatory. Defaults to None. It is 1-indexed.
            
                **Note** If `num_subjects_for_testing` is given but `subjects_for_testing` is not given, the subjects
                for testing will be chosen randomly from all subjects. The same goes for conditions and trials.
                
            - `conditions_for_testing` (list, optional): List of 1-indexed condition numbers used for testing. Defaults to None.
            - `trials_for_testing` (list, optional): List of 1-indexed trial numbers used for testing out of every condition. Defaults to None.
            - `use_filtered_data` (bool, optional): Whether to low-pass filter data before processing. Defaults to False.
            
                **Note** If given, a digital Butterworth low-pass filter will be deployed, only forward-facing, that is,
                using `filt`, NOT `filtfilt`.
                
            - `lpcutoff` (float, optional): Lowpass filter cutoff frequency, Hz. Defaults to None.
            - `lporder` (int, optional): Lowpass filter order. Defaults to None.
            - `lpsamplfreq` (float, optional): Lowpass filter sampling frequency, Hz. Defaults to None.
            - `data_squeezed` (bool, optional): Whether the input data should be squeezed. Defaults to True.
            
                Squeezed data are 2D, as in (num_data, sequence_length*num_features), but unsqueezed data are 3D, as in (num_data, sequence_length, num_features).
                Squeezed data can, e.g., be used as inputs for MLP models, while unsqueezed data can be used as inputs for RNN/1D-CNN models.
            
            ** The input arguments below will apply when the `process_data` of this class is called, not before then. **
                
            - `return_data_arrays_orig` (bool, optional): Whether to return original data arrays. Defaults to True.
            - `return_data_arrays_processed` (bool, optional): Whether to return procecssed data arrays. Defaults to True.
            - `return_train_val_test_data`(bool, optional): Whether to return model training-related arrays and data. Defaults to True.
            
                If `True`, the function will return processed, scaled and shuffled numpy arrays ready to be plugged into
                a learning model. They will include training, validation and test sets, if applicable.
                
                If `False`, the function will not return such data. This can come in handy if no training or machine learning
                is involved in what you are trying to do, and you are trying to save memory.
                
            - `return_train_val_test_arrays` (bool, optional): Whether to return per-trial individual model training-related arrays. Defaults to True.
            
                If `True`, the function will return processed, scaled and shuffled numpy arrays ready to be plugged into
                the machine learning model. However, these arrays will be wrapped in a cell array, where each element of the 
                array corresponds to machine-learning-ready training, validation & testing data of one individual trial of the
                experimentation.
                
                
        ### Important Implementation Notes:
    
        - In the data, subject, condition and trial numbers must be 1-indexed. The code will misbehave otherwise.
        This is a bug that will be fixed in a future improved version.
        - When indexing cell arrays, however, after running `process_data()`, indexing is 0-indexed as in Python. This is also buggy behavior, and will be
        fixed in a future version. Data for subject 1, controller 1, trial 1, is accessed as, e.g. `self.data_arrays_orig[0,0,0]`.
        """
        self.dataframe = dataframe
        self.hparams = hparams
        self.subjects_column = subjects_column
        self.conditions_column=conditions_column
        self.trials_column=trials_column
        self.input_cols=input_cols
        self.output_cols=output_cols
        self.input_preprocessor=input_preprocessor
        self.input_postprocessor=input_postprocessor
        self.output_preprocessor=output_preprocessor
        self.output_postprocessor=output_postprocessor
        self.specific_subjects=specific_subjects
        self.specific_conditions=specific_conditions
        self.specific_trials=specific_trials
        self.num_subjects_for_testing=num_subjects_for_testing
        self.subjects_for_testing=subjects_for_testing
        self.num_conditions_for_testing=num_conditions_for_testing
        self.num_trials_for_testing=num_trials_for_testing
        self.conditions_for_testing=conditions_for_testing
        self.trials_for_testing=trials_for_testing
        self.use_filtered_data=use_filtered_data
        self.lpcutoff=lpcutoff
        self.lporder=lporder
        self.lpsamplfreq=lpsamplfreq
        self.data_squeezed=data_squeezed
        self.return_data_arrays_orig=return_data_arrays_orig
        self.return_data_arrays_processed=return_data_arrays_processed
        self.return_train_val_test_data=return_train_val_test_data
        self.return_train_val_test_arrays=return_train_val_test_arrays
        self.is_processed = False
        
        
    
    def process_data(self, verbosity:int=0, return_output:bool=False, **kwargs):
        """Process all trials of all conditions of all subjects in the experiment, with preprocessing, post-procesisng, etc.

        ### Args:
        
            `verbosity` (int, optional): Verbosity. Defaults to 0. 0 means nothing. 1 means general info. 2 means everything.
            `return_output` (bool, optional): Return the output dictionary or just update the instance attributes. Defaults to False.

        ### Returns:
        
            If `return_output=True`, returns a dictionary containing the following keys, otherwise instance attributes with the same names will be updated.
            Note that depending on constructor inputs such as `return_data_arrays_orig`, `return_data_arrays_processed`, `return_train_val_test_data`, and
            `return_train_val_test_arrays`, some of these keys/variables could be None, or empty lists.
            
            - `is_test` (numpy nested cell arrays): Whether every trial is for testing data or not.
            - `x_train`,`x_val`,`x_test`,`y_train`,`y_val`,`y_test` (numpy arrays): Training, validation and testing
                arrays of input and output data, respectively, processed, scaled and processed with sliding window, fully
                ready to be fed to a learning algorithm. The data is also shuffled.
                If `hparams["validatoin_data"]` does not exist, `x_val` and `y_val` will be None, or empty.
                If testing-related parameters like `num_subjects_for_testing` or `subjects_for_testing` are not given,
                The `x_test` and `y_test` will be None, or empty.
                If `return_train_val_test_data` is False, `x_train`, `x_val`, `x_test`, `y_train`, `y_val`, `y_test` will
                not be included in the output dictionary.
            - `x_arrays` and `y_arrays` (numpy nested cell arrays): These include the same data as `x_train`, `x_val`, etc.,
                only they are separated for subjects, conditions and trials. If `return_train_val_test_arrays` is False,
                these will be empty lists, [].
                `x_arrays[subj,cond,trial]` holds the corresponding data of one timeseries experiment, for instance.
            - `data_arrays_orig` and `data_arrays_processed` hold the data itself, nested and rearranged,
                but not passed through the sliding window. The `orig` one holds the raw data before preprocessing function,
                if any, and the `processed` one contains preprocessed and scaled data. These will be empty or None, if 
                `return_data_arrays_orig` or `return_data_arrays_processed` are False, respectively.
                
                **Note** One of the preprocessing steps that takes place by default, is downsampling. Therefore, the `orig`
                data will NOT even be downsampled.
                
                `data_arrays_orig[subj,cond,trial]` is a dictionary holding `input` and `output` keys, whose values are the
                original or processed timeseries data for the corresponding timeseries experiment, containing the
                inputs and outputs, respectively.
                
            - `hparams` (dictionary): Dictionary of hyperparameters used in this function, modified and updated.
                **Note** Returning this object is not actually necessary. The `hparam` parameter is already modified and 
                updated, because the function modifies the reference to the hparams object, so there is no real need
                for returning it, unless for back-up or storage reasons.
            
            - `subjects_test` (list): List of subject numbers actually used for testing.
            - `conditions_test` (list): List of condition numbers actually used for testing.
            - `trials_test` (list): List of trial numbers actually used for testing.
            - `num_subjects`, `num_conditions`, `num_trials` (int): Number of subjects, conditions and trials, respectively.
        """
        # Lists of arrays holding trial data, to concatenate later
        x_lst_lrn = []
        y_lst_lrn = []
        x_lst_tst = []
        y_lst_tst = []
        
        # Calculate number of subjects, conditions and trials
        self.num_subjects = len(self.dataframe[self.subjects_column].value_counts()) if self.subjects_column else 1
        self.num_conditions = len(self.dataframe[self.conditions_column].value_counts()) if self.conditions_column else 1
        self.num_trials = len(self.dataframe[self.trials_column].value_counts()) if self.trials_column else 1
        
        if verbosity > 0:
            print("Number of subjects:   ", self.num_subjects)
            print("Number of conditions: ", self.num_conditions)
            print("Number of trials:     ", self.num_trials)
            print("\n")
        

        # Cellular arrays holding data of each trial
        if verbosity == 2: print("Initializing data arrays ...")
        x_arrays = np.empty((self.num_subjects,self.num_conditions,self.num_trials), dtype=np.ndarray)
        y_arrays = np.empty((self.num_subjects,self.num_conditions,self.num_trials), dtype=np.ndarray) 
        data_arrays_orig = np.empty((self.num_subjects,self.num_conditions,self.num_trials), dtype=dict)   
        data_arrays_processed = np.empty((self.num_subjects,self.num_conditions,self.num_trials), dtype=dict) 
        is_test_arr = np.empty((self.num_subjects,self.num_conditions,self.num_trials), dtype=object)

        # Determining which trials will be used for training+validation, and which ones will be used for testing
        if verbosity == 2: print("Determining training/validation, and testing trials...")
        
        # Determining subjects used for testing
        if self.subjects_for_testing:
            subjects_test = self.subjects_for_testing
        elif self.num_subjects_for_testing:
            subjects_test = np.random.choice(np.arange(1,self.num_subjects+1), size=self.num_subjects_for_testing, replace=False)
        else:
            subjects_test = []
            
        # Determine conditions used for testing
        if self.conditions_for_testing:
            conds_test = self.conditions_for_testing
        elif self.num_conditions_for_testing:
            conds_test = np.random.choice(np.arange(1,self.num_conditions+1), size=self.num_conditions_for_testing, replace=False)
        else:
            conds_test = []
            
        # Determine trials used for testing
        if self.trials_for_testing:
            trials_test = self.trials_for_testing
        elif self.num_trials_for_testing:
            trials_test = np.random.choice(np.arange(1,self.num_trials+1), size=self.num_trials_for_testing, replace=False)
        else:
            trials_test = []
        
        # Log
        if verbosity > 0:
            print("subjects used for testing:   ", subjects_test)
            print("conditions used for testing: ", conds_test)
            print("trials used for testing:     ", trials_test)
            print("\n")
        
        ########################################################################
        # Iterate through each trial
        if verbosity > 0: print("Iterating through all trials ...\n")
        for subj in range(self.num_subjects):
            if verbosity == 2: print("  > Subject %d ... "%(subj+1), end="")
            is_test_subject = (subj+1 in subjects_test) if subjects_test else False
            if verbosity == 2: print("(testing)" if is_test_subject else "")
            for ctrl in range(self.num_conditions):
                if verbosity==2: print("    >> Condition %d ... "%(ctrl+1), end="")
                is_test_cond = (ctrl+1 in conds_test) if conds_test else False
                if verbosity == 2: print("(testing)" if is_test_cond else "")
                for trial in range(self.num_trials):
                    if verbosity == 2: print("      >>> Trial %d ... "%(trial+1), end="")
                    is_test_trial = (trial+1 in trials_test) if trials_test else False
                    
                    # Figure out if the trial is for training or testing
                    is_test = (is_test_subject or is_test_cond or is_test_trial)
                    if verbosity == 2: print("(testing) " if is_test else "(training) ", end="")
                    
                    # Figure out if the trial is one of the specific ones that we want (if it should be covered at all)
                    if self.specific_subjects is not None:
                        if subj+1 not in self.specific_subjects:
                            x_arrays[subj, ctrl, trial] = []
                            y_arrays[subj, ctrl, trial] = []
                            data_arrays_orig[subj, ctrl, trial] = {}
                            data_arrays_processed[subj, ctrl, trial] = {}
                            is_test_arr[subj, ctrl, trial] = None
                            if verbosity == 2: print("[skip]")
                            continue
                    if self.specific_conditions is not None:
                        if ctrl+1 not in self.specific_conditions:
                            x_arrays[subj, ctrl, trial] = []
                            y_arrays[subj, ctrl, trial] = []
                            data_arrays_orig[subj, ctrl, trial] = {}
                            data_arrays_processed[subj, ctrl, trial] = {}
                            is_test_arr[subj, ctrl, trial] = None
                            if verbosity == 2: print("[skip]")
                            continue
                    if self.specific_trials is not None:
                        if trial+1 not in self.specific_trials:
                            x_arrays[subj, ctrl, trial] = []
                            y_arrays[subj, ctrl, trial] = []
                            data_arrays_orig[subj, ctrl, trial] = {}
                            data_arrays_processed[subj, ctrl, trial] = {}
                            is_test_arr[subj, ctrl, trial] = None
                            if verbosity == 2: print("[skip]")
                            continue
                    
                    # Update the array that stores if the trial is for training or testing        
                    is_test_arr[subj, ctrl, trial] = is_test
                    
                    # Extract relevant trial of the data
                    data_trial = self.dataframe
                    if self.subjects_column:
                        data_trial = data_trial[data_trial[self.subjects_column] == subj+1]
                    if self.conditions_column:
                        data_trial = data_trial[data_trial[self.conditions_column] == ctrl+1]
                    if self.trials_column:
                        data_trial = data_trial[data_trial[self.trials_column] == trial+1]
                    if len(data_trial) == 0: # There is no data in this particular trial
                        print("")
                        x_arrays[subj, ctrl, trial] = []
                        y_arrays[subj, ctrl, trial] = []
                        data_arrays_orig[subj, ctrl, trial] = {}
                        data_arrays_processed[subj, ctrl, trial] = {}
                        is_test_arr[subj, ctrl, trial] = None
                        print("")
                        warnings.warn("No data found for subject %d, condition %d, trial %d. Skipping ..."%(subj+1, ctrl+1, trial+1), RuntimeWarning)
                        continue
                    if verbosity == 2: print(data_trial.shape, end="")
                    
                    # Input Preprocessing
                    data_in = data_trial[self.input_cols] if self.input_cols else data_trial
                    if self.input_preprocessor:
                        x = self.input_preprocessor(data_in)
                    else:
                        x = data_in.to_numpy().astype(np.float32)
                    if len(x.shape) == 1:
                        x = x.reshape(-1, 1)
                    if verbosity == 2: print("; in: ",x.shape, end="")
                    
                    # Output Preprocessing
                    data_out = data_trial[self.output_cols] if self.output_cols else None
                    if self.output_cols:
                        if self.output_preprocessor:
                            y = self.output_preprocessor(data_out)
                        else:
                            y = data_out.to_numpy().astype(np.float32)
                        if len(y.shape) == 1:
                            y = y.reshape(-1, 1)
                        if verbosity == 2: print(", out: ",y.shape, end="")
                    else:
                        y = None
                    
                    # Construct DATA_ARRAYS_ORIG
                    data_arrays_orig[subj, ctrl, trial] = {"input": x, "output": y} if self.return_data_arrays_orig else {}
                    
                    # Low-pass filter dta
                    if self.use_filtered_data:
                        data_features = butter_lowpass_filter_forward(x, self.lpcutoff, self.lpsamplfreq, self.lporder)
                    else:
                        data_features = x
                    
                    # GENERATE DATASET OBJECT
                    if self.data_squeezed:
                        dataset, self.hparams = make_squeezed_dataset(self.hparams, data_features, y, verbose=False, **kwargs)
                    else:
                        dataset, self.hparams = make_unsqueezed_dataset(self.hparams, data_features, y, verbose=False, **kwargs)
                    
                    # Get input and output tables   
                    x_processed = dataset.table_in
                    y_processed = dataset.table_out
                    if verbosity == 2:
                        print("; x: ",x_processed.shape, end="")
                        print(", y: ",y_processed.shape, end="")
                    
                    # POSTPROCESSING
                    if self.input_postprocessor:
                        x_processed = self.input_postprocessor(x_processed)
                    if self.output_postprocessor:
                        y_processed = self.output_postprocessor(y_processed)
                    if verbosity == 2:
                        print("; (post) x: ",x_processed.shape, end="")
                        print(", (post) y: ",y_processed.shape, end="")
                    
                    # Construct data arrays    
                    if self.return_train_val_test_arrays:
                        x_arrays[subj, ctrl, trial] = x_processed
                        y_arrays[subj, ctrl, trial] = y_processed
                    else:
                        x_arrays[subj, ctrl, trial] = []
                        y_arrays[subj, ctrl, trial] = []
                    if self.return_data_arrays_processed:
                        data_arrays_processed[subj, ctrl, trial] = {"input":dataset._invec, "output":dataset._outvec}
                    else:
                        data_arrays_processed[subj, ctrl, trial] = {}
                    
                    # Construct train-val-test arrays    
                    if self.return_train_val_test_data:
                        if is_test:
                            x_lst_tst.append(x_processed)
                            y_lst_tst.append(y_processed)
                        else:
                            x_lst_lrn.append(x_processed)
                            y_lst_lrn.append(y_processed)
                    
                    # Go to the next line
                    if verbosity == 2: print("\n")
        
        ########################################################################
        
        if verbosity > 0 and self.return_data_arrays_orig:
            print("Size of data_arrays_orig in bytes:      ", total_size(data_arrays_orig))
        if verbosity > 0 and self.return_data_arrays_processed:
            print("Size of data_arrays_processed in bytes: ", total_size(data_arrays_processed))           
        
        # Concatenate arrays to make all inputs and outputs, tabulated, scaled
        if verbosity > 0: print("Concatenating arrays and generating outputs ...")
        if self.return_train_val_test_data:
            if verbosity == 2: print("Returning train-val-test data ...")
            if verbosity == 2: print("Concatenating all training inputs and outputs ...")
            x_all_lrn = np.concatenate(x_lst_lrn, axis=0)
            y_all_lrn = np.concatenate(y_lst_lrn, axis=0) if self.output_cols else None
            if self.hparams.get("validation_data"):
                if verbosity == 2: print("Calculating validation data ...")
                valdata = self.hparams["validation_data"]
                if isinstance(valdata, (tuple,list)):
                    val_portion, val_set = valdata
                    if "testset" not in val_set and "trainset" not in val_set:
                        if verbosity > 0: print("WARNING: validation set is neither 'trainset' nor 'testset'. 'trainset' will be used.")
                        val_set = "trainset"
                else:
                    val_portion = valdata
                    val_set = "testset" if subjects_test or conds_test or trials_test else "trainset"
                if verbosity > 0:
                    print("Validation data source:  ",val_set)
                    print("Validation data portion: ",val_portion)
                if val_set == "trainset" or not (subjects_test or conds_test or trials_test):
                    val_data_set_x = x_all_lrn
                    val_data_set_y = y_all_lrn
                else:
                    x_all_tst = np.concatenate(x_lst_tst, axis=0)
                    y_all_tst = np.concatenate(y_lst_tst, axis=0) if self.output_cols else None
                    val_data_set_x = x_all_tst
                    val_data_set_y = y_all_tst
                if verbosity == 2: print("Splitting data to extract validation dataset") 
                if self.output_cols:
                    x_else, x_val, y_else, y_val = train_test_split(val_data_set_x, val_data_set_y, 
                        test_size=val_portion, random_state=SEED, shuffle=True)
                else:
                    x_else, x_val = train_test_split(val_data_set_x, 
                        test_size=val_portion, random_state=SEED, shuffle=True)
                    y_else = None
                    y_val = None
                    
                if val_set=="trainset":
                    x_train = x_else
                    y_train = y_else if self.output_cols else None
                    if subjects_test or conds_test or trials_test:
                        x_test = np.concatenate(x_lst_tst, axis=0)
                        y_test = np.concatenate(y_lst_tst, axis=0) if self.output_cols else None
                        # for debugging
                        print("shape of x_test: ", x_test.shape)
                        print("shape of y_test: ", y_test.shape)
                        #
                        idx = np.random.permutation(x_test.shape[0])
                        x_test = x_test[idx]
                        y_test = y_test[idx] if self.output_cols else None
                    else:
                        x_test = None
                        y_test = None
                else:
                    x_train = x_all_lrn
                    y_train = y_all_lrn
                    idx = np.random.permutation(x_train.shape[0])
                    x_train = x_train[idx]
                    y_train = y_train[idx] if self.output_cols else None
                    x_test = x_else
                    y_test = y_else if self.output_cols else None
                
            else:
                if verbosity == 2: print("No validation data specified. Using all data for training ...")
                x_train = x_all_lrn
                y_train = y_all_lrn
                
                x_val = None
                y_val = None
                idx = np.random.permutation(x_train.shape[0])
                x_train = x_train[idx]
                y_train = y_train[idx] if self.output_cols else None
                
                if subjects_test or conds_test or trials_test:
                    x_test = np.concatenate(x_lst_tst, axis=0)
                    y_test = np.concatenate(y_lst_tst, axis=0) if self.output_cols else None
                    
                    idx = np.random.permutation(x_test.shape[0])
                    x_test = x_test[idx]
                    y_test = y_test[idx] if self.output_cols else None
                else:
                    x_test = None
                    y_test = None
                
            
            if verbosity > 0:
                print("x_train: ",x_train.shape)
                if y_train is not None: print("y_train: ",y_train.shape)
                if x_val is not None: print("x_val: ",x_val.shape)
                if y_val is not None: print("y_val: ",y_val.shape)
                if x_test is not None: print("x_test: ",x_test.shape)
                if y_test is not None: print("y_test: ",y_test.shape)
                
            self.x_train = x_train
            self.x_val = x_val
            self.x_test = x_test    
            self.y_train = y_train
            self.y_val = y_val
            self.y_test = y_test
            
        else:
            if verbosity == 2: print("Not returning train-val-test data ...")
            self.x_train = []
            self.x_val = []
            self.x_test = []
            self.y_train = []
            self.y_val = []
            self.y_test = []
            
        self.is_test = is_test_arr    
        self.x_arrays = x_arrays
        self.y_arrays = y_arrays
        self.data_arrays_orig = data_arrays_orig
        self.data_arrays_processed = data_arrays_processed
        self.subjects_test = subjects_test
        self.conditions_test = conds_test
        self.trials_test = trials_test
            
        if verbosity > 0: print("Constructing output dictionary ...")    
        outdict = {
            "is_test": is_test_arr,
            "x_train": x_train, "x_val": x_val, "x_test": x_test,
            "y_train": y_train, "y_val": y_val, "y_test": y_test,
            "x_arrays": x_arrays, "y_arrays": y_arrays, 
            "data_arrays_orig": data_arrays_orig, "data_arrays_processed": data_arrays_processed,
            "hparams": self.hparams, "subjects_test": subjects_test, "conditions_test": conds_test, "trials_test": trials_test,
            "num_subjects": self.num_subjects, "num_conditions": self.num_conditions, "num_trials": self.num_trials
        }
        if verbosity > 0:
            print("Size of output dictionary in bytes: {:,d}".format(int(total_size(outdict))))
            print("Done.\n")
        self.is_processed = True
        if return_output:
            return outdict




def generate_cell_array(dataframe, hparams,
    subjects_column:str=None, conditions_column:str=None, trials_column:str=None,
    input_cols:list=None, output_cols:list=None,
    input_preprocessor=None, input_postprocessor=None, 
    output_preprocessor=None, output_postprocessor=None,
    specific_subjects:list=None, specific_conditions:list=None, specific_trials:list=None,
    num_subjects_for_testing:int=None, subjects_for_testing:list=None, 
    conditions_for_testing:list=None, trials_for_testing:list=None,
    use_filtered_data:bool=False, lpcutoff:float=None, lporder:int=None, lpsamplfreq:float=None,
    data_squeezed:bool=True, 
    return_data_arrays_orig:bool=True, 
    return_data_arrays_processed:bool=True,
    return_train_val_test_data:bool=True,
    return_train_val_test_arrays:bool=True,
    verbosity:int=0,
    **kwargs):
    """
    Generates a cell array of data arrays, given a dataframe, and a set of parameters.
    
    Comes in handy when trying to separate the subjects, conditions, and trials of some timeseries experiments,
    and processing them separately such as scaling them, etc., including or excluding some of them from training or
    testing, and trying to generate training, validation, and testing sets out of those experiments.
    
    In many occasions, because input data to models will be sequence data, data for trials need to be analyzed and 
    scanned via a sliding window separately. On the other hand, a single preprocessed, scaled dataset is required for
    training. Sometimes, differnet subjects or conditions need to be kept for testing, and only some of them are
    desired to be used for training. This function is useful for all of those cases.
    
    As a bonus, this function is also capable of rearranging and returning the original data, that can later be used 
    for plotting time plots, etc. It is also capable of preprocessing or postprocessing any sequential data before 
    or after processing with a sliding window.

    ### Args:
    
        - `dataframe` (`pd.DataFrame`): DataFrame holding all the raw timeseries data, all subjects and conditions.
        - `hparams` (dict): Dictionary to be used for extracting useful hyperparameters for the sliding window.
        
            This dicitonary will be sent to, and returned by, the `make_ann_dataset` or `make_seq2dense_dataset`
            function, depending on whether or not squeezed or unsqueezed data is desired (see below).
            This dictionary should contain the following keys:
             - `in_seq_len_sec` (float): Length of the input sequence, in seconds.
             - `out_seq_len_sec` (float): Length of the output sequence, in seconds.
             - `data_downsampling` (int): Downsampling factor, i.e. one out of how many samples will be extracted.
             - `sequence_downsampling` (int): Downsampling factor for the sequences, AFTER data downsampling.
             - `data_sampling_rate_Hz` (float): Sampling rate of the data, in Hz.
             - `validation_data` (float|tuple, optional): Portion of the data to be used for validation while training.
                These datapoints will be selected randomly out of all the data. The data will be shuffled.
                If this is a tuple, it should hold the portion, followed by which set it comes from, 
                'trainset' or 'testset'. If it is a float, it will by default come from test set, if any.
                If there is no test set applicable according to the settings, training set will be used.
                If this is a tuple, it should be e.g. [0.2, 'trainset'] or [0.1,'testset'].
            
             
            ** Description of data downsampling and sequence downsampling **
            
            The data downsampling rate downsamples the data when extracting it, so dataset size (number of samples) is divided by the downsampling rate.
            After the time series is downsampled by the `data_downsampling`, sequences are extracted from it using a sliding window. After the sequences are extracted, they can 
            still have too many time steps in them especially if the sampling rate was high to begin with. Then, the `sequence_downsampling` is applied, and all the extracted 
            sequences are downsampled. This does not change the dataset size; it only decreases the number of time steps in each sequence.
            
            Data downsampling is typically used when the sampling frequency is too high and there are too many time series or the series are too long. Sequence downsampling is 
            typically used when the sequence length (in units of time) needs to remain large enough to extract meaningful trends and information, but because the sampling 
            frequency is too high the sequences end up having too many time steps. Sequence downsampling makes sure the time-length of the sequences remains constant while the 
            number of time steps in each sequence is reduced.
            
            For example, let us assume 100 trials of a time-series experiment were performed, each lasting 100 seconds, with a sampling frequency of 1000 Hz. This means there are 
            a total of 100 K timesteps in each trial, amounting to 10 M time steps (training samples) in total. Let us assume that the sequences that you extract with a sliding 
            window need to be at least 2 seconds long to be able to extract meaningful information from them. There are two problems here. Firstly, there are too many data points 
            (10 M) in the training set. Secondly, the sequences will have too many time steps in them (2000) which will make training difficult and memory-intensive. To solve this 
            problem, we apply a `data_downsampling` rate of 4, reducing the effective sampling frequency to 250 Hz. This reduces the number of data points to 2.5 M.
            Also, this will mean that our 2-second sequences will have 500 time steps in them. Right now, 2.5 M dataset size is good, and we do not want to reduce it further. 
            However, especially if the data is smooth enough, 500 time steps in a sequence may be still too high. If we increase the `data_downsampling` rate, dataset size will 
            also decrease, and we do not want that. Therefore, we simply apply a `sequence_downsampling` rate of 10, which will reduce the number of time steps in each sequence to
            50, without touching the dataset size, affecting the rate of extracting sequences from the time series, or affecting the time length of the extracted sequences. 
            Assuming that the data is smooth and 50 timesteps forming a 2-second sequence are enough to extract meaningful information from the data, this is a good solution. 
            We will eventually have 2.5 M sequences with 50 time steps in each.
            
            Therefore, if the size and/or sampling frequency of the data is too high, data downsampling is preferred.
            However, if the dataset size is fine, but due to the long sequence length or high sampling rate, sequences
            hold too many data points in them and matrices end up being too large for the memory, sequence downsampling 
            is preferred. Sequence downsampling will not touch the size/sampling frequency of the data itself, 
            nor will it touch the true time length of the sequences. It will only make the sequences downsampled 
            and more coarse. Therefore, number of data points in the dataset will remain constant, as will the true 
            time length of the sequences. However, the number of time steps in the sequences will decrease.
            
            
            
            
            **IMPORTANT** 
            Depending on whether squeezed or unsqueezed data is required (see below), the passed hyperparameter 
            dictionary will be updated as follows:
            
             - If `data_squeezed` is True: The `input_size` and `output_size` hyperparameters will be updated.
            This is useful when MLP models will be deployed,
            where inputs are 2D tables.
            
             - If `data_squeezed` is False: The `in_seq_len` and `out_seq_len` hyperparameters will be updated.
            This is useful when generally RNN-based or CNN-based models
            will be deployed, where inputs are 3D. In this case, the `out_features` key will also be multiplied by the `out_seq_len` to get the total number of output features.
            This is because regardless of input shapes, outputs in this function are always assumed to be squeezed. `out_features` is the final output layer width.
            
            
        - `subjects_column` (str, optional): Column of the DataFrame holding subject numbers, if any. Defaults to None.
        - `conditions_column` (str, optional): Column of the DataFrame holding condition numbers. Defaults to None.
        - `trials_column` (str, optional): Column of the DataFrame holding trial numbers, if any. Defaults to None.
            **NOTE**: If any of the above arguments are None, it is assumed only one subject/condition/trial is
            involved in the timeseries experiments.
        - `input_cols` (list, optional): List of columns of input data. Defaults to None, meaning all data is input.
        - `output_cols` (list, optional): List of columns of output data. Defaults to None, meaning there is no output.
        - `input_preprocessor` (function, optional): Function to perform before processing. Defaults to None.
            **Note** This function should take in a DataFrame extracted from a specific subject/condition/trial,
            and return a numpy array containing preprocessed data.
        - `input_postprocessor` (function, optional): Function to perform after processing. Defaults to None.
            **Note** This function should take a numpy array which represents the processed tabulated data after 
            sliding window etc., and return a new numpy array with the same number of rows, containing the 
            postprocessed data.
            **Note** Scaling of inputs and outputs can be done automatically (see below) and do not need to be
            manually employed as pre/postprocessing steps.
        - `output_preprocessor` (function, optional): Same as the one for inputs. Defaults to None.
        - `output_postprocessor` (function, optional): Same as the one for inputs. Defaults to None.
        - `specific_subjects` (list, optional): List of 1-indexed subject numbers to use. Defaults to None.
        - `specific_conditions` (list, optional): List of 1-indexed condition numbers to use. Defaults to None.
            **Note** If any of the above arguments are given, the cell array will be complete, but the corresponding
            elements of the cell arrays to the subjects/conditions not included in the list will be empty lists, [].
            These data will also not be used for generating training or testing data for a model. 
        - `num_subjects_for_testing` (int, optional): Self-explanatory. Defaults to None. If provided, subjects will
            be chosen randomly from all subjects.
        - `subjects_for_testing` (list, optional): Self-explanatory. Defaults to None. It is 1-indexed.
            **Note** If `num_subjects_for_testing` is given but `subjects_for_testing` is not given, the subjects
            for testing will be chosen randomly from all subjects.
        - `conditions_for_testing` (list, optional): List of 1-indexed condition numbers used for testing.
            Defaults to None.
        - `trials_for_testing` (list, optional): List of 1-indexed trial numbers used for testing 
            out of every condition. Defaults to None.
        - `use_filtered_data` (bool, optional): Whether to low-pass filter data before processing. Defaults to False.
            **Note** If given, a digital Butterworth filter will be deployed, only forward-facing, that is,
            using `filt`, NOT `filtfilt`.
        - `lpcutoff` (float, optional): Lowpass filter cutoff frequency, Hz. Defaults to None.
        - `lporder` (int, optional): Lowpass filter order. Defaults to None.
        - `lpsamplfreq` (float, optional): Lowpass filter sampling frequency, Hz. Defaults to None.
        - `data_squeezed` (bool, optional): Whether the input data should be squeezed. Defaults to True.
            Squeezed data are 2D, as in (num_data, sequence_length*num_features),
            but unsqueezed data are 3D, as in (num_data, sequence_length, num_features).
            Squeezed data can, e.g., be used as inputs for MLP models, while unsqueezed data can be used as inputs for
            RNN/CNN models.
        - `return_data_arrays_orig` (bool, optional): Whether to return original data arrays. Defaults to True.
        - `return_data_arrays_processed` (bool, optional): Whether to return preprocecssed data arrays. Default True.
        - `return_train_val_test_data`(bool, optional): Whether to return model training-related arrays and data. 
            Defaults to True.
            If True, the function will return processed, scaled and shuffled numpy arrays ready to be plugged into
            a learning model. They will include training, validation and testsets, if applicable.
            If False, the function will not return such data. This can come in handy if no training or machine learning
            is involved in what you are trying to do, and you are trying to save memory.
        - `return_train_val_test_arrays` (bool, optional): Whether to return per-trial individual model 
        training-related arrays. Defaults to True.
        If True, the function will return processed, scaled and shuffled numpy arrays ready to be plugged into
        the machine learning model. However, these arrays will be wrapped in a cell array, where each element of the 
        array corresponds to machine-learning-ready training, validation & testing data of one individual trial of the
        experimentation.
        - `verbosity` (int, optional): Verbosity level. Defaults to 0. If 1, only the shape of the resulting databases
            are printed, as well as some fundamental information about the database. If 2, then basically everything is
            printed, along all the steps of the way.

    ### Returns:
    
        This function returns a dictionary holding some of the following, according to the arguments.
        - `is_test` (numpy nested cell arrays): Whether every trial is for testing data or not.
        - `x_train`,`x_val`,`x_test`,`y_train`,`y_val`,`y_test` (numpy arrays): Training, validation and testing
            arrays of input and output data, respectively, processed, scaled and processed with sliding window, fully
            ready to be fed to a learning algorithm. The data is also shuffled.
            If `hparams["validatoin_data"]` does not exist, `x_val` and `y_val` will be None, or empty.
            If testing-related parameters like `num_subjects_for_testing` or `subjects_for_testing` are not given,
            The `x_test` and `y_test` will be None, or empty.
            If `return_train_val_test_data` is False, `x_train`, `x_val`, `x_test`, `y_train`, `y_val`, `y_test` will
            not be included in the output dictionary.
        - `x_arrays` and `y_arrays` (numpy nested cell arrays): These include the same data as `x_train`, `x_val`, etc.,
            only they are separated for subjects, conditions and trials. If `return_train_val_test_arrays` is False,
            these will be empty lists, [].
            `x_arrays[subj,cond,trial]` holds the corresponding data of one timeseries experiment, for instance.
        - `data_arrays_orig` and `data_arrays_processed` hold the data itself, nested and rearranged,
            but not passed through the sliding window. The `orig` one holds the raw data before preprocessing function,
            if any, and the `processed` one contains preprocessed and scaled data. These will be empty or None, if 
            `return_data_arrays_orig` or `return_data_arrays_processed` are False, respectively.
            
            **Note** One of the preprocessing steps that takes place by default, is downsampling. Therefore, the `orig`
            data will NOT even be downsampled.
            
            `data_arrays_orig[subj,cond,trial]` is a dictionary holding `input` and `output` keys, whose values are the
            original or processed timeseries data for the corresponding timeseries experiment, containing the
            inputs and outputs, respectively.
            
        - `hparams` (dictionary): Dictionary of hyperparameters used in this function, modified and updated.
            **Note** Returning this object is not actually necessary. The `hparam` parameter is already modified and 
            updated, because the function modifies the reference to the hparams object, so there is no real need
            for returning it, unless for back-up or storage reasons.
        
        - `subjects_test` (list): List of subject numbers used for testing.
        - `conditions_test` (list): List of condition numbers used for testing.
        - `trials_test` (list): List of trial numbers used for testing.
        - `num_subjects`, `num_conditions`, `num_trials` (int): Number of subjects, conditions and trials, respectively.
        
        
    ### Important Implementation Notes:
    
    - In the data, subject, condition and trial numbers must be 1-indexed. The code will misbehave otherwise.
      This is a bug that will be fixed in a future improved version.
    - When indexing cell arrays, however, indexing is 0-indexed as in Python. This is also buggy behavior, and will be
      fixed in a future version. Data for subject 1, controller 1, trial 1, is accessed as `data_arrays[0,0,0]`.
        
    """
    
    # Lists of arrays holding trial data, to concatenate later
    x_lst_lrn = []
    y_lst_lrn = []
    x_lst_tst = []
    y_lst_tst = []
    
    
    num_subjects = len(dataframe[subjects_column].value_counts()) if subjects_column else 1
    num_conditions = len(dataframe[conditions_column].value_counts()) if conditions_column else 1
    num_trials = len(dataframe[trials_column].value_counts()) if trials_column else 1
    
    if verbosity > 0:
        print("Number of subjects:   ", num_subjects)
        print("Number of conditions: ", num_conditions)
        print("Number of trials:     ", num_trials)
        print("\n")
    

    # Cellular arrays holding data of each trial
    if verbosity == 2: print("Initializing data arrays ...")
    x_arrays = np.empty((num_subjects,num_conditions,num_trials), dtype=np.ndarray)
    y_arrays = np.empty((num_subjects,num_conditions,num_trials), dtype=np.ndarray) 
    data_arrays_orig = np.empty((num_subjects,num_conditions,num_trials), dtype=dict)   
    data_arrays_processed = np.empty((num_subjects,num_conditions,num_trials), dtype=dict) 
    is_test_arr = np.empty((num_subjects,num_conditions,num_trials), dtype=object)

    # Determining which trials will be used for training+validation, and which ones will be used for testing
    if verbosity == 2: print("Determining training/validation, and testing trials...")
    
    if subjects_for_testing:
        subjects_test = subjects_for_testing
    elif num_subjects_for_testing:
        subjects_test = np.random.choice(np.arange(1,num_subjects+1), size=num_subjects_for_testing, replace=False)
    else:
        subjects_test = []
    
    if conditions_for_testing:
        conds_test = conditions_for_testing
    else:
        conds_test = []
        
    if trials_for_testing:
        trials_test = trials_for_testing
    else:
        trials_test = []
        
    if verbosity > 0:
        print("subjects used for testing:   ", subjects_test)
        print("conditions used for testing: ", conds_test)
        print("trials used for testing:     ", trials_test)
        print("\n")
    
    # Iterate through each trial
    if verbosity > 0: print("Iterating through all trials ...\n")
    for subj in range(num_subjects):
        if verbosity == 2: print("  > Subject %d ... "%(subj+1), end="")
        is_test_subject = (subj+1 in subjects_test) if subjects_test else False
        if verbosity == 2: print("(testing)" if is_test_subject else "")
        for ctrl in range(num_conditions):
            if verbosity==2: print("    >> Condition %d ... "%(ctrl+1), end="")
            is_test_cond = (ctrl+1 in conds_test) if conds_test else False
            if verbosity == 2: print("(testing)" if is_test_cond else "")
            for trial in range(num_trials):
                if verbosity == 2: print("      >>> Trial %d ... "%(trial+1), end="")
                is_test_trial = (trial+1 in trials_test) if trials_test else False
                #if verbosity == 2: print("(testing) " if is_test_trial else " ", end="")
                
                # Figure out if the trial is for training or testing
                is_test = (is_test_subject or is_test_cond or is_test_trial)
                if verbosity == 2: print("(testing) " if is_test else " ", end="")
                
                # Figure out if the trial is one of the specific ones that we want
                if specific_subjects is not None:
                    if subj+1 not in specific_subjects:
                        x_arrays[subj, ctrl, trial] = []
                        y_arrays[subj, ctrl, trial] = []
                        data_arrays_orig[subj, ctrl, trial] = {}
                        data_arrays_processed[subj, ctrl, trial] = {}
                        is_test_arr[subj, ctrl, trial] = None
                        if verbosity == 2: print("[skip]")
                        continue
                if specific_conditions is not None:
                    if ctrl+1 not in specific_conditions:
                        x_arrays[subj, ctrl, trial] = []
                        y_arrays[subj, ctrl, trial] = []
                        data_arrays_orig[subj, ctrl, trial] = {}
                        data_arrays_processed[subj, ctrl, trial] = {}
                        is_test_arr[subj, ctrl, trial] = None
                        if verbosity == 2: print("[skip]")
                        continue
                if specific_trials is not None:
                    if trial+1 not in specific_trials:
                        x_arrays[subj, ctrl, trial] = []
                        y_arrays[subj, ctrl, trial] = []
                        data_arrays_orig[subj, ctrl, trial] = {}
                        data_arrays_processed[subj, ctrl, trial] = {}
                        is_test_arr[subj, ctrl, trial] = None
                        if verbosity == 2: print("[skip]")
                        continue
                        
                is_test_arr[subj, ctrl, trial] = is_test
                # data_trial = dataframe[
                #     (dataframe[subjects_column] == subj+1) & \
                #     (dataframe[conditions_column] == ctrl+1) & \
                #     (dataframe[trials_column] == trial+1)]
                
                # Extract relevant trial of the data
                data_trial = dataframe
                if subjects_column:
                    data_trial = data_trial[data_trial[subjects_column] == subj+1]
                if conditions_column:
                    data_trial = data_trial[data_trial[conditions_column] == ctrl+1]
                if trials_column:
                    data_trial = data_trial[data_trial[trials_column] == trial+1]
                if len(data_trial) == 0: # There is no data in this particular trial
                    print("")
                    x_arrays[subj, ctrl, trial] = []
                    y_arrays[subj, ctrl, trial] = []
                    data_arrays_orig[subj, ctrl, trial] = {}
                    data_arrays_processed[subj, ctrl, trial] = {}
                    is_test_arr[subj, ctrl, trial] = None
                    print("")
                    warnings.warn("No data found for subject %d, condition %d, trial %d. Skipping ..."%(subj+1, ctrl+1, trial+1), RuntimeWarning)
                    continue
                if verbosity == 2: print(data_trial.shape, end="")
                
                # Input Preprocessing
                data_in = data_trial[input_cols] if input_cols else data_trial
                if input_preprocessor:
                    x = input_preprocessor(data_in)
                else:
                    x = data_in.to_numpy().astype(np.float32)
                if len(x.shape) == 1:
                    x = x.reshape(-1, 1)
                if verbosity == 2: print("; in: ",x.shape, end="")
                
                # Output Preprocessing
                data_out = data_trial[output_cols] if output_cols else None
                if output_cols:
                    if output_preprocessor:
                        y = output_preprocessor(data_out)
                    else:
                        y = data_out.to_numpy().astype(np.float32)
                    if len(y.shape) == 1:
                        y = y.reshape(-1, 1)
                    if verbosity == 2: print(", out: ",y.shape, end="")
                else:
                    y = None
                
                # Construct DATA_ARRAYS_ORIG
                data_arrays_orig[subj, ctrl, trial] = {"input": x, "output": y} if return_data_arrays_orig else {}
                
                # Low-pass filter dta
                if use_filtered_data:
                    data_features = butter_lowpass_filter_forward(x, lpcutoff, lpsamplfreq, lporder)
                else:
                    data_features = x
                
                # GENERATE DATASET OBJECT
                if data_squeezed:
                    dataset, hparams = make_squeezed_dataset(hparams, data_features, y, verbose=False, **kwargs)
                else:
                    dataset, hparams = make_unsqueezed_dataset(hparams, data_features, y, verbose=False, **kwargs)
                
                # Get input and output trables   
                x_processed = dataset.table_in
                y_processed = dataset.table_out
                if verbosity == 2:
                    print("; x: ",x_processed.shape, end="")
                    print(", y: ",y_processed.shape, end="")
                
                # POSTPROCESSING
                if input_postprocessor:
                    x_processed = input_postprocessor(x_processed)
                if output_postprocessor:
                    y_processed = output_postprocessor(y_processed)
                if verbosity == 2:
                    print("; x: ",x_processed.shape, end="")
                    print(", y: ",y_processed.shape, end="")
                
                # Construct data arrays    
                if return_train_val_test_arrays:
                    x_arrays[subj, ctrl, trial] = x_processed
                    y_arrays[subj, ctrl, trial] = y_processed
                else:
                    x_arrays[subj, ctrl, trial] = []
                    y_arrays[subj, ctrl, trial] = []
                if return_data_arrays_processed:
                    data_arrays_processed[subj, ctrl, trial] = {"input":dataset._invec, "output":dataset._outvec}
                else:
                    data_arrays_processed[subj, ctrl, trial] = {}
                # for debugging:
                # print("-------------------------------------")
                # Construct train-val-test arrays    
                if return_train_val_test_data:
                    if is_test:
                        x_lst_tst.append(x_processed)
                        y_lst_tst.append(y_processed)
                        # For debugging
                        # print("x_lst_tst: ")
                        # print(x_lst_tst)
                        # print("length of x_lst_tst: ")
                        # print(len(x_lst_tst))
                        # print("y_lst_tst: ")
                        # print(y_lst_tst)
                        # print("length of y_lst_tst: ")
                        # print(len(y_lst_tst))
                    else:
                        x_lst_lrn.append(x_processed)
                        y_lst_lrn.append(y_processed)
                        # For debugging
                        # print("x_lst_lrn: ")
                        # print(x_lst_lrn)
                        # print("length of x_lst_lrn: ")
                        # print(len(x_lst_lrn))
                        # print("y_lst_lrn: ")
                        # print(y_lst_lrn)
                        # print("length of y_lst_lrn: ")
                        # print(len(y_lst_lrn))
                
                # Go to the next line
                if verbosity == 2: print("\n")
    
    if verbosity > 0 and return_data_arrays_orig:
        print("Size of data_arrays_orig in bytes:      ", total_size(data_arrays_orig))
    if verbosity > 0 and return_data_arrays_processed:
        print("Size of data_arrays_processed in bytes: ", total_size(data_arrays_processed))           
    # Concatenate arrays to make all inputs and outputs, tabulated, scaled
    if verbosity > 0: print("Concatenating arrays and generating outputs ...")
    if return_train_val_test_data:
        if verbosity == 2: print("Returning train-val-test data ...")
        if verbosity == 2: print("Concatenating all training inputs and outputs ...")
        # For debugging
        # print("x_lst_lrn includes %d arrays." % len(x_lst_lrn))
        # print("y_lst_lrn includes %d arrays." % len(y_lst_lrn))
        # print("x_lst_tst includes %d arrays." % len(x_lst_tst))
        # print("y_lst_tst includes %d arrays." % len(y_lst_tst))
        #
        x_all_lrn = np.concatenate(x_lst_lrn, axis=0)
        y_all_lrn = np.concatenate(y_lst_lrn, axis=0) if output_cols else None
        # for debugging
        # print("shape of x_all_lrn: ", x_all_lrn.shape)
        # if output_cols: print("shape of y_all_lrn: ", y_all_lrn.shape)
        # Up to this point everything is correct, and training data size is correct.
        if hparams.get("validation_data"):
            if verbosity == 2: print("Calculating validation data ...")
            valdata = hparams["validation_data"]
            if isinstance(valdata, tuple) or isinstance(valdata, list):
                val_portion, val_set = valdata
                if "testset" not in val_set and "trainset" not in val_set:
                    if verbosity > 0: 
                        print("WARNING: validation set is neither 'trainset' nor 'testset'. 'trainset' will be used.")
                    val_set = "trainset"
            else:
                val_portion = valdata
                val_set = "testset" if subjects_test or conds_test or trials_test else "trainset"
            if verbosity > 0:
                print("Validation data source:  ",val_set)
                print("Validation data portion: ",val_portion)
            if val_set == "trainset" or not (subjects_test or conds_test or trials_test):
                val_data_set_x = x_all_lrn
                val_data_set_y = y_all_lrn
            else:
                x_all_tst = np.concatenate(x_lst_tst, axis=0)
                y_all_tst = np.concatenate(y_lst_tst, axis=0) if output_cols else None
                val_data_set_x = x_all_tst
                val_data_set_y = y_all_tst
            if verbosity == 2: print("Splitting data to extract validation dataset") 
            if output_cols:
                x_else, x_val, y_else, y_val = train_test_split(val_data_set_x, val_data_set_y, 
                    test_size=val_portion, random_state=SEED, shuffle=True)
            else:
                x_else, x_val = train_test_split(val_data_set_x, 
                    test_size=val_portion, random_state=SEED, shuffle=True)
                y_else = None
                y_val = None
                
            if val_set=="trainset":
                x_train = x_else
                y_train = y_else if output_cols else None
                if subjects_test or conds_test or trials_test:
                    x_test = np.concatenate(x_lst_tst, axis=0)
                    y_test = np.concatenate(y_lst_tst, axis=0) if output_cols else None
                    # for debugging
                    print("shape of x_test: ", x_test.shape)
                    print("shape of y_test: ", y_test.shape)
                    #
                    idx = np.random.permutation(x_test.shape[0])
                    x_test = x_test[idx]
                    y_test = y_test[idx] if output_cols else None
                else:
                    x_test = None
                    y_test = None
            else:
                x_train = x_all_lrn
                y_train = y_all_lrn
                idx = np.random.permutation(x_train.shape[0])
                x_train = x_train[idx]
                y_train = y_train[idx] if output_cols else None
                x_test = x_else
                y_test = y_else if output_cols else None
            #
            # For debugging
            # print("Shape of x_train: ", x_train.shape)
            # if output_cols: print("Shape of y_train: ", y_train.shape)
            # print("Shape of x_val: ", x_val.shape)
            # if output_cols: print("Shape of y_val: ", y_val.shape)
            # print("Shape of x_test: ", x_test.shape)
            # if output_cols: print("Shape of y_test: ", y_test.shape)
            # This conditional block seems to be working fine.
        else:
            if verbosity == 2: print("No validation data specified. Using all data for training ...")
            x_train = x_all_lrn
            y_train = y_all_lrn
            # For debugging
            # print("Shape of x_train before shuffling: ", x_train.shape)
            # if output_cols: print("Shape of y_train before shuffling: ", y_train.shape)
            # Up to this point everything is correct.
            x_val = None
            y_val = None
            idx = np.random.permutation(x_train.shape[0])
            x_train = x_train[idx]
            y_train = y_train[idx] if output_cols else None
            # For debugging
            # print("Shape of x_train after shuffling: ", x_train.shape)
            # if output_cols: print("Shape of y_train after shuffling: ", y_train.shape)
            # Up to this point everything is correct.
            if subjects_test or conds_test or trials_test:
                x_test = np.concatenate(x_lst_tst, axis=0)
                y_test = np.concatenate(y_lst_tst, axis=0) if output_cols else None
                # for debugging
                # print("shape of x_test: ", x_test.shape)
                # print("shape of y_test: ", y_test.shape)
                #
                idx = np.random.permutation(x_test.shape[0])
                x_test = x_test[idx]
                y_test = y_test[idx] if output_cols else None
            else:
                x_test = None
                y_test = None
            
        
        if verbosity > 0:
            print("x_train: ",x_train.shape)
            if y_train is not None: print("y_train: ",y_train.shape)
            if x_val is not None: print("x_val: ",x_val.shape)
            if y_val is not None: print("y_val: ",y_val.shape)
            if x_test is not None: print("x_test: ",x_test.shape)
            if y_test is not None: print("y_test: ",y_test.shape)
        # if subjects_test or conds_test or trials_test:
        #     x_test = np.concatenate(x_lst_tst, axis=0)
        #     y_test = np.concatenate(y_lst_tst, axis=0) if output_cols else None
        #     # for debugging
        #     print("shape of x_test: ", x_test.shape)
        #     print("shape of y_test: ", y_test.shape)
        #     #
        #     idx = np.random.permutation(x_test.shape[0])
        #     x_test = x_test[idx]
        #     y_test = y_test[idx] if output_cols else None
        # else:
        #     x_test = None
        #     y_test = None
            
        
    else:
        if verbosity == 2: print("Not returning train-val-test data ...")
        x_train = []
        x_val = []
        x_test = []
        y_train = []
        y_val = []
        y_test = []
        
        
    if verbosity > 0: print("Constructing output dictionary ...")    
    outdict = {
        "is_test": is_test_arr,
        "x_train": x_train, "x_val": x_val, "x_test": x_test,
        "y_train": y_train, "y_val": y_val, "y_test": y_test,
        "x_arrays": x_arrays, "y_arrays": y_arrays, 
        "data_arrays_orig": data_arrays_orig, "data_arrays_processed": data_arrays_processed,
        "hparams": hparams, "subjects_test": subjects_test, "conditions_test": conds_test, "trials_test": trials_test,
        "num_subjects": num_subjects, "num_conditions": num_conditions, "num_trials": num_trials
    }
    if verbosity > 0:
        print("Size of output dictionary in bytes: {:,d}".format(int(total_size(outdict))))
        print("Done.\n")
    return outdict