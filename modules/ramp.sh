#!/usr/bin/env bash

if [ -z "$1" ]
then
   echo "Missing repository URI as first parameter."
   echo "Usage: ramp.sh repository branch/tag"
   exit 1
fi

if [ -z "$2" ]
then
   echo "Missing branch or tag as second parameter."
   echo "Usage: ramp.sh repository branch/tag"
   exit 1
fi

mkdir tmp
cd tmp
git init
git remote add origin $1
git fetch
git checkout $2 -- ramp.yml
cp ramp.yml ..
cd ..
rm -rf tmp
