#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools, RunEnvironment
import os
import subprocess
import time


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            process = None
            try:
                if self.options["mosquitto"].with_binaries == True:
                    process = subprocess.Popen(["mosquitto"])
                    time.sleep(2)
                bin_path = os.path.join("bin", "test_package")
                if self.settings.os == "Windows":
                    self.run(bin_path)
                elif self.settings.os == "Macos":
                    self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
                else:
                    self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))
            finally:
                if process:
                    process.kill()
