---
title: Sending messages directly
---

If you're sending messages directly, you'll need to:

* have a fixed IP address;
* configure a reverse PTR record;
* configure SPF and/or DKIM as explained in this document;
* it's also highly advisable to have your own IP block.

Your configuration would be as follows:

```shell script
ALLOWED_SENDER_DOMAINS=<your-domain>
```