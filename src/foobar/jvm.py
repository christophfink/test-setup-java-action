#!/usr/bin/env python3

"""Set up a JVM and import basic java classes."""

import os
import pathlib
import shutil
import sys

import jpype
import jpype.imports

MAX_JVM_MEMORY = 20000


__all__ = ["start_jvm"]


def start_jvm():
    """
    Start a Java Virtual Machine (JVM) if none is running already.

    Takes into account the `--max-memory` and `--verbose` command
    line and configuration options.
    """
    if not jpype.isJVMStarted():

        # preload signal handling; this, among other things, prevents some of
        # the warning messages we have been seeing
        # (cf. https://stackoverflow.com/q/15790403 and
        #  https://docs.oracle.com/en/java/javase/19/vm/signal-chaining.html )
        JVM_PATH = pathlib.Path(jpype.getDefaultJVMPath()).resolve()
        if sys.platform == "linux":
            try:
                LIBJSIG = next(JVM_PATH.parent.glob("**/libjsig.so"))
                os.environ["LD_PRELOAD"] = str(LIBJSIG)
            except StopIteration:
                pass  # don’t fail completely if libjsig not found
        elif sys.platform == "darwin":
            try:
                LIBJSIG = next(JVM_PATH.parent.glob("**/libjsig.dylib"))
                os.environ["DYLD_INSERT_LIBRARIES"] = str(LIBJSIG)
            except StopIteration:
                pass  # don’t fail completely if libjsig not found

        TEMP_DIR = "/tmp/asdfasdf/"

        jpype.startJVM(
            f"-Xmx{MAX_JVM_MEMORY:d}",
            "-Xcheck:jni",
            "-Xrs",  # https://stackoverflow.com/q/34951812
            "-Duser.language=en",  # Set a default locale, …
            "-Duser.country=US",  # … as R5 formats numeric return …
            "-Duser.variant=",  # … values as a localised string
            f"-Djava.io.tmpdir={TEMP_DIR}",
            interrupt=True,
        )

        # Add shutdown hook that cleans up the temporary directory
        @jpype.JImplements("java.lang.Runnable")
        class ShutdownHookToCleanUpTempDir:
            @jpype.JOverride
            def run(self):
                try:
                    shutil.rmtree(TEMP_DIR)
                except OSError:
                    pass

        import java.lang

        java.lang.Runtime.getRuntime().addShutdownHook(
            java.lang.Thread(ShutdownHookToCleanUpTempDir())
        )


# # The JVM should be started before we attempt to import any Java package.
# # If we run `start_jvm()` before another `import` statement, linting our
# # code would result in many E402 (‘Module level import not at top of file’)
# # warnings, if the JVM would start implicitely when `__file__` is imported,
# # we would end up with F401 (‘Module imported but unused’) warnings.
#
# # This below is a middle way: We don’t start the JVM right away, only
# # when `start_jvm()` is called. However, if we attempt to import a
# # Java package (or, more precisely, a package that’s likely to be a
# # Java package), the `import` statement would trigger `start_jvm()`
#
# # see:
# # https://github.com/jpype-project/jpype/blob/master/jpype/imports.py#L146
#
#
# class _JImportLoaderThatStartsTheJvm(jpype.imports._JImportLoader):
#     """Find Java packages for import statements, start JVM before that."""
#
#     def find_spec(self, name, path, target=None):
#         # we got this far in `sys.meta_path` (no other finder/loader
#         # knew about the package we try to load), and naturally, we’re
#         # towards the end of that list.
#
#         # Let’s assume the requested packages is a Java package,
#         # and start the JVM
#         start_jvm()
#
#         # then go the standard jpype way:
#         return super().find_spec(name, path, target)
#
#
# # replace jpype’s _JImportLoader with our own:
# for i, finder in enumerate(sys.meta_path):
#     if isinstance(finder, jpype.imports._JImportLoader):
#         sys.meta_path[i] = _JImportLoaderThatStartsTheJvm()
