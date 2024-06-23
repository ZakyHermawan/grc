import os
from setuptools import setup
from prebuilt_binaries import prebuilt_binary, PrebuiltExtension

ext_module = PrebuiltExtension(os.environ['PREBUILT_FILE'])

setup(
    name='grc',
    version='3.10.0.0',
    cmdclass={
        'build_ext': prebuilt_binary,
    },
    ext_modules=[ext_module]
)
