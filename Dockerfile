FROM python:3.6-alpine

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

WORKDIR /var/www

ENTRYPOINT ["python"]
CMD ["app.py", "-p 8000"]