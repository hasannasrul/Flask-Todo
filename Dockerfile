FROM python:3.9.15-slim-bullseye
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "app.py" ]
EXPOSE 7000