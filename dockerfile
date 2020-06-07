# Pull base image
FROM python:3.7-buster

RUN mkdir -p /app
RUN mkdir -p /usr/src/static
RUN mkdir -p /usr/src/data


WORKDIR /app
COPY ./ /app

RUN pip install -r requirements.txt
# Copy project
COPY . /code/

EXPOSE 80

# Run gunicorn
CMD sh start.sh