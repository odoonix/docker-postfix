---
title: Configuration options
---

### General options

* `TZ` = The timezone for the image, e.g. `Europe/Amsterdam`
* `FORCE_COLOR` = Set to `1` to force color output (otherwise auto-detected)
* `INBOUND_DEBUGGING` = Set to `1` to enable detailed debugging in the logs
* `ALLOWED_SENDER_DOMAINS` = domains which are allowed to send email via this server
* `ALLOW_EMPTY_SENDER_DOMAINS` = if value is set (i.e: `true`), `ALLOWED_SENDER_DOMAINS` can be unset
* `LOG_FORMAT` = Set your log format (JSON or plain)

#### Inbound debugging

Enable additional debugging for any connection coming from `POSTFIX_mynetworks`. Set to a non-empty string (usually `1`
or  `yes`) to enable debugging.

#### `ALLOWED_SENDER_DOMAINS` and `ALLOW_EMPTY_SENDER_DOMAINS`

Due to in-built spam protection in [Postfix](http://www.postfix.org/postconf.5.html#smtpd_relay_restrictions) you will
need to specify sender domains -- the domains you are using to send your emails from, otherwise Postfix will refuse to
start.

Example:

```shell script
docker run --rm \
  --name postfix \
  -e "ALLOWED_SENDER_DOMAINS=example.com example.org" \
  -p 1587:587 \
  viraweb123/gpost
```

If you want to set the restrictions on the recipient and not on the sender (anyone can send mails but just to a single domain
for instance), set `ALLOW_EMPTY_SENDER_DOMAINS` to a non-empty value (e.g. `true`) and `ALLOWED_SENDER_DOMAINS` to an empty
string. Then extend this image through custom scripts to configure Postfix further.

#### Log format

The image will by default output logs in human-readable (`plain`) format. If you are deploying the image to Kubernetes, it might
be worth chaging the output format to `json` as it's more easily parsable by tools such as [Prometheus](https://prometheus.io/).

To change the log format, set the (unsurprisingly named) variable `LOG_FORMAT=json`.

### Postfix-specific options

* `RELAYHOST` = Host that relays your messages
* `SASL_RELAYHOST` = (optional) Relay Host referenced in the `sasl_passwd` file. Defaults to the value of `RELAYHOST`
* `RELAYHOST_USERNAME` = An (optional) username for the relay server
* `RELAYHOST_PASSWORD` = An (optional) login password for the relay server
* `RELAYHOST_PASSWORD_FILE` = An (optional) file containing the login password for the relay server. Mutually exclusive with the previous option.
* `POSTFIX_smtp_tls_security_level` = Relay host TLS connection level
* `XOAUTH2_CLIENT_ID` = OAuth2 client id used when configured as a relayhost.
* `XOAUTH2_SECRET` = OAuth2 secret used when configured as a relayhost.
* `XOAUTH2_INITIAL_ACCESS_TOKEN` = Initial OAuth2 access token.
* `XOAUTH2_INITIAL_REFRESH_TOKEN` = Initial OAuth2 refresh token.
* `MASQUERADED_DOMAINS` = domains where you want to masquerade internal hosts
* `SMTP_HEADER_CHECKS`= Set to `1` to enable header checks of to a location of the file for header checks
* `POSTFIX_hostname` = Set the name of this postfix server
* `POSTFIX_mynetworks` = Allow sending mails only from specific networks ( default `127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16` )
* `POSTFIX_message_size_limit` = The maximum size of the messsage, in bytes, by default it's unlimited
* `POSTFIX_<any_postfix_setting>` = provide any additional postfix setting

#### `RELAYHOST`, `RELAYHOST_USERNAME` and `RELAYHOST_PASSWORD`

Postfix will try to deliver emails directly to the target server. If you are behind a firewall, or inside a corporation
you will most likely have a dedicated outgoing mail server. By setting this option, you will instruct postfix to relay
(hence the name) all incoming emails to the target server for actual delivery.

Example:

```shell script
docker run --rm --name postfix -e RELAYHOST=192.168.115.215 -p 1587:587 viraweb123/gpost
```

You may optionally specifiy a relay port, e.g.:

```shell script
docker run --rm --name postfix -e RELAYHOST=192.168.115.215:587 -p 1587:587 viraweb123/gpost
```

Or an IPv6 address, e.g.:

```shell script
docker run --rm --name postfix -e 'RELAYHOST=[2001:db8::1]:587' -p 1587:587 viraweb123/gpost
```

If your end server requires you to authenticate with username/password, add them also:

```shell script
docker run --rm --name postfix \
  -e RELAYHOST=mail.google.com \
  -e RELAYHOST_USERNAME=hello@gmail.com \
  -e RELAYHOST_PASSWORD=world \
  -p 1587:587 \
  viraweb123/gpost
```

#### `POSTFIX_smtp_tls_security_level`

Define relay host TLS connection level. See 
[smtp_tls_security_level](http://www.postfix.org/postconf.5.html#smtp_tls_security_level) 
for details. By default, the permissive level ("may") is used, which 
basically means "use TLS if available" and should be a sane default in most cases.

This level defines how the postfix will connect to your upstream server.

#### `XOAUTH2_CLIENT_ID`, `XOAUTH2_SECRET`, `XOAUTH2_INITIAL_ACCESS_TOKEN` and `XOAUTH2_INITIAL_REFRESH_TOKEN`

> Note: These parameters are used when `RELAYHOST` and `RELAYHOST_USERNAME` are provided.

These parameters allow you to configure a relayhost that requires (or recommends) 
the [XOAuth2 authentication method](https://github.com/tarickb/sasl-xoauth2) (e.g. GMail).

* `XOAUTH2_CLIENT_ID` and  `XOAUTH2_SECRET` are the [OAuth2 client credentials](#oauth2-client-credentials-gmail).
* `XOAUTH2_INITIAL_ACCESS_TOKEN` and `XOAUTH2_INITIAL_REFRESH_TOKEN` are the [initial access token and refresh tokens](#obtain-initial-access-token-gmail).
   These values are only  required to initialize the token file `/var/spool/postfix/xoauth2-tokens/$RELAYHOST_USERNAME`.

Example:

```shell script
docker run --rm --name pruebas-postfix \
    -e RELAYHOST="[smtp.gmail.com]:587" \
    -e RELAYHOST_USERNAME="<put.your.account>@gmail.com" \
    -e POSTFIX_smtp_tls_security_level="encrypt" \
    -e XOAUTH2_CLIENT_ID="<put_your_oauth2_client_id>" \
    -e XOAUTH2_SECRET="<put_your_oauth2_secret>" \
    -e ALLOW_EMPTY_SENDER_DOMAINS="true" \
    -e XOAUTH2_INITIAL_ACCESS_TOKEN="<put_your_acess_token>" \
    -e XOAUTH2_INITIAL_REFRESH_TOKEN="<put_your_refresh_token>" \
    viraweb123/gpost
```

Next sections describe how to obtain these values.

##### OAuth2 Client Credentials (GMail)

Visit the [Google API Console](https://console.developers.google.com/) to obtain OAuth 2 
credentials (a client ID and client secret) for an "Installed application" application type.

Save the client ID and secret and use them to initialize `XOAUTH2_CLIENT_ID` 
and  `XOAUTH2_SECRET` respectively.

We'll also need these credentials in the next step.

##### Obtain Initial Access Token (GMail)

Use the [Gmail OAuth2 developer tools](https://github.com/google/gmail-oauth2-tools/) 
to obtain an OAuth token by following the [Creating and Authorizing an OAuth Token](https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough#creating-and-authorizing-an-oauth-token) instructions.

Save the resulting tokens and use them to initialize `XOAUTH2_INITIAL_ACCESS_TOKEN` 
and `XOAUTH2_INITIAL_REFRESH_TOKEN`.

##### Debug XOAuth2 issues

If you have XOAuth2 authentication issues you can enable XOAuth2 debug message 
setting `XOAUTH2_SYSLOG_ON_FAILURE` to `"yes"` (default: `"no"`). If you need a more detailed
log trace about XOAuth2 you can set `XOAUTH2_FULL_TRACE` to `"yes"` (default: `"no"`).

#### `MASQUERADED_DOMAINS`

If you don't want outbound mails to expose hostnames, you can use this variable to enable Postfix's
[address masquerading](http://www.postfix.org/ADDRESS_REWRITING_README.html#masquerade). This can be used to do things
like rewrite `lorem@ipsum.example.com` to `lorem@example.com`.

Example:

```shell script
docker run --rm --name postfix \
  -e "ALLOWED_SENDER_DOMAINS=example.com example.org" \
  -e "MASQUERADED_DOMAINS=example.com" \
  -p 1587:587 \
  viraweb123/gpost
```

#### `SMTP_HEADER_CHECKS`

This image allows you to execute Postfix [header checks](http://www.postfix.org/header_checks.5.html). Header checks
allow you to execute a certain action when a certain MIME header is found. For example, header checks can be used
prevent attaching executable files to emails.

Header checks work by comparing each message header line to a pre-configured list of patterns. When a match is found the
corresponding action is executed. The default patterns that come with this image can be found in the `smtp_header_checks`
file. Feel free to override this file in any derived images or, alternately, provide your own in another directory.

Set `SMTP_HEADER_CHECKS` to type and location of the file to enable this feature. The sample file is uploaded into
`/etc/postfix/smtp_header_checks` in the image. As a convenience, setting `SMTP_HEADER_CHECKS=1` will set this to
`regexp:/etc/postfix/smtp_header_checks`.

Example:

```shell script
docker run --rm --name postfix \
  -e "SMTP_HEADER_CHECKS="regexp:/etc/postfix/smtp_header_checks" \
  -e "ALLOWED_SENDER_DOMAINS=example.com example.org" \
  -p 1587:587 \
  viraweb123/gpost
```

#### `POSTFIX_myhostname`

You may configure a specific hostname that the SMTP server will use to identify itself. If you don't do it,
the default Docker host name will be used. A lot of times, this will be just the container id (e.g. `f73792d540a5`)
which may make it difficult to track your emails in the log files. If you care about tracking at all,
I suggest you set this variable, e.g.:

```shell script
docker run --rm --name postfix \
  -e "POSTFIX_myhostname=postfix-docker" \
  -p 1587:587 \
  viraweb123/gpost
```

#### `POSTFIX_mynetworks`

This implementation is meant for private installations -- so that when you configure your services using _docker compose_
you can just plug it in. Precisely because of this reason and the prevent any issues with this postfix being inadvertently
exposed on the internet and then used for sending spam, the *default networks are reserved for private IPv4 IPs only*.

Most likely you won't need to change this. However, if you need to support IPv6 or strenghten the access further, you
can override this setting.

Example:

```shell script
docker run --rm --name postfix \
  -e "POSTFIX_mynetworks=10.1.2.0/24" \
  -p 1587:587 \
  viraweb123/gpost
```

#### `POSTFIX_message_size_limit`

Define the maximum size of the message, in bytes.
See more in [Postfix documentation](http://www.postfix.org/postconf.5.html#message_size_limit).

By default, this limit is set to 0 (zero), which means unlimited. Why would you want to set this? Well, this is
especially useful in relation with `RELAYHOST` setting. If your relay host has a message limit (and usually it does),
set it also here. This will help you "fail fast" -- your message will be rejected at the time of sending instead having
it stuck in the outbound queue indefinitely.

#### Overriding specific postfix settings

Any Postfix [configuration option](http://www.postfix.org/postconf.5.html) can be overriden using `POSTFIX_<name>`
environment variables, e.g. `POSTFIX_allow_mail_to_commands=alias,forward,include`. Specifying no content (empty
variable) will remove that variable from postfix config.

### DKIM / DomainKeys

**This image is equipped with support for DKIM.** If you want to use DKIM you will need to generate DKIM keys. These can
be either generated automatically, or you can supply them yourself.

The DKIM supports the following options:

* `DKIM_SELECTOR` = Override the default DKIM selector (by default "mail").
* `DKIM_AUTOGENERATE` = Set to non-empty value (e.g. `true` or `1`) to have
  the server auto-generate domain keys.
* `OPENDKIM_<any_dkim_setting>` = Provide any additional OpenDKIM setting.

#### Supplying your own DKIM keys

If you want to use your own DKIM keys, you'll need to create a folder for every domain you want to send through. You
will need to generate they key(s) with the `opendkim-genkey` command, e.g.

```shell script
mkdir -p /host/keys; cd /host/keys

for DOMAIN in example.com example.org; do
    # Generate a key with selector "mail"
    opendkim-genkey -b 2048 -h rsa-sha256 -r -v --subdomains -s mail -d $DOMAIN
    # Fixes https://github.com/linode/docs/pull/620
    sed -i 's/h=rsa-sha256/h=sha256/' mail.txt
    # Move to proper file
    mv mail.private $DOMAIN.private
    mv mail.txt $DOMAIN.txt
done
...
```

`opendkim-genkey` is usually in your favourite distribution provided by installing 
`opendkim-tools` or `opendkim-utils`.

Add the created `<domain>.txt` files to your DNS records. Afterwards, just mount 
`/etc/opendkim/keys` into your image and DKIM will be used automatically, e.g.:

```shell script
docker run --rm --name postfix \
    -e "ALLOWED_SENDER_DOMAINS=example.com example.org" \
    -v /host/keys:/etc/opendkim/keys \
    -p 1587:587 viraweb123/gpost
```

#### Auto-generating the DKIM selectors through the image

If you set the environment variable `DKIM_AUTOGENERATE` to a non-empty value (e.g. `true` or `1`) 
the image will automatically generate the keys.

**Be careful when using this option**. If you don't bind `/etc/opendkim/keys` to a persistent 
volume, you will get new keys every single time. You will need to take the generated public part 
of the key (the one in the `.txt` file) and copy it over to your DNS server manually.

#### Changing the DKIM selector

`mail` is the *default DKIM selector* and should be sufficient for most usages. If you wish to 
override the selector, set the environment variable `DKIM_SELECTOR`, e.g. `... -e DKIM_SELECTOR=postfix`. 
Note that the same DKIM selector will be applied to all found domains. To override a selector for a 
specific domain use the syntax `[<domain>=<selector>,...]`, e.g.:

```shell script
DKIM_SELECTOR=foo,example.org=postfix,example.com=blah
```

This means:

* use `postfix` for `example.org` domain
* use `blah` for `example.com` domain
* use `foo` if no domain matches

#### Overriding specific OpenDKIM settings

Any OpenDKIM [configuration option](http://opendkim.org/opendkim.conf.5.html) can be overriden using `OPENDKIM_<name>`
environment variables, e.g. `OPENDKIM_RequireSafeKeys=yes`. Specifying no content (empty variable) will remove that
variable from OpenDKIM config.

#### Verifying your DKIM setup

We strongly suggest using a service such as [dkimvalidator](https://dkimvalidator.com/) to make sure your keys are set up
properly and your DNS server is serving them with the correct records.


### Docker Secrets / Kubernetes secrets

As an alternative to passing sensitive information via environment variables, `_FILE` may be appended to some environment variables (see below), causing the initialization script to load the values for those variables from files present in the container. In particular, this can be used to load passwords from Docker secrets stored in `/run/secrets/<secret_name>` files. For example:

```
docker run --rm --name pruebas-postfix \
    -e RELAYHOST="[smtp.gmail.com]:587" \
    -e RELAYHOST_USERNAME="<put.your.account>@gmail.com" \
    -e POSTFIX_smtp_tls_security_level="encrypt" \
    -e XOAUTH2_CLIENT_ID_FILE="/run/secrets/xoauth2-client-id" \
    -e XOAUTH2_SECRET_FILE="/run/secrets/xoauth2-secret" \
    -e ALLOW_EMPTY_SENDER_DOMAINS="true" \
    -e XOAUTH2_INITIAL_ACCESS_TOKEN_FILE="/run/secrets/xoauth2-access-token" \
    -e XOAUTH2_INITIAL_REFRESH_TOKEN_FILE="/run/secrets/xoauth2-refresh-token" \
    viraweb123/gpost
```

Currently, this is only supported for `RELAYHOST_PASSWORD`, `XOAUTH2_CLIENT_ID`, `XOAUTH2_SECRET`, `XOAUTH2_INITIAL_ACCESS_TOKEN`
and `XOAUTH2_INITIAL_REFRESH_TOKEN`.



#### Careful

Getting all of this to work properly is not a small feat:

* Hosting providers will regularly block outgoing connections to port 25. On AWS, for example you can
  [fill out a form](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-port-25-throttle/) and request for
  port 25 to be unblocked.
* You'll most likely need to at least [set up SPF records](https://en.wikipedia.org/wiki/Sender_Policy_Framework) or
  [DKIM](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail).
* You'll need to set up [PTR](https://en.wikipedia.org/wiki/Reverse_DNS_lookup) records to prevent your emails going
  to spam.
* Microsoft is especially notorious for trashing emails from new IPs directly into spam. If you're having trouble
  delivering emails to `outlook.com` domains, you will need to enroll in their
  [Smart Network Data Service](https://sendersupport.olc.protection.outlook.com/snds/) programme. And to do this you
  will need to *be the owner of the netblock you're sending the emails from*.


