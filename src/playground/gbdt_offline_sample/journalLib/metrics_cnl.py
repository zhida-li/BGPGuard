"""
Metrics: confusion matrix
Author: Zhida Li
Date: Oct. 17, 2020
"""


# print(__doc__)

def confusion_matrix_cnl(y_true, y_pred):
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    # Find the labels for anomaly and regular classes
    y_anomalyRef = 1
    y_regularRef = 2
    # for y_true_i in y_true:
    #     if y_true_i != 1:
    #         y_regularRef = y_true_i
    #     break
    # Calculate TP FN FP TN
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i] == y_anomalyRef:
            tp += 1
        elif (y_true[i] != y_pred[i]) and (y_pred[i] == y_regularRef):
            fn += 1
        elif (y_true[i] != y_pred[i]) and (y_pred[i] == y_anomalyRef):
            fp += 1
        elif y_true[i] == y_pred[i] == y_regularRef:
            tn += 1
        else:
            print("Please check input vectors.")
            print(y_regularRef)

    return tp, fn, fp, tn
