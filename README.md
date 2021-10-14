# BGPDetect-web-app
The Flask web application of the BGP AnomalyDetection Tool

Structure:
	```
	BGPAnomalyDectionTool
	├── README.md
	├── LICENSE
	├── service
	│   ├── requirements.txt
	│   ├── app.py
	│   ├── Tool module 1
	│   ├── Tool module 2
	│   ├── Tool module 3
	│   └── ...
	└── ui
		├── src
		│   ├── index.html
		│	├── bgp-ad-experiment.html
		│ 	├── bgp-ad-realtime.html
		│	├── common
		│	   ├── layout.html
		├── static
		│ 	├── unknown.css
		│ 	├── unknown.js
		│	├── image
		│	   ├── RNN model.png
		│	   ├── BLS model.png
		└──	   ├── logo.png
	```

Run app:
    ```bash
    FLASK_APP=app.py flask run
    ```
