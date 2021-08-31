#!/usr/bin/env bash
set -e
mkdir -p fixtures

for i in `find -maxdepth 1 -type f -name test\*yml | sort`; do
    echo "☆☆☆☆☆☆☆☆☆☆ $i ☆☆☆☆☆☆☆☆☆☆"
    helm template -f $i --dry-run mail > fixtures/demo.yaml
    docker run -it -v `pwd`/fixtures:/fixtures garethr/kubeval fixtures/demo.yaml
done
