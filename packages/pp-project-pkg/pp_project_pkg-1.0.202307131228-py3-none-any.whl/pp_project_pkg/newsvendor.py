## newsvendor functions

__all__ = ['newsvendor_func']


def newsvendor_func(latest_pred,pred_val,actual_val):
    """
    Newsvendor function

    Args:
        latest_pred: forcast value of the latest iteration
        pred_val : list of prediction (last 7 days before the latest iteration preferable)
        actual_val : list of number. Same length as pred.
        avg_mean: mean of the overall data
        avg_std: std of the overall data
    """

    p = ((actual_val).sum()/len(actual_val)) / ((pred_val.sum())/len(pred_val))
    val = latest_pred * p
    return val

