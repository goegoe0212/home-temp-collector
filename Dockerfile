ARG PYTHON_VERSION=3.13.4

FROM python:${PYTHON_VERSION}-slim-bookworm AS base
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/app
ENV PATH=/root/.local/bin:$PATH

RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && apt-get -y dist-upgrade

# 依存解決 (本番用: 通常依存 only)
FROM base AS prod-deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY ./app/pyproject.toml /usr/src/app/
RUN uv pip install --system --no-cache-dir --no-compile

# 開発用ステージ
FROM base AS develop
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    git

COPY ./app/pyproject.toml /usr/src/app/
RUN uv pip install --system --no-cache-dir --no-compile --group dev

COPY ./ /usr/src/app/


# 本番用ステージ (dev依存なし)
FROM base AS production
WORKDIR /usr/src/app

COPY --from=prod-deps /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=prod-deps /usr/local/bin /usr/local/bin

COPY ./ /usr/src/app/
# CMD [""]