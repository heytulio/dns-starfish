
FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    bind9 \
    bind9utils \
    bind9-doc \
    dnsutils \
    && apt-get clean

RUN mkdir -p /etc/bind
RUN chown -R bind:bind /etc/bind && chmod -R 755 /etc/bind
COPY ./bind /etc/bind/

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["named", "-g"]
