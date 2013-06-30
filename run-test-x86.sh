#!/bin/sh

base_dir=$(cd $(dirname $0) && pwd)

BOOST_BUILD_PATH=$base_dir/build/boost-build

cd $base_dir
cd tests
cd hello-world
HOME=$BOOST_BUILD_PATH bjam toolset=gcc-android_x86 toolset=clang-android_x86 testing.launcher=$base_dir/tools/run_on_device.py "$@"
