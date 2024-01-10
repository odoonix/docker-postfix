---
title: A Postrix service to relay to Odoo
---


Postfix host ("postfix null client") for your Docker containers. Based on Alpine Linux.


This image allows you to run POSTFIX internally inside your docker cloud/swarm installation to 
centralise outgoing email sending. 
The embedded postfix enables you to either _send messages directly_ or _relay them to your 
company's main server_.

This is a _server side_ POSTFIX image, geared towards emails that need to be sent from your applications. 
That's why this postfix configuration does not support username / password login or similar client-side security features.

**IF YOU WANT TO SET UP AND MANAGE A POSTFIX INSTALLATION FOR END USERS, THIS IMAGE IS NOT FOR YOU.** 
If you need it to manage your application's outgoing queue, read on.

## TL;DR

To run the container, do the following:

```shell script
docker run \
	--rm \
	--name postfix \
	-e "ALLOWED_SENDER_DOMAINS=example.com" \
	-p 1587:587 viraweb123/gpost
```


You can now send emails by using `localhost:1587` (on Docker) as your SMTP server address. 
Note that if you haven't configured your domain to allow sending from this IP/server/nameblock, 
**your emails will most likely be regarded as spam.**

All standard caveats of configuring the SMTP server apply:

* **MAKE SURE YOUR OUTGOING PORT 25 IS NOT BLOCKED.**
  * Most ISPs block outgoing connections to port 25 and several companies (e.g.
    [NoIP](https://www.noip.com/blog/2013/03/26/my-isp-blocks-smtp-port-25-can-i-still-host-a-mail-server/),
    [Dynu](https://www.dynu.com/en-US/Blog/Article?Article=How-to-host-email-server-if-ISP-blocks-port-25)) offer
    workarounds.
  * Hosting centers also tend to block port 25, which can be unblocked per request, see below for AWS hosting.
* You'll most likely need to at least [set up SPF records](https://en.wikipedia.org/wiki/Sender_Policy_Framework) (see also [openspf](http://www.open-spf.org/)) and/or
  [DKIM](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail).
* If using DKIM ([below](#dkim--domainkeys)), make sure to add DKIM keys to your domain's DNS entries.
* You'll most likely need to set up [PTR](https://en.wikipedia.org/wiki/Reverse_DNS_lookup) records as well to prevent your
  mails going to spam.

If you don't know what any of the above means, get some help. Google is your friend. 
It's also worth noting that it's pretty difficult to host a SMTP server on a dynamic IP address.

**Please note that the image uses the submission (587) port by default**. Port 25 is not exposed on purpose, as it's regularly blocked
by ISPs, already occupied by other services, and in general should only be used for server-to-server communication.

## Architectures

Available for all your favourite architectures. Run in your server cluster. Run it on your Raspberry Pi 4. Run it 
on your acient Pentium or an old Beaglebone. 
The following architectures are supported: 

- `linux/386`
- `linux/amd64`
- `linux/arm/v6`
- `linux/arm/v7`
- `linux/arm64`
- `linux/ppc64le`



