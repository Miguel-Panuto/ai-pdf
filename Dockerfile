FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY create_gcp_keys.py ./
RUN python create_gcp_keys.py

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/gcp-keys.json


CMD [ "python", "." ]
