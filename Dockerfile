# Stage 1: Build the wheel
FROM python:3.12-slim AS builder

RUN useradd -m appuser
WORKDIR /app

RUN pip install --no-cache-dir build

COPY pyproject.toml .
COPY . .

RUN python -m build


# Stage 2: Runtime image
FROM python:3.12-slim

# Create the same user here
RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl

USER appuser

ENTRYPOINT ["python", "-m", "trident.updater"]
