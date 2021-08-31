
## Extending the image

### Using custom init scripts

If you need to add custom configuration to postfix or have it do something outside of the scope of this configuration,
simply add your scripts to `/docker-init.db/`: All files with the `.sh` extension will be executed automatically at the
end of the startup script.

E.g.: create a custom `Dockerfile` like this:

```shell script
FROM boky/postfix
LABEL maintainer="Jack Sparrow <jack.sparrow@theblackpearl.example.com>"
ADD Dockerfiles/additional-config.sh /docker-init.db/
```

Build it with docker, and your script will be automatically executed before Postfix starts.

Or -- alternately -- bind this folder in your docker config and put your scripts there. Useful if you need to add a
config to your postfix server or override configs created by the script.

For example, your script could contain something like this:

```shell script
#!/bin/sh
postconf -e "address_verify_negative_cache=yes"
```
