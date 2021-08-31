# Updates

## v3.0.0

There's a potentially breaking change introduced now in `v3.0.0`: Oracle has changed the license of BerkleyDB to AGPL-3.0, making it
unsuitable to link to packages with GPL-incompatible licenses. 
As a result Alpine (on which this image is based)
[has deprecated BerkleyDB throughout the image](https://wiki.alpinelinux.org/wiki/Release_Notes_for_Alpine_3.13.0#Deprecation_of_Berkeley_DB_.28BDB.29):

> Support for Postfix `hash` and `btree` databases has been removed. `lmdb` is the recommended replacement. Before upgrading, all tables in
> `/etc/postfix/main.cf` using `hash` and `btree` must be changed to a supported alternative. See the
> [Postfix lookup table documentation](http://www.postfix.org/DATABASE_README.html) for more information.

While this should not affect most of the users (`/etc/postfix/main.cf` is managed by this image), there might be use cases where
people have their own configuration which relies on `hash` and `btree` databases. 
To avoid braking live systems, the version of this image has been updated to `v3.0.0.`.
