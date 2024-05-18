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


## Usage

### 1. Data collection
<li><strong><a href="https://github.com/MathewShuvarikov/pabd24/blob/main/src/parse_cian.py">parse_cian.py</a></strong> Script for pasing flats charachteristics (e.g. price, location, meters etc.).</li>

### 2. Upload data to S3 storage
Для доступа к хранилищу скопируйте файл `.env` в корень проекта.  

todo  

### 3. Загрузка данных из S3 на локальную машину  

todo  

### 4. Предварительная обработка данных  

todo 

### 5. Обучение модели 

todo Описание модели и входных параметров для предсказания здесь.  

### 6. Запуск приложения flask 

todo

### 7. Использование сервиса через веб интерфейс 

Для использования сервиса используйте файл `web/index.html`.  
