FROM python

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install -r requirements.txt

CMD python collect_weather_data.py
