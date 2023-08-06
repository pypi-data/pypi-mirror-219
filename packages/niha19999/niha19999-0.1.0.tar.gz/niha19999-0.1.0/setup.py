from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.0'
DESCRIPTION = 'just say hellooo'


# Setting up
setup(
    name="niha19999",
    version=VERSION,
    author="NiharikaB",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)