#!/bin/sh

base_dir=$(cd $(dirname $0) && pwd)
toolset=arm-linux-androideabi-4.6
toolset_x86=x86-4.6
llvm=3.2

mkdir -p build
$ANDROID_NDK_ROOT/build/tools/make-standalone-toolchain.sh --platform="android-9" --install-dir="$base_dir/build/tools" --toolchain=$toolset --llvm-version=$llvm
$ANDROID_NDK_ROOT/build/tools/make-standalone-toolchain.sh --platform="android-9" --install-dir="$base_dir/build/tools_x86" --toolchain=$toolset_x86 --llvm-version=$llvm

cat > $base_dir/build/boost-build/user-config.jam << _END_
using gcc : android : $base_dir/build/tools/bin/arm-linux-androideabi-g++ ;
using clang : android : $base_dir/build/tools/bin/clang++ ;
using gcc : android_x86 : $base_dir/build/tools_x86/bin/i686-linux-android-g++ ;
using clang : android_x86 : $base_dir/build/tools_x86/bin/clang++ ;
_END_
