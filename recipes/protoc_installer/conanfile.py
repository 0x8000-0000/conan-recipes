import os
from conans import ConanFile, CMake, tools


class ProtocInstaller(ConanFile):
    name = "protoc_installer"
    description = "Protocol Buffers - Google's data interchange format"
    topics = ("conan", "protobuf", "protocol-buffers",
              "protocol-compiler", "serialization", "rpc", "protocol-compiler")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/protocolbuffers/protobuf"
    license = "BSD-3-Clause"
    version = "3.11.4"
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
        self.requires.add("zlib/1.2.11")
        self.requires.add("protobuf/3.11.4")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "protobuf-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        #tools.patch(base_path=self._source_subfolder, patch_file="protoc.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["protobuf_BUILD_TESTS"] = "OFF"
        cmake.definitions["protobuf_WITH_ZLIB"] = "ON"
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["protobuf_MSVC_STATIC_RUNTIME"] = "MT" in self.settings.compiler.runtime
        cmake.configure(build_folder=self._build_subfolder)
        return cmake


    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        self.info.include_build_settings()

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)

        protoc = "protoc.exe" if self.settings.os_build == "Windows" else "protoc"
        self.env_info.PROTOC_BIN = os.path.normpath(os.path.join(self.package_folder, "bin", protoc))

