---
title: REST API Overview for Postfix Management
permalink: /dev/api-rest-overview/
---

# REST API Overview for Postfix Management

This document explains the API implemented in the FastAPI application and describes what each section is responsible for.

Main implementation file:

- api/fastapi_app.py

## 1. Purpose of This API

This API provides an external control layer for Postfix-related data and operations.

It allows an external system to:

- Manage allowed sender domains
- Manage virtual alias maps
- Manage virtual mailbox maps
- Generate and remove DKIM keys
- Read Prometheus metrics

In short, it exposes Postfix management functions through HTTP endpoints.

## 2. Application Bootstrap and Imports

The application is initialized with FastAPI and imports internal modules for each functional area.

Main imported modules:

- allowed_senders: domain allow-list management
- virtual_alias_maps: alias mapping management
- virtual_mailbox_maps: mailbox mapping management
- opendkim: DKIM key generation and removal
- metrics: Prometheus decorators and metrics output

## 3. Health and Basic Test Endpoints

### GET /

- Returns a simple hello response.
- Useful as a very basic connectivity check.

### GET /items/{item_id}

- Returns sample path and query values.
- Acts as a demo/test endpoint and not a core mail-management endpoint.

## 4. Allowed Senders Section

These endpoints manage sender domain policies.

### GET /allowed_senders

- Reads all configured allowed sender domains.

### POST /allowed_senders

- Adds a new allowed sender rule.
- Expected model fields:
  - domain
  - allowed

### DELETE /allowed_senders

- Removes an allowed sender rule.

Operational behavior behind the scenes:

- Writes updated records to the relevant map file
- Rebuilds the Postfix map using postmap
- Reloads Postfix

## 5. Virtual Alias Maps Section

These endpoints manage alias forwarding rules.

### GET /virtual_alias_maps

- Returns current alias mappings.

### POST /virtual_alias_maps

- Adds an alias mapping.
- Expected model fields:
  - source
  - destination

### DELETE /virtual_alias_maps

- Removes an alias mapping.

Operational behavior:

- Updates map file
- Runs postmap
- Reloads Postfix

## 6. Virtual Mailbox Maps Section

These endpoints manage mailbox location mappings.

### GET /virtual_mailbox_maps

- Returns current mailbox mappings.

### POST /virtual_mailbox_maps

- Adds a mailbox mapping.
- Expected model fields:
  - mailbox
  - location

### DELETE /virtual_mailbox_maps

- Removes a mailbox mapping.

Operational behavior:

- Updates map file
- Runs postmap
- Reloads Postfix

## 7. DKIM Section

These endpoints manage DKIM keys through OpenDKIM integration.

### GET /dkim/{name}

- Reads existing DKIM public value for a domain.
- If key does not exist, it generates a new key and returns the public data.

### POST /dkim/{name}

- Triggers DKIM generation (internally uses the same logic as GET).

### DELETE /opendkim/{name}

- Removes both public and private DKIM key files for the domain.

## 8. Metrics Section

### GET /metrics

- Returns Prometheus-formatted metrics.
- Used for monitoring request counts and other exposed metrics.

## 9. Virtual Mailbox Domains (Currently Disabled)

The section for virtual mailbox domains exists in code but is commented out in the API file.

Current status:

- Endpoints are not active
- Module is present but endpoint registration is disabled

## 10. How Sections Work Together

Write operations in sender/alias/mailbox sections generally follow this flow:

1. Receive HTTP request and validate input model.
2. Load current records from map file.
3. Add or remove the requested item.
4. Save the updated list to file.
5. Rebuild Postfix map.
6. Reload Postfix.

This design keeps the API lightweight and focused on Postfix operational control.

## 11. Notes for Integration Teams

Important integration observations:

- Authentication and authorization are not enforced in these endpoints by default.
- Response payloads are simple and operationally focused.
- This API is suitable as a management gateway layer for an external control system.

For production use, add:

- API authentication
- Input hardening and validation rules
- Error normalization and structured response models
- Audit logging and rate limiting
