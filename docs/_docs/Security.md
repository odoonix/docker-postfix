-----
title: Security
----


 Postfix will run the master proces as `root`, because that's how it's
designed. Subprocesses will run under the `postfix` account which will
use `UID:GID` of `100:101`. `opendkim` will run under account `102:103`.
