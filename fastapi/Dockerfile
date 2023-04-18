FROM python:3.9

RUN mkdir /proj
COPY ./ /proj
WORKDIR /proj

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false 
RUN poetry config experimental.new-installer false
RUN poetry install --no-dev

WORKDIR /
