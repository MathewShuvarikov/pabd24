# Predictive Big Data Analytics

In this repo I create a web-app which determines the price for a flat in Moscow using ML-model under the hood

## Installation 

Clone the repo, create vertual environment, activate and install dependencies:  

```sh
git clone https://github.com/MathewShuvarikov/pabd24
cd pabd24
python -m venv venv

source venv/bin/activate  # mac or linux
.\venv\Scripts\activate   # windows

pip install -r requirements.txt
```

## Usage

### 1. Data collection
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/parse_cian.py">parse_cian.py</a></strong> Script for parsing flats charachteristics (e.g. price, location, meters etc.).</li>

```sh
python src/parse_cian.py 
```  

### 2. Upload data to S3 storage
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/upload_to_s3.py">upload_to_s3.py</a></strong> Script for uploading parsed files to S3 storage.</li> 
Для доступа к хранилищу скопируйте файл `.env` в корень проекта.  

```sh
python src/upload_to_s3.py -i data/raw/file.csv
```
i - an argument we use in funtion ('i' for 'input'), in this specific situation we provide a path to files we want to upload to S3 storage
### 3.Download data to your local machine 
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/download_from_s3.py">download_from_s3.py</a></strong> Script for downloading files from S3 storage to your local directory.</li> 

```sh
python src/download_from_s3.py
```

### 4. Data preprocessing 
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/preprocess_data.py">preprocess_data.py</a></strong> Script for data preprocessing.</li> 

```sh
python src/preprocess_data.py
```
For feature engineering, I used data in what administrative district (there are 12 of them) the flat is located. File with mapping lies <a href="https://github.com/MathewShuvarikov/pabd24/blob/main/mapping/county.txt">here</a></li> 

### 5. Model training
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/train_model.py">train_model.py</a></strong> Script for model training.</li> 

```sh
python src/train_model.py
```

### 6. Flask app launch
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/predict_app.py">predict_app.py</a></strong> Script for app launching.</li>

```sh
python src/predict_app.py
```

### 7. Service usage through web-interface

For service usage use this file `web/index.html`.  

### 8. App on production server
Detailed description of testing this web-application through virtual machine using gunicorn is <strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/docs/report_3.md">here.</a>

Port on which the application is currently running: 'http://192.144.12.8:8000/predict'
