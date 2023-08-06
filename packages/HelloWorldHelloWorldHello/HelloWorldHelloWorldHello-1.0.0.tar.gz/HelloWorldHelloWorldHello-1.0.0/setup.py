from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="HelloWorldHelloWorldHello",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[""],
    install_requires=["numpy", "pandas"],
)

