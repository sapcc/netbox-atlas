FROM python:3.13

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt

RUN pip install --upgrade pip\
    && pip install poetry

# -------------------------------------------------------------------------------------
# install netbox
# -------------------------------------------------------------------------------------
ARG netbox_ver=v4.1.11

RUN git clone --single-branch --branch ${netbox_ver} https://github.com/netbox-community/netbox.git /opt/netbox/ && \
    cd /opt/netbox/ && \
    pip install -r /opt/netbox/requirements.txt

# -------------------------------------------------------------------------------------
# install netbox atlas plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /plugin
WORKDIR /plugin
COPY . /plugin
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

WORKDIR /opt/netbox/netbox/
