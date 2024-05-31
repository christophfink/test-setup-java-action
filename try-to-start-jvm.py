#!/usr/bin/env python3

import jpype

if not jpype.isJVMStarted():
    jpype.startJVM(classpath="r5-v7.0-r5py-all.jar")
    import java.lang  # noqa: F401
    print("successfully started JVM")
