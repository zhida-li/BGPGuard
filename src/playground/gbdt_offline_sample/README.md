# gbdt_offline_sample

GBDT Python sample code for network anomaly detection

**XGBoost, LightGBM, CatBoost**

---

###### Python 3.6 or newer

*Requirement Python libraries:*

- numpy

- scipy

- scikit-learn

- xgboost

- lightgbm

- catboost

## Install the external Python libraries by running:

```bash
> pip install -r requirements.txt
```

#n the cross-validation file
Specify the hyper-parameters, then run:

```bash
> python gbm_crossValidate.py
```

Folders are generated: 

- tempAcc_lightgbm_slammer_all
- tempAcc_lightgbm_slammer_16
- tempAcc_lightgbm_slammer_8

Then, the best sets of parameters (num_estimators and learn_rate) are saved in 
_lightgbm_param_final_slammer.csv_ (the last two columns).

Enter the best parameters into _final_eval_gbm.py_, and run it:

```bash
> python final_eval_gbm.py
```

Results are saved in _lightgbm_param_final_slammer.csv_.

---

**Note:**

Cross-validation python file may be edited if new datasets will be added:

> ./journalLib/gbm_cross_validation.py
