#!/usr/bin/env sh

if [ $# -eq 0 ]; then
  echo "No ubuntu build versions supplied"
  echo "example usage: $0 latest jammy"
  exit 1
fi

# Authenticate to push images
docker login

# build, tag, and push alpine versions supplied as script arguments
base_repo=viraweb123/gpost
for ubuntu_version in "$@"; do
  docker build -t "$base_repo" --build-arg=BASE_IMAGE="ubuntu:$ubuntu_version" .
done
