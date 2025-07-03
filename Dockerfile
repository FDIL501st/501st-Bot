# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# debian based python image
FROM python:3.12-slim-bookworm AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Copy the source code into /app
COPY . .


# add app/tmp as something the appuser can read and write from
# as we use that folder to write and read files used by the app

# Change ownership of the working directory to appuser
RUN chown -R appuser /app/tmp

# Grant read and write permissions to the appuser for the working directory
RUN chmod -R 755 /app/tmp
# need read write permissions as application writes and read files within /app (program code)


# Expose the port that the application listens on.
# EXPOSE 8000
# No need to expose a port as we don't need networking

# Switch to the non-privileged user to run the application.
USER appuser

# Run the application.
CMD ["python3", "."]
