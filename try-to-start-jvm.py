#!/usr/bin/env python3

import pathlib
import sys

import jpype
import jpype.imports


CLASS_PATH = pathlib.Path() / "r5-v7.1-r5py-all.jar"


def start_jvm():
    if not jpype.isJVMStarted():
        jpype.startJVM(
            "-Xcheck:jni",
            classpath=CLASS_PATH,
        )

        # Add shutdown hook that cleans up the temporary directory
        @jpype.JImplements("java.lang.Runnable")
        class ShutdownHookToCleanUpTempDir:
            @jpype.JOverride
            def run(self):
                print("foo baar")

        import java.lang

        java.lang.Runtime.getRuntime().addShutdownHook(
            java.lang.Thread(ShutdownHookToCleanUpTempDir())
        )


class _JImportLoaderThatStartsTheJvm(jpype.imports._JImportLoader):
    """Find Java packages for import statements, start JVM before that."""

    def find_spec(self, name, path, target=None):
        # we got this far in `sys.meta_path` (no other finder/loader
        # knew about the package we try to load), and naturally, we’re
        # towards the end of that list.

        # Let’s assume the requested packages is a Java package,
        # and start the JVM
        start_jvm()

        # then go the standard jpype way:
        return super().find_spec(name, path, target)


# replace jpype’s _JImportLoader with our own:
for i, finder in enumerate(sys.meta_path):
    if isinstance(finder, jpype.imports._JImportLoader):
        sys.meta_path[i] = _JImportLoaderThatStartsTheJvm()

import com.conveyal.r5  # noqa: F401, E402
