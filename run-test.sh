#!/bin/sh

base_dir=$(cd $(dirname $0) && pwd)

export BOOST_BUILD_PATH=$base_dir/build/boost-build

cd $base_dir
cd tests
cd hello-world
bjam toolset=gcc-android toolset=clang-android testing.launcher=$base_dir/tools/run_on_device.py "$@"
