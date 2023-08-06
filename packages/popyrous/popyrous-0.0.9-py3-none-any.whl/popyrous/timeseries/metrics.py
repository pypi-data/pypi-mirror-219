

import numpy as np
from sklearn.metrics import accuracy_score, f1_score



def tsc_metrics(y_true, y_pred, transition_radius:int=None, consistency_penalty:float=1.0):
    """
    Calculate metrics for a time series classification problem.
    Metrics include:
     - `accuracy`: Overall accuracy score
     - `f1_score`: Overall F1 score
     - `concurrency`: Accuracy of the model in transition regions.
     - `consistency`: Accuracy of the model in consistent regions, reduced using a penalty.
     
     ### Parameters
     
        - `y_true`: True labels for the data, of a single timeseries experiment.
        - `y_pred`: Predicted labels for the data, of a single timeseries experiment.
        - `transition_radius`: Radius of transition regions, in number of time steps.
        - `consistency_penalty`: Penalty for consistency.
        
    ### Returns
        
    A dictionary holding the above metrics.
    
    **NOTE** The `consistency_penalty` multiplies the number of erroneous predictions in the consistent regions 
    by this value, before calculating the accuracy.
        
    """
    
    # Squeeze data
    y_true = y_true.squeeze()
    y_pred = y_pred.squeeze()
    num_points = len(y_true)
    
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    # Auto-radius
    if not transition_radius:
        transition_radius = len(y_true)//20
    
    # Find transition points
    trans_points = np.where(np.diff(y_true) != 0)[0] + 1
    
    # Find indices of transition points
    indices = np.concatenate([np.arange(trans-transition_radius, trans+transition_radius+1) \
        for trans in trans_points]).astype(int)
    indices_list = indices.tolist()
    indices_list_opposite = [i for i in range(num_points)]
    for idx in indices_list:
        indices_list_opposite.remove(idx)
    
    # Extract indices of transition points and their vicinity from both y_true and y_pred
    y_true_transition = y_true[indices].astype(np.float32)
    y_pred_transition = y_pred[indices].astype(np.float32)
    
    # Calculate concurrency of chosen data
    concurrency = accuracy_score(y_true_transition, y_pred_transition)
    
    y_true_consistent = y_true[indices_list_opposite].astype(np.float32)
    y_pred_consistent = y_pred[indices_list_opposite].astype(np.float32)
    
    # Calculate consistency of chosen data
    consistency = 1-consistency_penalty+consistency_penalty*accuracy_score(y_true_consistent, y_pred_consistent)
    
    return {"accuracy":accuracy, "f1_score":f1, "consistency":consistency, "concurrency":concurrency}
