#!/usr/bin/env python3

import jpype
import jpype.imports

if not jpype.isJVMStarted():
    jpype.startJVM()

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
