#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: Conan is supported on a best-effort basis. Abseil doesn't use Conan
# internally, so we won't know if it stops working. We may ask community
# members to help us debug any problems that arise.

import os

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conans.model.version import Version


class AbseilConan(ConanFile):
    name = "abseil"
    version = "20200225.2"
    description = "Abseil Common Libraries (C++) from Google"
    homepage = "https://github.com/abseil/abseil-cpp"
    url = "https://github.com/0x8000-0000/conan-recipes/"
    license = "Apache-2.0"
    author = "Florin Iucha <florin@signbit.net>"
    topics = ("conan", "abseil", "abseil-cpp", "google", "common-libraries")
    settings = "os", "compiler", "build_type", "arch"
    exports = ["LICENSE"]
    exports_sources = ["CMakeLists.txt", "CMake/*", "absl/*"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}    
    generators = "cmake"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def configure(self):
        if (
            self.settings.os == "Windows"
            and self.settings.compiler == "Visual Studio"
            and Version(self.settings.compiler.version.value) < "14"
        ):
            raise ConanInvalidConfiguration("Abseil does not support MSVC < 14")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-cpp-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy("*.h", dst="include", src=self._source_subfolder, keep_path=True)
        self.copy("*.inc", dst="include", src=self._source_subfolder, keep_path=True)
        self.copy("*.a", dst="lib", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [
            "absl_flags_parse",
            "absl_flags_usage",
            "absl_flags_usage_internal",
            "absl_flags",
            "absl_flags_internal",
            "absl_flags_registry",
            "absl_flags_config",
            "absl_flags_program_name",
            "absl_flags_marshalling",
            "absl_raw_hash_set",
            "absl_random_seed_sequences",
            "absl_hashtablez_sampler",
            "absl_synchronization",
            "absl_time",
            "absl_civil_time",
            "absl_time_zone",
            "absl_failure_signal_handler",
            "absl_random_internal_distribution_test_util",
            "absl_examine_stack",
            "absl_symbolize",
            "absl_str_format_internal",
            "absl_graphcycles_internal",
            "absl_stacktrace",
            "absl_malloc_internal",
            "absl_demangle_internal",
            "absl_debugging_internal",
            "absl_periodic_sampler",
            "absl_exponential_biased",
            "absl_random_internal_pool_urbg",
            "absl_random_distributions",
            "absl_random_internal_seed_material",
            "absl_random_seed_gen_exception",
            "absl_hash",
            "absl_strings",
            "absl_strings_internal",
            "absl_bad_variant_access",
            "absl_throw_delegate",
            "absl_city",
            "absl_base",
            "absl_dynamic_annotations",
            "absl_bad_any_cast_impl",
            "absl_scoped_set_env",
            "absl_bad_optional_access",
            "absl_raw_logging_internal",
            "absl_log_severity",
            "absl_spinlock_wait",
            "absl_random_internal_randen",
            "absl_random_internal_randen_hwaes",
            "absl_random_internal_randen_slow",
            "absl_random_internal_randen_hwaes_impl",
            "absl_leak_check",
            "absl_leak_check_disable",
            "absl_int128",
        ]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
        self.cpp_info.names["cmake"] = "absl"
