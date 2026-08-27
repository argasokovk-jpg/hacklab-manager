FROM hacklab/lab:latest

USER root

RUN apt-get update && apt-get install -y \
    nmap \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Даём права на nmap без пароля
RUN echo "student ALL=(ALL) NOPASSWD: /usr/bin/nmap" >> /etc/sudoers

USER student
WORKDIR /home/student
