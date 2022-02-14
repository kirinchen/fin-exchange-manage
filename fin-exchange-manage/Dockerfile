FROM python:3.9.2
RUN pip install pipenv
COPY ./fin-exchange-manage /myapp
ADD ./max-exchange-api-python3 /max-exchange-api-python3
WORKDIR  /myapp
RUN pipenv install

EXPOSE 5000
ENV FLASK_APP=main
ENV FLASK_ENV=production
CMD ["pipenv","run","flask","run","--host=0.0.0.0"]
