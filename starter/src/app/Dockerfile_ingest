FROM oraclelinux:8
WORKDIR /app

RUN dnf install -y sudo wget unzip
COPY src_ingest .
RUN ls -al
RUN chmod +x shared_compute.sh install.sh start.sh
RUN ./install.sh
RUN ls

ENTRYPOINT ["start.sh"]

