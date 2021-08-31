
### Relaying messages through Amazon's SES

If your application runs in Amazon Elastic Compute Cloud (Amazon EC2), you can use Amazon SES to send up to 62,000 emails
every month at no additional charge. You'll need an AWS account and SMTP credentials. The SMTP settings are available
on the SES page. For example, for `eu-central-1`:

* see the [SES page for details](https://eu-central-1.console.aws.amazon.com/ses/home?region=eu-central-1#smtp-settings),
* [create the user credentials](https://console.aws.amazon.com/iam/home?#s=SESHomeV4/eu-central-1)

**Make sure you write the user credentials down, as you will only see them once.**

By default, messages that you send through Amazon SES use a subdomain of `amazonses.com` as the `MAIL FROM` domain. See
[Amazon's documentation](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/mail-from.html) on how the domain can
be configured.

Your configuration would be as follows (example data):

```shell script
RELAYHOST=email-smtp.eu-central-1.amazonaws.com:587
RELAYHOST_USERNAME=AKIAGHEVSQTOOSQBCSWQ
RELAYHOST_PASSWORD=BK+kjsdfliWELIhEFnlkjf/jwlfkEFN/kDj89Ufj/AAc
ALLOWED_SENDER_DOMAINS=<your-domain>
```

You will need to configure DKIM and SPF for your domain as well.
