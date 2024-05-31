#!/usr/bin/env python3

import jpype
import jpype.imports

if not jpype.isJVMStarted():
    jpype.startJVM()
    import java.lang  # noqa: F401
    print("successfully started JVM")
