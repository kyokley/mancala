FROM python:3.8-slim
ARG REQS=base

RUN /bin/bash -c "if [[ x\"$REQS\" == xdev ]] ; then \
        apt-get update && \
        apt-get install -y git ; fi"

COPY . /code
WORKDIR /code

RUN pip install -r ${REQS}_requirements.txt

CMD ["mancala-series"]
