# syntax=docker/dockerfile:1

FROM python:3.10
WORKDIR /app
COPY . .
RUN apt-get -y update && apt-get install -y cmake
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt
RUN gunicorn -b 0.0.0.0 src.predict_app:app --deamon
# CMD ["python3", "src/predict_app.py"]
EXPOSE 5000