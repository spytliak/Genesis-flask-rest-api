FROM python:3.9-alpine as base

LABEL NAME="spytliak/genesis-flask-rest-api"
LABEL VERSION="0.0.1"
LABEL MAINTEINER="Serhii Pytliak pytliak.serhii@gmail.com" 

RUN apk add -u --no-cache gcc libc-dev libffi-dev curl && \
    rm -rf /var/cache/apk/*

FROM base as builder

WORKDIR /install

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip --no-cache-dir --prefix=/install -r /tmp/requirements.txt

FROM base

COPY --from=builder /install /usr/local

WORKDIR /app 
COPY /app /app

ENV FLASK_RUN_HOST="0.0.0.0"
ENV PORT="5000"
ENV FLASK_APP="api.py"
ENV FLASK_DEBUG: 1

HEALTHCHECK --interval=5s --timeout=3s --start-period=3s --retries=3 CMD [ "curl", "0.0.0.0:5000" ]

EXPOSE 5000

CMD ["flask", "run"]