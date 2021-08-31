
### Relaying messages through Google Apps account

Google Apps allows third-party services to use Google's SMTP servers without much hassle. If you have a static IP, you
can configure Gmail to accept your messages. You can then send email *from any address within your domain*.

You need to enable the [SMTP relay service](https://support.google.com/a/answer/2956491?hl=en):

* Go to Google [Admin /Apps / G Suite / Gmail /Advanced settings](https://admin.google.com/AdminHome?hl=en_GB#ServiceSettings/service=email&subtab=filters).
* Find the **Routing / SMTP relay service**
* Click **Add another** button that pops up when you hover over the line
* Enter the name and your server's external IP as shown in the picture below:
  * **Allowed senders:** Only registered Apps users in my domains
  * Select **Only accept mail from specified IP Addresses**
  * Click **Add IP RANGE** and add your external IP
  * Make sure **Require SMTP Authentication** is **NOT** selected
  * You *may* select **Require TLS encryption**

![Add setting SMTP relay service](GApps-SMTP-config.png)

Your configuration would be as follows:

```shell script
RELAYHOST=smtp-relay.gmail.com:587
ALLOWED_SENDER_DOMAINS=<your-domain>
```

There's no need to configure DKIM or SPF, as Gmail will add these headers automatically.
