from setuptools import setup, find_packages
import os


HERE = os.path.dirname(__file__)
README_PATH = os.path.join(HERE, "README.rst")

with open(README_PATH) as fp:
    readme = fp.read()

setup(
    name="httpd-echo",
    version="0.1",
    license="GPL",
    url="https://github.com/rpatterson/httpd-echo",
    description="A Simple Python HTTP server that echos the request in the response",
    long_description=readme,
    author="Ross Patterson",
    author_email="me@rpatterson.net",
    py_modules=["httpdecho"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        "six",
    ],
    extras_require={
        "test": ["requests"],
    },
    entry_points={"console_scripts": ["httpd-echo=httpdecho:main"]},
    keywords="httpd http echo server",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Utilities",
    ],
)
