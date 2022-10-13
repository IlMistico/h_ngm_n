FROM python:3.10.7-buster as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir ./wheels -r requirements.txt



FROM python:3.10.7-buster 

ENV HOST "0.0.0.0"
ENV PORT 8765

# # Set these variables if you have certificates for the server domain and wish to use https.
# ENV SSL_KEYFILE /path/to/privkey.pem
# ENV SSL_CERTFILE /path/to/fullchain.pem

EXPOSE $PORT

RUN apt-get update && apt-get upgrade -y

COPY --from=builder /usr/src/wheels ./wheels
COPY --from=builder /usr/src/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache ./wheels/*

WORKDIR /src
COPY . /

CMD ["python", "main.py"]