# Use httpd from Apache as the base since it is setup already
# to run without systemd and to log to stdout. It is built on
# a Debian base.
FROM httpd:2.4
LABEL name="LIGO gwdatafind-server application" \
      maintainer="duncan.meacher@ligo.org" \
      date="20201016"

# Install Python3, the dev and venv module, and gcc.
RUN apt-get update \
    && apt-get install -y \
        python3 \
        python3-dev \
        python3-venv \
        gcc

# Create a Python3 virtual environment and install 
# gunicorn, supervisor, and gwdatafind-server from pip.
RUN python3 -m venv /opt/gwdatafind-server \
    && . /opt/gwdatafind-server/bin/activate \
    && pip install --upgrade pip \
    && pip install wheel \
    && pip install gunicorn \
    && pip install supervisor \
    && pip install gwdatafind-server

COPY docker/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY docker/supervisord.conf /usr/local/etc/supervisord.conf
COPY config/gunicorn.conf /usr/local/apache2/conf.d/gwdatafind-server.conf
COPY config/gwdatafind-server.ini /etc/gwdatafind-server.ini

# Easiest to set this as the working directory for gunicorn, but
# not strictly necessary.
WORKDIR /opt/gwdatafind-server

# Run supervisord when this image starts as a container.
ENTRYPOINT ["/opt/gwdatafind-server/bin/supervisord", "-c", "/usr/local/etc/supervisord.conf"]
