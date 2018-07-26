FROM alpine
RUN mkdir /www
WORKDIR /www
COPY . /www/
RUN apk update
RUN apk upgrade
RUN apk --no-cache add \
    python3 \
    python3-dev \
    build-base \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    openssl-dev
RUN pip3 install --upgrade pip
RUN pip3 install -e .
ENV PYTHONUNBUFFERED 1