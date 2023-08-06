from setuptools import setup,find_packages


with open("README.md","r") as f:
    markdown=f.read()

with open("LISENCE","r") as f:
    lisence=f.read()

setup(
    name="SempCode",
    version="0.5.72",
    packages=find_packages(),
    license="Mozilla Public License Version 2.0",
    install_requires=["requests","pillow","pathlib","subprocess","datetime",
                      "ctypes","ttkthemes","random","tqdm","warnings"],
    author="是真的Win12Home",
    author_email="mcdhj-work@outlook.com",
    description="Simplified the Python Code",
    classifiers=["Development Status :: 5 - Production/Stable"],
    long_description=markdown,
    long_description_content_type="text/markdown",
    license_files=lisence,
    package_data={"mypkg":["Semp/*.pyi"]}
)