FROM python:3.13
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
COPY ./pyproject.toml /src/pyproject.toml
COPY ./uv.lock /src/uv.lock
COPY ./.python-version /src/.python-version
WORKDIR src
RUN uv sync --group prod
COPY ./src /src