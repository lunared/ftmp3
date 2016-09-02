FROM python:3.5-alpine

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

WORKDIR /var/www

ENTRYPOINT ["gunicorn"]
CMD ["-w", "4", "-b", "0.0.0.0:5000", "app:app"]
