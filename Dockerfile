FROM python:3.11 as builder

RUN pip install maturin

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade
RUN apt-get install -y curl build-essential gcc make
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup-init.sh
RUN sh rustup-init.sh -y

ENV PATH="/root/.cargo/bin:${PATH}"

COPY ./lib/pdf_extraction .

RUN cargo build

RUN maturin build --release

FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY --from=builder /usr/src/app/target/wheels/*.whl .
RUN pip install *.whl

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/gcp-keys.json


CMD [ "python", "." ]
