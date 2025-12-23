# ================================
# Stage 1: Build the wheel
# ================================
FROM python:3.12-slim-bookworm AS builder

# OS security updates (builder)
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Upgrade pip and install build tools
RUN python -m pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir build setuptools wheel

# Copy project metadata and source
COPY pyproject.toml .
COPY . .

# Build wheel into /app/dist
RUN python -m build


# ================================
# Stage 2: Runtime image
# ================================
FROM python:3.12-slim-bookworm

# OS security updates (runtime)
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Copy built wheel from builder stage
COPY --from=builder /app/dist/*.whl .

# Upgrade pip (to pick up pip CVE fixes) and install the wheel
RUN python -m pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir *.whl \
    && rm -f *.whl

# Drop privileges
USER appuser

# Default entrypoint for the updater module
ENTRYPOINT ["python", "-m", "trident.updater"]
