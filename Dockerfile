FROM alpine
MAINTAINER Ove Stavnås
COPY skagenfondene/requirements.txt /requirements.txt
RUN apk update ; \
    apk add python3 \
            python3-dev \
            libxslt-dev \
            libxml2-dev \
            g++ ; \
    pip3 install -r requirements.txt
COPY skagenfondene /skagenfondene
WORKDIR /skagenfondene
ENTRYPOINT ["python3", "sf.py"]
