#!/usr/bin/env bash

mkdir tmp
cd tmp
git init
git remote add origin https://github.com/RedisGears/RedisGears.git
git fetch
git checkout origin/$1 ramp.yml
cp ramp.yml ..
cd ..
rm -rf tmp
