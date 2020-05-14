from conans import ConanFile, CMake, tools
import shutil
import os


class Antlr4Conan(ConanFile):
    name = "antlr4"
    license = "The BSD License"
    author = "Ruisheng Wang <ruisheng.wang@outlook.com>"
    url = "https://github.com/ushering/conan-antlr"
    description = "C++ runtime support for ANTLR"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources-cpp"][self.version], destination=self._source_subfolder)
        tools.get(**self.conan_data["sources-jar"][self.version], destination=self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["WITH_LIBCXX"]="OFF"
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build(target='antlr4_static')

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self._source_subfolder, "runtime", "src"))
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.jar", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
