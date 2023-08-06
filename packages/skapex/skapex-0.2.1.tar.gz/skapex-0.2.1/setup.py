from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy

setup_kwargs = {}

ext_modules = [
    Extension(
        name="skapex.inner_ap",
        sources=["skapex/inner_ap.pyx"],
        language="c++",
    )
]

setup_kwargs.update({
    'ext_modules': cythonize(ext_modules, language_level='3'),
    'cmdclass': {'build_ext': build_ext},
    'include_dirs': [numpy.get_include()],
    'zip_safe': False,
})

setup(**setup_kwargs)
