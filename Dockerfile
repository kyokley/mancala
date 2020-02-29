FROM python:3.8-slim AS build
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH:/root/.poetry/bin"
RUN python3 -m venv $VIRTUAL_ENV

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR /code
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . /code
RUN python setup.py install


FROM build AS prod
CMD ["mancala-series"]


FROM build AS dev
RUN apt-get install -y git
RUN poetry install

CMD ["mancala-series"]