# BGPGuard

A Flask web application of the BGP Anomaly Detection Framework.

Structure:

``` 
BGPGaurd
├── LICENSE
├── README.md
├── app.py
├── app_offline.py
├── app_realtime.py
├── config.py
├── requirements.txt
├── database
│   ├── database.py
│   └── db_files
├── src
│   ├── __init__.py
│   ├── check_versions.py
│   ├── dataDownload.py
│   ├── data_partition.py
│   ├── data_process.py
│   ├── featureExtraction.py
│   ├── input_exp.txt
│   ├── label_generation.py
│   ├── progress.py
│   ├── progress_bar.py
│   ├── subprocess_cmd.py
│   ├── time_tracker.py
│   ├── CSharp_Tool_BGP
│   ├── STAT
│   ├── VFBLS_v110
│   ├── data_historical
│   ├── data_ripe
│   ├── data_routeviews
│   ├── data_split
│   ├── data_test
│   └── parmSel
├── static
│   ├── css
│   │   └── style.css
│   ├── imgs
│   │   ├── bgpGuard_framework.png
│   │   ├── bgpGuard_index__jumbotron.png
│   │   ├── bgpGuard_index_offline.png
│   │   ├── bgpGuard_index_realtime.png
│   │   └── profile_zl.png
│   └── js
│       ├── click_func.js
│       ├── data_emit_labels_5min.js
│       ├── echart_emit_cpu.js
│       ├── echart_emit_features.js
│       └── echart_emit_labels.js
└── templates
    ├── bgp_ad_offline.html
    ├── bgp_ad_realtime.html
    ├── contact.html
    ├── index.html
    └── layout.html
```

Run app:

```bash
> export FLASK_APP=app.py
> export FLASK_ENV=development
> flask run
 * Running on http://127.0.0.1:5000/
```
