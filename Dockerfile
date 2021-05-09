FROM python:alpine

WORKDIR /opt/base16-builder-python

RUN pip install -U pip \
 & pip install pybase16-builder \
 & pybase16 update -v \
 & pybase16 build -t styles -v


FROM python:alpine

RUN apk add --no-cache --virtual .build-deps git \
 & cd /opt \
 & git clone https://github.com/Master-Hash/postcard.git \
 & cd postcard \
 & pip install -U -r ./requirements.txt \
 & python ./translate.py compile \
 & apk del .build-deps \
 & curl -O https://raw.fastgit.org/P3TERX/GeoLite.mmdb/download/GeoLite2-City.mmdb

COPY --from=0 ["/opt/base16-builder-python/output/styles/css-variables/", "/opt/postcard/templates/themes/"]

EXPOSE 8000
WORKDIR /opt/postcard
CMD ["uvicorn", "--host", "0.0.0.0" "postcard:app"]
