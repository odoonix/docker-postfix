---
layout: post
title: "Roadmap for Odoo"
date: 2026-05-30 10:00:00 +0330
categories: odoo roadmap
cover_image: /assets/images/blog/odoo-roadmap-cover-sample.svg
---

![Roadmap Cover Sample]({{ page.cover_image }})

In this new version, our goal is to evolve this project into an email gateway that is fully compatible with Odoo. All inbound and outbound email flows should be managed through this gateway, while Odoo remains the core business and user-experience layer.

## Vision

This system should operate as a middle layer between the internet and Odoo:

- Receive email through Postfix
- Process and validate messages in a Python/FastAPI service
- Deliver messages to Odoo through controlled APIs
- Route outbound Odoo email through the same gateway

The final objective is to let Odoo act not only as an ERP, but also as an operational webmail solution.

## Core Principles for the New Version

- Full compatibility with standard Odoo patterns
- Multi-tenant design based on domains and mailboxes
- Preserve raw RFC822 messages for audit, threading, and recovery
- Clear separation of concerns: Postfix for transport, Odoo for data and user workflows
- Docker-ready deployment for development and production

## Development Roadmap

### Phase 1: Core Odoo Integration

- Define Odoo models for Tenant, Mailbox, Message, and Thread
- Implement inbound APIs to register received email in Odoo
- Define baseline outbound routes from Odoo to the gateway

### Phase 2: Inbound Flow Completion

- Connect Postfix to FastAPI for raw message ingestion
- Extract headers, attachments, and threading metadata
- Map domain/mailbox rules to precise routing in Odoo

### Phase 3: Outbound Flow Completion

- Add queue-based outbound processing from Odoo
- Apply DKIM/SPF/DMARC for deliverability
- Implement error handling, retries, and sent/failed status tracking

### Phase 4: Webmail Experience in Odoo

- Provide Inbox/Sent/Thread views in the Odoo UI
- Add search, filters, reply, forward, and attachment workflows
- Deliver a modern webmail experience built on native Odoo capabilities

### Phase 5: Security, Monitoring, and Scale

- Enforce API authentication (JWT or API key) and signed requests
- Apply rate limiting at IP/domain/mailbox levels
- Add operational metrics and observability dashboards
- Prepare for high-scale domain and mailbox growth

## Outcome

By executing this roadmap, the project evolves from a Postfix management service into a complete Odoo email gateway. In this model, Odoo can serve both as an ERP platform and as a webmail interface, providing a unified environment for enterprise email operations.
