FROM netboxcommunity/netbox:v3.5.9

RUN pip install --upgrade pip\
    && pip install poetry

RUN mkdir -p /source
WORKDIR /source
COPY . /source
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

WORKDIR /opt/netbox/netbox/
