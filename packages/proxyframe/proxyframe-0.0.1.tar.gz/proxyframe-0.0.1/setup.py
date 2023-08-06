from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Creating clones of datasets'
LONG_DESCRIPTION = 'A package that allows to create imperfect clones of datasets that can be used to evaluate model performace on test datasets for which real targets are not available ahead of time.'

# Setting up
setup(
    name="proxyframe",
    version=VERSION,
    author="Kyrylo Mordan",
    author_email="<parachute.repo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['torch', 'sklearn'],
    keywords=['python', 'clustering', 'clonning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
