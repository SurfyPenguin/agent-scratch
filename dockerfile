FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev --group gemini

COPY . .
RUN uv sync --frozen --no-dev --group gemini

# Same sandboxing: non-root user, and a workspace folder that's
# the ONLY thing the agent can read/write.
RUN useradd -m agent \
    && mkdir /workspace \
    && chown -R agent:agent /app /workspace
USER agent

ENV PATH="/app/.venv/bin:$PATH" \
    PROJECT_ROOT=/workspace

WORKDIR /workspace
ENTRYPOINT ["python", "/app/main.py"]