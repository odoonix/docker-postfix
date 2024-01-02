# ============================ BUILD SASL XOAUTH2 ============================
FROM ubuntu:jammy as build

ARG SASL_XOAUTH2_REPO_URL=https://github.com/tarickb/sasl-xoauth2.git
ARG SASL_XOAUTH2_GIT_REF=release-0.10

RUN true && \
	export DEBIAN_FRONTEND=noninteractive && \
	echo "Europe/Berlin" > /etc/timezone && \
	apt-get update -y -qq && \
	apt-get install -y \
		git \
		build-essential \
		cmake \
		pkg-config \
		libcurl4-openssl-dev \
		libssl-dev \
		libjsoncpp-dev \
		libsasl2-dev
RUN git clone --depth 1 --branch ${SASL_XOAUTH2_GIT_REF} ${SASL_XOAUTH2_REPO_URL} /sasl-xoauth2
RUN true && \
	cd /sasl-xoauth2 && \
	mkdir build && \
	cd build && \
	cmake -DCMAKE_INSTALL_PREFIX=/ .. && \
	make

# ============================ BUILD SASL XOAUTH2 ============================
FROM ubuntu:jammy
LABEL maintainer="ViraWeb123 - https://github.com/viraweb123/gpost/"

# Install supervisor, postfix
# Install postfix first to get the first account (101)
# Install opendkim second to get the second account (102)
RUN true && \
	export DEBIAN_FRONTEND=noninteractive && \
	echo "Europe/Berlin" > /etc/timezone && \
	apt-get update -y -q && \
	apt-get install -y \
		libsasl2-modules \
		postfix \
		postfix-pgsql \
		postfix-lmdb \
		opendkim \
		opendkim-tools \
		ca-certificates \
		tzdata \
		supervisor \
		rsyslog \
		bash \
		curl \
		libcurl4 \
		netcat \
		postgresql-client \
		uvicorn \
		python3 \
		python3-pydantic \
		python3-starlette \
		python3-uvicorn \
		python3-fastapi && \
	cp -r /etc/postfix /etc/postfix.template && \
	apt-get clean && \
	find /var/log -type f -delete

# Copy SASL-XOAUTH2 plugin
COPY --from=build /sasl-xoauth2/build/src/libsasl-xoauth2.so /usr/lib/sasl2/

# Set up configuration
COPY ./configs/supervisord.conf /etc/supervisord.conf
COPY ./configs/rsyslog*.conf /etc/
COPY ./configs/opendkim.conf /etc/opendkim/opendkim.conf
COPY ./configs/smtp_header_checks /etc/postfix/smtp_header_checks

# Applications (CLI)
COPY ./bin/*.sh /usr/bin/

# API app
RUN mkdir /api
COPY api /api

RUN chmod +x \
	/usr/bin/run.sh \
	/usr/bin/opendkim.sh \
	/usr/bin/postfix.sh \
	/usr/bin/api.sh

# Set up volumes
VOLUME [ \
	"/var/spool/postfix", \
	"/etc/postfix", \
	"/etc/opendkim/keys" ]

# Run supervisord
USER root
WORKDIR /tmp

# Check if the postfix main service is live. It sends a EHLO command and
# gets the result as health check.
HEALTHCHECK  \
	--interval=30s \
	--timeout=5s \
	--start-period=10s \
	--retries=3 \
	CMD printf "EHLO healthcheck\n" | nc 127.0.0.1 587 | grep -qE "^220.*ESMTP Postfix"

EXPOSE 587
EXPOSE 80
CMD [ "/bin/sh", "-c", "/usr/bin/run.sh" ]