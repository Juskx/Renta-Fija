from setuptools import setup, find_packages

setup(
    name="functions",
    version="0.0.1",
    author="Joaquin Pulgar",
    author_email="joaquin.pulgar10@gmail.com",
    description="Test",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Juskx/Renta-Fija",
    license="GPL-3.0-or-later", 
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=[""]),
    python_requires=">=3.09",
)