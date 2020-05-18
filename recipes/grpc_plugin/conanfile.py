import os
from conans import ConanFile, CMake, tools


class GrpcConan(ConanFile):
    name = "grpc_plugin"
    version = "1.28.1"
    description = "The C based gRPC (C++, Python, Ruby, Objective-C, PHP, C#)"
    homepage = "https://grpc.io"
    url = "https://github.com/0x8000-0000/conan-recipes/"
    license = "Apache-2.0"
    author = "Florin Iucha <florin@signbit.net>"
    topics = ("conan", "grpc", "rpc")
    settings = "os_build", "arch_build", "compiler", "arch"
    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        self.requires("zlib/1.2.11")
        self.requires("gflags/2.2.2")
        self.requires("openssl/1.1.1e")
        self.requires("libuv/1.34.2")
        self.requires("c-ares/1.15.0")
        self.requires("protobuf/3.11.4")
        self.requires("abseil/20200225.2")

    def build_requirements(self):
        self.build_requires("protobuf_compiler/3.11.4@signbit/testing")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "grpc-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        for patch in self.conan_data["patches"][self.version]:
            print("Looking for {}".format(patch))
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["gRPC_BUILD_CODEGEN"] = "ON"
        cmake.definitions["gRPC_BUILD_CSHARP_EXT"] = "OFF"
        cmake.definitions["gRPC_BUILD_TESTS"] = "OFF"
        cmake.definitions["gRPC_INSTALL"] = "ON"
        cmake.definitions["gRPC_INSTALL"] = "ON"
        cmake.definitions["gRPC_USE_PROTO_LITE"] = "OFF"

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def package(self):
        cmake = self._configure_cmake()

        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        binDir = src="{}/bin".format(self._build_subfolder)
        self.copy("grpc_cpp_plugin", dst="bin", src=binDir)
        self.copy("grpc_node_plugin", dst="bin", src=binDir)
        self.copy("grpc_python_plugin", dst="bin", src=binDir)
        self.copy("grpc_ruby_plugin", dst="bin", src=binDir)

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        self.info.include_build_settings()

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.GRPC_CPP_PLUGIN_BIN = os.path.normpath(
            os.path.join(self.package_folder, "bin", "grpc_cpp_plugin")
        )
        self.env_info.GRPC_PYTHON_PLUGIN_BIN = os.path.normpath(
            os.path.join(self.package_folder, "bin", "grpc_python_plugin")
        )
        self.env_info.GRPC_NODE_PLUGIN_BIN = os.path.normpath(
            os.path.join(self.package_folder, "bin", "grpc_node_plugin")
        )
        self.env_info.GRPC_RUBY_PLUGIN_BIN = os.path.normpath(
            os.path.join(self.package_folder, "bin", "grpc_ruby_plugin")
        )
