

def npixel_samples_in_stimulus_clock(
        npixel_samples, 
        beh2stim_slope, 
        beh2stim_intercept, 
        npixel2beh_slope, 
        npixel2beh_intercept,
        **kwargs
    ): 
    """
    Function to convert neuropixel sample times to stimulus clock times.
    
    :param npixel_samples: 
    :param beh2stim_slope: 
    :param beh2stim_intercept: 
    :param npixel2beh_slope: 
    :param npixel2beh_intercept: 
    """
    return beh2stim_slope * (npixel2beh_slope * npixel_samples + npixel2beh_intercept) + beh2stim_intercept