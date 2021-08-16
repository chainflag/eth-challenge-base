FROM python:3-slim-buster

WORKDIR /home/ctf

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libsodium-dev tini xinetd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py .
COPY eth_challenge_base eth_challenge_base/

COPY entrypoint.sh /entrypoint.sh
COPY 00-create-xinetd-service 99-start-xinetd /startup/

RUN mkdir /var/log/ctf
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
