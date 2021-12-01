# BGPDetect-web-app
The Flask web application of the BGP Anomaly Detection Tool

Structure:
```
BGPAnomalyDectionTool
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── LICENSE
├── templates
│   ├── index.html
│   ├── bgp_ad_realtime.html
│   ├── bgp_ad_offline.html
│   ├── contact.html
│   └── layout.html
│
├── static
│	├── css
│	│   └── style.css
│	├── js
│	│ 	├── backToTop.js
│	│ 	├── data_emit.js
│	│	└── ...
│	├── img
│	│ 	├── BGPAnomalyDetect_framework.png
│	│ 	├── cnl_logo.png
│	│ 	├── profile.png
│	└──	└── ...
│
├── apps
│	├── __init__.py
│	├── app_realtime
│	│   ├── __init__.py
│	│	├── models.py
│	│	└── ...
│	├── app_offline
│	│   ├── __init__.py
│	│	├── models.py
│	│	└── ...
│	│	   ├── ...
│	│	   ├── ...
│	└──	   └── ...
│
├── database
│	├── __init__.py
│	├── database.py
│	├── db_files
│	│	├── ...
│	└──	└── ...
└──	
```

Run app:

```bash
FLASK_APP=app.py flask run
```
