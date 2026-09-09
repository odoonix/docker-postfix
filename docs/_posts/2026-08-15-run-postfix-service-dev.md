---
layout: post
title: "How to run Postfix in a development environment"
date: 2026-08-14 10:00:00 +0330
categories: develop
cover_image: /assets/images/blog/odoo-roadmap-cover-sample.svg
---

## Overview

This project is designed to run a complete mail stack inside a containerized development environment. The main goal is to make it easy to test, debug, and evolve the email infrastructure without needing a full production deployment.

The system is built around Postfix, but it does not rely on a single monolithic process. Postfix itself is a multi-process service, and each process has a dedicated responsibility such as queue management, cleanup, delivery, or SMTP handling. To manage this runtime correctly, the environment uses `supervisord` as the central process manager.

From the container’s point of view, there is only one service to start: `supervisord`. Once it runs, it launches and supervises the remaining internal services, including `rsyslog`, `postfix`, `opendkim`, and the API layer.

---

## Project structure

The project is organized into a small set of directories, each with a specific purpose.

### .github

This folder contains the automation for CI/CD workflows. It is the place where GitHub Actions or related pipeline logic can be defined for testing, building, and validating the project.

### .vscode

This folder stores local editor configuration for development in VS Code. It usually contains:

- `launch.json` for running and debugging the application
- `settings.json` for editor-level configuration and workflow preferences

### api

This directory contains the Python service that exposes the mail system through an HTTP API. In practice, this acts as a mediator between the mail platform and external applications, allowing requests to send or process email-related operations through a REST interface.

### bin

This folder includes helper scripts used to start and manage the services inside the container:

- `api.sh`
- `opendkim.sh`
- `postfix.sh`
- `run.sh`

These scripts make the runtime setup cleaner and allow the system to start the correct process with the expected environment.

### config

This directory contains the initial configuration files loaded when the container starts. These are the base files that define service behavior. In a real deployment, these files can be moved to a host-managed configuration directory, but for development they are kept alongside the project and loaded into the image.

### Dockerfile

The root-level `Dockerfile` defines the complete runtime environment. It installs the dependencies, copies the configuration, configures the operating system environment, and prepares the container so that the mail stack can run as a single self-contained unit.

### docs

The documentation website is stored in this directory. It is built using Jekyll, which can generate static pages automatically from markdown content. This makes the documentation easier to publish and maintain as a website for developers and operators.

### tests

This folder contains validation files and checks used to exercise the system and verify expected behavior.

---

## Service startup flow

A mail platform does not work as a single process. Postfix is inherently composed of multiple workers and daemons, each responsible for handling a different stage of the mail lifecycle.

Because of that, the project uses `supervisord` to orchestrate the complete runtime. This is the single process that Docker starts, and from there the rest of the system is managed as child processes.

The definition of the runtime is stored in `configs/supervisord.conf`.

This file declares which services are started and how they are supervised. The first and most important service is `supervisord` itself, which runs in the foreground and manages the other programs.

The relevant configuration is:

```ini
[supervisord]
user            = root
nodaemon        = true
logfile         = /dev/null
logfile_maxbytes= 0
```

This tells the system which user should run the services and how the main supervisor process should behave. The configuration is intentionally minimal and designed for container execution.

---

## rsyslog service

One of the key requirements in a containerized mail environment is centralized log collection. `rsyslog` is responsible for receiving and processing log entries from the different services and forwarding them to the standard output streams so Docker can capture them cleanly.

The configuration is defined as follows:

```ini
[program:rsyslog]
command         = rsyslogd -n
autostart       = true
autorestart     = true
startsecs       = 2
stopwaitsecs    = 2
stdout_logfile  = /dev/stdout
stderr_logfile  = /dev/stderr
stdout_logfile_maxbytes = 0
stderr_logfile_maxbytes = 0
```

This pattern is important in container environments. Instead of writing logs to files inside the container, the service writes to `/dev/stdout` and `/dev/stderr`. That way, Docker can handle log collection and streaming without the need for extra log volume management.

---

## Postfix service

Postfix is the core component of the email system. It handles message submission, queueing, routing, and delivery. In this project, it is configured as a supervised service so it can run reliably in a container environment.

The Postfix service is configured like this:

```ini
[program:postfix]
command         = /usr/bin/postfix.sh
autostart       = true
autorestart     = false
directory       = /etc/postfix
startsecs       = 0
stdout_logfile  = /dev/stdout
stderr_logfile  = /dev/stderr
stdout_logfile_maxbytes = 0
stderr_logfile_maxbytes = 0
```

The most important configuration file is `main.cf`, which lives at `/etc/postfix/main.cf`. This file contains the primary mail transport settings, including how Postfix handles message submission, relay configuration, network behavior, and security-related options.

The project includes a base version at `configs/main.cf`, and that file is copied into the container at runtime as the initial system configuration. You can modify it to suit your local development needs or adjust your mail environment.

---

## OpenDKIM service

Security is a crucial concern in mail systems, especially when sending messages to external domains. OpenDKIM provides digital signing of outgoing email messages using the DKIM standard. This helps recipients verify that the message really came from the configured domain and was not altered in transit.

The service definition is:

```ini
[program:opendkim]
command         = /usr/bin/opendkim.sh
user            = opendkim
autostart       = true
autorestart     = true
startsecs       = 5
stopwaitsecs    = 5
stdout_logfile  = /dev/stdout
stderr_logfile  = /dev/stderr
stdout_logfile_maxbytes = 0
stderr_logfile_maxbytes = 0
```

This ensures that DKIM signing is run as a dedicated service, isolated from the rest of the stack, with its own user context and process lifecycle.

---

## API service

The API service acts as the integration layer between the mail infrastructure and other software systems. It exposes functionality through a REST interface so that other applications can interact with the mail system in a structured way instead of handling raw mail operations directly.

The service is configured as:

```ini
[program:api]
command         = /usr/bin/api.sh
directory       = /api
user            = root
autostart       = true
autorestart     = true
startsecs       = 5
stopwaitsecs    = 5
stdout_logfile  = /dev/stdout
stderr_logfile  = /dev/stderr
stdout_logfile_maxbytes = 0
stderr_logfile_maxbytes = 0
```

This makes the environment useful for both manual testing and automation. Developers can interact with the mail stack through either direct local commands or the API, depending on the use case.

---

## Building the Docker image

To build the container image, run:

```bash
docker build -t docker-postfix .
```

After the image is built, list local Docker images with:

```bash
docker images
```

The output should look similar to the following:

```text
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker-postfix      latest              123456789abc        2 minutes ago       500
```

Once the image is present, run the container with:

```bash
docker run --rm --name docker-postfix docker-postfix
```

The `--rm` flag ensures the container is removed automatically when it exits, which is useful during development and testing.

---

## Testing the mail system

To validate that the Postfix stack is running correctly, start the container first:

```bash
docker run --rm --name docker-postfix docker-postfix
```

Then, in a second terminal, open a shell inside the running container:

```bash
docker exec -it docker-postfix bash
```

To verify that Postfix is active, run:

```bash
postfix status
```

The expected output is similar to:

```text
postfix/postfix-script: the Postfix mail system is running: PID: 1234
```

Alternative checks can also be used:

```bash
ps aux | grep postfix
```

or:

```bash
postconf mail_version
```

These commands help confirm that the daemon is installed, initialized, and responding as expected.

---

## Sending a test email

Assuming the `mail` command is available, you can send a test message with:

```bash
echo "This is a test email from Docker Postfix." | mail -s "Docker Postfix Test" your-email@example.com
```

If no special mail transport configuration is set, the message will still be processed by Postfix but will likely bounce because the destination domain is not a valid external recipient in a development environment. That behavior is actually useful for testing: it confirms that the mail pipeline is active and that the system is attempting delivery.

The logs should look similar to the following:

```text
2026-08-15T03:20:51.897004+02:00 INFO    postfix/pickup[123]: DAFA431404AB: uid=0 from=<root@df0c5333e774>
2026-08-15T03:20:51.897204+02:00 INFO    postfix/cleanup[137]: DAFA431404AB: message-id=<20260815012051.DAFA431404AB@4926aec7f780>
2026-08-15T03:20:51.898028+02:00 INFO    postfix/qmgr[124]: DAFA431404AB: from=<root@df0c5333e774>, size=380, nrcpt=1 (queue active)
2026-08-15T03:20:51.940525+02:00 INFO    postfix/smtp[139]: DAFA431404AB: to=<your-email@example.com>, relay=none, delay=0.04, delays=0/0/0.04/0, dsn=5.1.0, status=bounced (Domain example.com does not accept mail (nullMX))
2026-08-15T03:20:51.942094+02:00 INFO    postfix/cleanup[137]: E5D2531404BD: message-id=<20260815012051.E5D2531404BD@4926aec7f780>
2026-08-15T03:20:51.943152+02:00 INFO    postfix/bounce[141]: DAFA431404AB: sender non-delivery notification: E5D2531404BD
2026-08-15T03:20:51.943424+02:00 INFO    postfix/qmgr[124]: E5D2531404BD: from=<>, size=2279, nrcpt=1 (queue active)
2026-08-15T03:20:51.943751+02:00 INFO    postfix/qmgr[124]: DAFA431404AB: removed
2026-08-15T03:20:52.072455+02:00 INFO    postfix/smtp[139]: E5D2531404BD: to=<root@df0c5333e774>, relay=none, delay=0.13, delays=0/0/0.13/0, dsn=5.4.4, status=bounced (Host or domain name not found. Name service error for name=df0c5333e774 type=AAAA: Host not found)
2026-08-15T03:20:52.073641+02:00 INFO    postfix/qmgr[124]: E5D2531404BD: removed
```

This is a valuable sign: the message entered the Postfix queue, was processed, and then bounced according to the local mail routing rules. In other words, the system is functioning, even if the destination domain is intentionally invalid for a test environment.

---

## Final notes

The goal of this setup is not to create a production-grade mail gateway immediately, but to provide a reliable local environment for testing email logic, validating routing behavior, and experimenting with Postfix-related integrations. By packaging the workflow in Docker and managing services with `supervisord`, the platform becomes straightforward to run, inspect, and evolve.

That structure is especially useful during development because it keeps the runtime deterministic and the debugging workflow simple. It also makes it easier to test domain configuration, queue handling, DKIM signing, and API interaction without needing to change the host operating system or install complex dependencies directly on the machine.

For a development environment, this is a very practical and scalable pattern: a single container, a controlled startup sequence, a few essential services, and clear visibility into system behavior through logs and local shell access.

