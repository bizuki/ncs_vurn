FROM python:3.10-alpine
# used with live-reload so .pyc isn't stored on host
ENV PYTHONPYCACHEPREFIX=/tmp
#/
WORKDIR /app
EXPOSE 5000
COPY . .
RUN pip install pipenv
RUN pipenv install --deploy --system
ENTRYPOINT ["python", "/app/src/main.py"]
