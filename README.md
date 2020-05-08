Conan Packaging Recipes
=======================

This repository contains several Conan recipes. It was developed with the
primary aim of packaging <https://github.com/grpc/grpc> but might grow in
scope in the future.

Prerequisites
-------------

These recipes have been tested on Debian GNU/Linux "bullseye" (currently in
testing phase) using the native GCC 9.3.0 toolchain and CMake 3.16.3 .

Conan 1.24.1 installed via pip3.

Building
--------

   ```shell
   $ cd recipes/abseil
   $ conan create . abseil/20200225.2@signbit/testing
   $ cd ../protoc_installer
   $ conan create . protobuf_compiler/3.11.4@signbit/testing
   $ cd ../grpc_plugin
   $ conan create . grpc_plugin/1.28.1@signbit/testing
   $ cd ../grpc
   $ conan create . grpc/1.28.1@signbit/testing
   ```

Feel free to substitute your own channel for "signbit/testing", just make
sure you adapt the test recipes.

Testing
-------

   ```shell
   $ cd tests
   # abseil
   $ mkdir abseil.build
   $ cd abseil.build
   $ conan install ../abseil
   $ cmake ../abseil
   $ cmake --build .
   $ ./test1
   dewey                                                                    
   huey            
   louie 
   # grpc
   $ cd ../
   $ mkdir greeter_example.build
   $ cd greeter_example.build
   $ conan install ../greeter_example
   $ cmake ../greeter_example
   $ cmake --build .
   $ ./greeter_server&
   Server listening on 0.0.0.0:50051
   $ ./greeter_client 
   Greeter received: Hello world
   # terminate the background process
   $ fg
   ^C
   ```

License
-------

These scripts have been heavily influenced by the original upstream sources:

   * <https://github.com/abseil/abseil-cpp/blob/master/conanfile.py> licensed under Apache-2.0
   * <https://github.com/bincrafters/conan-protoc_installer> licensed under MIT
   * <https://github.com/inexorgame/conan-grpc> licensed under MIT

As such, this work is licensed under the [MIT license](LICENSE.md).

NOTE: The Conan recipe license applies only to the files of this recipe,
which can be used to build the included packages. It does not in any way
apply or is related to the actual software being packaged.
