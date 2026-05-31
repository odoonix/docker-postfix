---
title: Postfix Architecture Summary
permalink: /dev/postfix-architecture/
---

Postfix is built as a set of Linux processes. It runs multiple specialized programs, and these programs are controlled through command-line tools.

The processes communicate through different internal mechanisms, especially queues and service sockets.

Because of this design, operating Postfix requires a clear set of commands for controlling, reloading, inspecting, and troubleshooting the system.

The system we designed follows the same operational model: API actions eventually trigger Postfix command-line operations in a controlled way.

To use these commands correctly, we need to understand where each command fits and what responsibility it has.

This section explains the overall architecture in a practical and easy-to-follow way.

## Big Picture

Postfix is a modular mail system. Each process has one job, and queues connect those jobs.

Core idea:

- Receive mail safely
- Normalize and queue mail
- Deliver mail using the right transport
- Retry deferred mail without blocking normal flow

## How Mail Enters Postfix


The diagram below shows, at a high level, how messages move through the system.


![Postfix Architecture Diagram](/assets/images/dev/postfix-arch.drawio.svg)

There are two common entry paths:

- Network path: `smtpd` (SMTP) or `qmqpd` receives remote mail.
- Local path: `sendmail` + `postdrop` place mail into `maildrop`, then `pickup` processes it.

Both paths send messages to `cleanup`, which:

- Adds missing headers
- Rewrites addresses into normalized form
- Applies optional lightweight checks
- Stores message into the `incoming` queue

## How Mail Is Delivered

The queue manager `qmgr` is the heart of delivery.

![Postfix Mail Delivery](/assets/images/dev/how-postfix-deliver-message.drawio.svg)

It moves messages from `incoming` to `active` and selects delivery agents:

- `smtp` for remote SMTP servers
- `lmtp` for LMTP mailbox servers
- `local` for local UNIX/maildir delivery
- `virtual` for virtual domain mailbox delivery
- `pipe` for external commands/filters

Queue design is important:

- `active` queue is intentionally limited for memory safety under load.
- `deferred` queue holds temporarily undeliverable mail and retries later.

## Behind-the-Scenes Services

Postfix reliability and security depend on helper daemons:

- `master`: supervisor that starts/restarts Postfix services and enforces process limits.
- `anvil`: connection/request rate tracking and throttling support.
- `bounce`, `defer`, `trace`: status tracking for failed/delayed/success notifications.
- `flush`: moves selected deferred mail back for retry.
- `proxymap`: shared lookup-table access service.
- `scache`: outbound SMTP connection cache for faster repeated delivery.
- `tlsmgr` and `tlsproxy`: TLS state/session support and secure connection handling.
- `verify`: probe-based sender/recipient address verification.
- `postscreen`: pre-filter in front of `smtpd` to reduce bot/spam load.
- `showq`: queue listing backend used by queue inspection commands.
- `postlogd`: optional logging backend (file/stdout), useful in containers.

## Queue-Centric Model (Why It Matters)

Postfix is queue-driven, which gives:

- Better fault isolation
- Safe retries
- Back-pressure under heavy load
- Predictable behavior during component restarts

For gateway design, this means API actions should align with queue semantics, not direct mailbox mutation.

## Operational Command Family

Postfix includes administration commands (mostly `post*` tools), for example:

- `postfix`: start/stop/reload system
- `postconf`: inspect/update config
- `postmap`: build lookup tables
- `postqueue`: list/flush queue
- `postsuper`: queue maintenance
- `postalias`: aliases database maintenance

In this project, `postmap` and `postfix reload` are especially relevant because API updates regenerate lookup tables and then reload Postfix.

## Practical Mapping to This Project

For this repository's API-based management model:

- Map files are updated by API operations.
- `postmap` compiles lookup data.
- Postfix is reloaded to apply changes.
- Delivery still follows Postfix queue and daemon flow.

So the API is a control plane, while Postfix remains the mail transport data plane.

## Short Mental Model

Think of Postfix as:

- Ingress services -> `cleanup` -> `incoming` queue
- `qmgr` -> delivery agents (`smtp`, `lmtp`, `local`, `virtual`, `pipe`)
- Retry/status/security handled by dedicated helper daemons

This separation is the reason Postfix is stable at scale and suitable as an email gateway core.
