FROM python:3.8-slim
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
COPY app.py app.py
CMD ["flask", "run"]

