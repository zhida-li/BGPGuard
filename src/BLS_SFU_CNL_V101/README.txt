BLS_SFU_CNL_V1.0.1
======================================================================
@authors Zhida Li, Ana Laura Gonzalez Rios, and Guangyu Xu
@email {zhidal, anag, gxa5}@sfu.ca
@date Nov. 4, 2019
@version: 1.0.1
@description:
            Modules of BLS, RBF-BLS, CFBLS, CEBLS, and CFEBLS and 
	    incremental BLS, RBF-BLS, CFBLS, CEBLS, and CFEBLS.

@copyright Copyright (c) Nov. 4, 2019
    All Rights Reserved

Python code (version 3.6)
----------------------------------------------------------------------
The BLS code relies on several external libraries.
The external libraries are expected to be installed on the system prior to running the main files.

Libraries that are installed by pip (a package management system):
- NumPy: The fundamental package for scientific computing with Python, 
  https://numpy.org/

- Scipy:  The Python library used for mathematics, science, and engineering, 
  https://www.scipy.org/

- Scikit-learn: Tools for data mining and data analysis, 
  https://scikit-learn.org/stable/

----------------------------------------------------------------------
Structure:
BLS_SFU_CNL_V1.0.1
│   README.txt
│   BLS_demo_for_lower_memory.py  
│	BLS_incremental_demo_lower_memory.py
│
└───bls
    │   __init__.py
    │  
	└───model
	│   │   __init__.py
	│   │   bls_train_fscore.py
	│   │	rbfbls_train_fscore.py
	│   │	cfbls_train_fscore.py
	│   │	cebls_train_fscore.py
	│   │	cfebls_train_fscore.py
	│   │	bls_train_fscore_incremental.py
	│   │	rbfbls_train_fscore_incremental.py
	│   │	cfbls_train_fscore_incremental.py
	│   │	cebls_train_fscore_incremental.py
	│   │	cfebls_train_fscore_incremental.py
	│   
	└───processing
		│   __init__.py
		│   mapminmax.py
		│   one_hot_m.py
		│   result.py
		│   sparse_bls.py
		│   replaceNan.py

----------------------------------------------------------------------
The following Python files are needed to run the code:
- BLS_demo_for_lower_memory.py  
- BLS_incremental_demo_lower_memory.py

Run the Python code
Type the following command in the directory BLS_SFU_CNL_V1.0.1:
>  python3 xxx.py

Note: xxx.py are Python files.
Detailed descriptions are written in each files.

