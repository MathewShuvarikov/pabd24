# syntax=docker/dockerfile:1

FROM python:3.10
WORKDIR /app
COPY . .
RUN apt-get -y update && apt-get install -y cmake
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt
CMD ["python3", "src/predict_app.py"]
EXPOSE 5000