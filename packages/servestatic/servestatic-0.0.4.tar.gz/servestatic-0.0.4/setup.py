import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="servestatic",
    version="0.0.4",
    description="static web server cli tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mujdecisy/serve-static",
    keywords=["python", "static", "web", "server"],
    author="mujdecisy",
    author_email="mujdecisy@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["servestatic"],
    include_package_data=True,
    install_requires=[]
)