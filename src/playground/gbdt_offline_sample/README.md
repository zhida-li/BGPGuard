# gbdt_offline_sample

GBDT Python sample code for network anomaly detection

**XGBoost, LightGBM, CatBoost**

---

###### Python 3.6 or newer

## Requirement Python libraries:

- numpy

- scipy

- scikit-learn

- xgboost

- lightgbm

- catboost

## 🏗️ Install the external Python libraries by running:

```bash
pip install -r requirements.txt
```

## 🚀 Run experiments
### 1. Specify the hyper-parameters in n the cross-validation file, then run:

```bash
python gbm_crossValidate.py
```

Folders are generated: 

- tempAcc_lightgbm_slammer_all
- tempAcc_lightgbm_slammer_16
- tempAcc_lightgbm_slammer_8

Then, the best sets of parameters (num_estimators and learn_rate) are saved in 
`lightgbm_param_final_slammer.csv` (the last two columns).

### 2. Enter the best parameters into `final_eval_gbm.py`, and run:

```bash
python final_eval_gbm.py
```

Results are saved in `lightgbm_param_final_slammer.csv`.

---

### 📒 Note:

Cross-validation python file may be edited if new datasets will be added:

> ./journalLib/gbm_cross_validation.py
