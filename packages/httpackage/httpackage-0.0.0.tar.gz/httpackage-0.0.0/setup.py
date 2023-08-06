from setuptools import setup

with open("quas.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="httpackage",
    version="0.0.0",
    author="PyModuleDev",
    author_email="pxcom@mail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["httpackage"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6"
)
