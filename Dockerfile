FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "AIJobMatcher.wsgi:application", "--bind", "0.0.0.0:8000"]
