# Odoo Multi-Tenant Mail Platform Architecture

## Goal

Build a multi-tenant email platform integrated with Odoo 19.

The platform must allow:

* Receiving emails for multiple domains.
* Sending emails from Odoo users.
* Managing mailboxes directly inside Odoo.
* Supporting thousands of domains and mailboxes.
* Providing Gmail-like user experience within Odoo.
* Avoiding IMAP storage and mailbox management outside Odoo.
* Using Postfix as the SMTP gateway.
* Using a dedicated Mail Receiver Service as the integration layer.


# High-Level Architecture

```text
Internet
    |
    v
Postfix
    |
    v
Mail Receiver Service (FastAPI)
    |
    v
Odoo REST API
    |
    v
PostgreSQL

Attachments
    |
    +--> MinIO / S3
```

Responsibilities:

| Component       | Responsibility                           |
| --------------- | ---------------------------------------- |
| Postfix         | SMTP receiving and sending               |
| FastAPI Service | Email parsing, validation, routing       |
| Odoo            | Mailbox management, users, UI, threading |
| PostgreSQL      | Metadata storage                         |
| MinIO/S3        | Attachment storage                       |

# Design Principles

1. Odoo is the source of truth.
2. Postfix must not store user mailboxes.
3. Postfix is only an SMTP transport layer.
4. Mailboxes exist only inside Odoo.
5. Attachments must not be stored inside PostgreSQL.
6. Multi-tenancy must be domain-based.
7. All inbound mail must pass through FastAPI.
8. All outbound mail must pass through Postfix.
9. Email threading must be preserved.
10. RFC822 raw messages must be preserved.

# Multi-Tenant Design

A tenant represents multi email domain.

Examples:

```text
company-a.com
company-b.com
company-c.com
```

Each tenant can have:

* Multiple domain
* Multiple users
* Multiple mailboxes
* Multiple aliases
* Multiple inbound routes

Tenant isolation is mandatory.

No mailbox can access another tenant's emails.

# Odoo Models

## mail.tenant

Fields:

```python
name
domain
company_id
active
```

Example:

```text
Company A
company-a.com
```

## mail.mailbox

Fields:

```python
name
email
tenant_id
user_id
active
```

Example:

```text
sales@company-a.com
support@company-a.com
```

## mail.message

Fields:

```python
message_id
subject
body_html
body_text

sender
sender_name

recipient_to
recipient_cc
recipient_bcc

mailbox_id
tenant_id

thread_id

received_at
sent_at

direction

raw_email

state
```

Direction values:

```text
inbound
outbound
```

State values:

```text
received
queued
sent
failed
rejected
```

## mail.thread

Fields:

```python
thread_key
subject
mailbox_id
tenant_id
```

Used for conversation grouping.

## mail.attachment

Fields:

```python
name
storage_key
mime_type
size
message_id
```

Attachment binary content must never be stored in PostgreSQL.

# Email Receiving Flow

## Step 1

External sender sends email:

```text
john@gmail.com
    ->
sales@company-a.com
```

## Step 2

Postfix receives email.

Example:

```text
Port 25
SMTP
```

## Step 3

Postfix forwards email to FastAPI service.

Possible methods:

* Pipe transport
* Local SMTP relay
* LMTP

Preferred:

```text
Pipe Transport
```

## Step 4

FastAPI receives raw RFC822 email.

Store:

```python
raw_email
```

without modification.

## Step 5

Parse email using Python email package.

Extract:

```python
Message-ID
Subject
From
To
CC
Date
Attachments
References
In-Reply-To
HTML Body
Text Body
```

## Step 6

Resolve tenant.

Example:

```text
sales@company-a.com
```

Domain:

```text
company-a.com
```

Find:

```python
mail.tenant
```

## Step 7

Resolve mailbox.

Example:

```text
sales@company-a.com
```

Find:

```python
mail.mailbox
```

## Step 8

Upload attachments.

Target:

```text
MinIO
or
S3
```

Store metadata only.

## Step 9

Call Odoo API.

Example:

```http
POST /api/mail/inbound
```

## Step 10

Odoo stores email.

Create:

```python
mail.message
```

record.

# Threading

Use RFC822 standards.

Primary keys:

```text
Message-ID
References
In-Reply-To
```

Thread matching order:

1. In-Reply-To
2. References
3. Subject normalization

Never rely only on subject.

# Email Sending Flow

## Step 1

User sends email from Odoo.

## Step 2

Create outbound mail.message.

State:

```text
queued
```

## Step 3

Worker processes queue.

## Step 4

Generate RFC822 message.

Include:

```text
Message-ID
References
DKIM headers
MIME
Attachments
```

## Step 5

Submit to Postfix.

Protocol:

```text
SMTP Submission
Port 587
```

Authentication required.

## Step 6

Postfix delivers email.

## Step 7

Update state:

```text
sent
```

or

```text
failed
```

# DNS Requirements

For every tenant:

Required:

```text
MX
SPF
DKIM
DMARC
```

Example:

company-a.com

```dns
MX
TXT SPF
TXT DKIM
TXT DMARC
```

# Security Requirements

Must implement:

## Authentication

JWT

or

API Keys

## Webhook Signature

All inbound requests must be signed.

## Rate Limiting

Per:

* Domain
* Mailbox
* IP

## Antivirus

Support:

```text
ClamAV
```

before storing attachments.

## Spam Detection

Support:

```text
Rspamd
```

or

```text
SpamAssassin
```

before delivery.

# FastAPI Service Responsibilities

Must:

* Receive emails
* Parse MIME
* Validate recipients
* Validate tenant
* Upload attachments
* Call Odoo APIs
* Retry failures
* Log all events

Must not:

* Store mailbox state
* Manage users
* Manage threads

# Odoo API Requirements

Inbound:

```http
POST /api/mail/inbound
```

Outbound:

```http
POST /api/mail/send
```

Mailbox listing:

```http
GET /api/mail/messages
```

Thread view:

```http
GET /api/mail/thread/{id}
```

# Scalability

Design for:

```text
1000+ domains
10000+ mailboxes
Millions of messages
```

Requirements:

* Queue-based processing
* Background workers
* Attachment object storage
* Database indexing
* Message archiving

# Recommended Technologies

SMTP Gateway:

```text
Postfix
```

API Layer:

```text
FastAPI
```

Queue:

```text
Redis + RQ
```

or

```text
RabbitMQ
```

Object Storage:

```text
MinIO
```

Database:

```text
PostgreSQL
```

Application:

```text
Odoo 19
```


# Development Order

Phase 1

* Tenant model
* Mailbox model
* Inbound API

Phase 2

* FastAPI Receiver
* Postfix Integration

Phase 3

* Attachments
* Threading

Phase 4

* Outbound Queue

Phase 5

* DKIM/SPF/DMARC

Phase 6

* Spam Filtering

Phase 7

* Monitoring and Metrics

Phase 8

* Horizontal Scaling

