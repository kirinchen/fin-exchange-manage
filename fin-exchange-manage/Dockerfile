FROM python:3.11.5
RUN pip install pipenv
COPY ./fin-exchange-manage /myapp
ADD ./max-exchange-api-python3 /max-exchange-api-python3
WORKDIR  /myapp
RUN pipenv install

EXPOSE 5000
ENV FLASK_ENV=production
ENV FLASK_APP=main
RUN ls -al
CMD ["pipenv","run","flask","run","--host=0.0.0.0"]
