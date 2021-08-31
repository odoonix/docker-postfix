
### Relaying messages through your Gmail account

Please note that Gmail does not support using your password with non-OAuth2 clients. You will need to either enable
[Less secure apps](https://support.google.com/accounts/answer/6010255?hl=en) in your account and assign an "app password",
or [configure postfix support for XOAuth2 authentication](#xoauth2_client_id-xoauth2_secret-xoauth2_initial_access_token-and-xoauth2_initial_refresh_token).
You'll also need to use (only) your email as the sender address.

If you follow the *less than secure* route, your configuration would be as follows:

```shell script
RELAYHOST=smtp.gmail.com:587
RELAYHOST_USERNAME=you@gmail.com
RELAYHOST_PASSWORD=your-gmail-app-password
ALLOWED_SENDER_DOMAINS=gmail.com
```

There's no need to configure DKIM or SPF, as Gmail will add these headers automatically.
