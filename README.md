<p align="center">
  <img width="50%" src="./static/imgs/bgpGuard_logo.png" alt="BGPGuard logo">
</p>

<h2 align="center">
  BGP anomaly detection tool that integrates various stages of the anomaly detection process
</h2>

## About BGPGuard
**BGPGuard** is used to detect BGP anomalous events based on 
routing records collected from major Internet exchange points worldwide. 
It also facilitates creating new machine learning models based on historical BGP anomalous events.
**BGPGuard** integrates various stages of the anomaly detection process. 
The tool consists of: data download, feature extraction, label refinement, data partition, data processing, 
machine learning algorithms, parameter selection, machine learning models, and classification modules.
**BGPGuard** is based on Python and JavaScript and has been developed with both terminal-based 
and web-based applications for Linux platforms.
The web-based version of **BGPGuard** offers an interactive interface with a better view for monitoring and performing experiments. 
Its front-end is built based on HTML, CSS ([Bootstrap](https://getbootstrap.com): an open-source CSS framework), 
and [Socket.IO](https://socket.io) (a transport protocol written in a JavaScript for real-time web applications).
Its back-end is developed using [Flask](https://flask.palletsprojects.com/en/2.0.x) 
(a micro web framework written in Python).

**BGPGuard** is used for real-time anomaly detection or off-line data classification 
based on messages collected from [RIPE](https://www.ripe.net/analyse) or [Route Views](http://www.routeviews.org).
For real-time anomaly detection, BGP _update_ messages are retrieved, processed, and analyzed using available pre-trained models. 
The off-line classification is based on the specified start and end dates, times of 
the anomalous event, partitioning of the training and test datasets, and 
machine learning algorithms (GBDT, CNN, RNN, or [VFBLS](https://ieeexplore.ieee.org/document/9430511)).

![](./static/imgs/bgpGuard_modules.png)

---

## Structure:

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
│   └── playground
├── static
│   ├── css
│   │   └── style.css
│   ├── imgs
│   └── js
└── templates
    ├── bgp_ad_offline.html
    ├── bgp_ad_realtime.html
    ├── contact.html
    ├── index.html
    └── layout.html
```
The `src` directory contains the source code for the real-time detection and off-line classification tasks.
Various Python functions have been developed to implement and incorporate the anomaly detection steps.

---

## 🏗️ Getting Started with BGPGuard
###### Python 3.6

### External Libraries
The web-based application relies on additional external libraries. 
The external CSS and JavaScript libraries provided by [_jsDelivr_](https://www.jsdelivr.com) have been 
included in `layout.html`.

The Python libraries installed by [_pip_](https://pip.pypa.io/en/stable/) are:
- [_NumPy_](https://numpy.org): used to perform mathematical operations 
on multi-dimensional arrays and on matrices generated during the process.
- [_SciPy_](https://scipy.org): dependency of the _scikit-learn_ library. 
_SciPy_'s _zscore_: function used to perform normalization.
- [_scikit-learn_](https://scikit-learn.org/stable): employed for processing data and calculating performance metrics.
- [_PyTorch_](https://pytorch.org): used for developing deep learning models.

- [_Flask_](https://flask.palletsprojects.com/en/2.0.x): web framework based on _Werkzeug_
and _Jinja_.
(The _Flask_'s functions are used to transfer variables and render web pages. 
_Flask_ also processes the GET/POST requests from the front-end.)
- [_Werkzeug_](https://werkzeug.palletsprojects.com/en/2.0.x): web application library used to 
create a web server gateway interface (WSGI).
- [_Jinja_](https://jinja.palletsprojects.com/en/3.0.x): web template engine. Variables, statements, 
and expressions allowed to include in HTML files. 
- [_Flask-SocketIO_](https://flask-socketio.readthedocs.io/en/latest): offers bi-directional communications 
with low latency between the clients (front-end) and the server (back-end) for _Flask_ applications.
- [_python-engineio_](https://python-socketio.readthedocs.io/en/latest): implementation of the _Engine.IO_ in Python. 
- [_python-socketio_](https://github.com/miguelgrinberg/python-engineio): library for real-time communication 
between client and server based on WebSocket. 
- [_Eventlet_](https://eventlet.net): networking library for executing asynchronous tasks.

### Install the external Python libraries by running:

```bash
pip install -r requirements.txt
```

### The C# compiler should be installed prior to executing the BGP C# tool.
- [_Mono_](https://www.mono-project.com): an open source version of Microsoft .NET framework. 
Mono includes a C# compiler for several operating systems 
such as macOS, Linux, and Windows.

## 🚀 Launching BGPGuard
The Python file `app.py` is used to execute the application.
The following command is used to start the application:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Running on:
```bash
http://127.0.0.1:5000/
```

---
## 🎡 Playground
Sample code for gradient boosting machines may be run without launching the `app.py`:
```bash
./src/playground/gbdt_offline_sample
```
Please see details in `README.md`.
