FROM python:3.11

WORKDIR /app

RUN pip install Flask prometheus_client

COPY /app/app.py /app/app.py

EXPOSE 5000

ENV FLASK_APP /app/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]