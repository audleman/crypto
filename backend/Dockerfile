# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Copying requirements.txt first prevents any change in the code directory from 
# re-running the pip install step
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python manage.py runserver 0.0.0.0:8000"]