import numpy as np

def compute_explainable_var(outputs, eps=1e-9):
    """
    Args:
        outputs (list): Neuronal responses (ground truth) to image repeats. Dimensions: [num_images] np.array(num_reaps, num_neurons).
                        Expects either a 3D numpy array of shape (N images, N repeats, N neurons),
                        or a list of numpy arrays. with one list per test image, for example:
                            outputs = [np.array(20, 100), np.array(19, 100), np.array(20, 100), ...]
                        - in this example, there are as many images as there are list entries.
                        - and in each array, there are the number of responses
                            (20 repeats, or less, depending on the number of valid trials)
                            times the number of neurons (N=100 in this example)
    Returns:
        explainable_var (np.array): the fraction of explainable variance per neuron (0.0 - 1.0)

    """
    ImgVariance = []
    TotalVar = np.var(np.vstack(outputs), axis=0, ddof=1)
    for out in outputs:
        ImgVariance.append(np.var(out, axis=0, ddof=1))
    ImgVariance = np.vstack(ImgVariance)
    NoiseVar = np.mean(ImgVariance, axis=0)
    explainable_var = (TotalVar - NoiseVar) / (TotalVar + eps)
    return explainable_var