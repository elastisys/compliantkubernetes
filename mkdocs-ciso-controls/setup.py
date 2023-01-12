from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-ciso-controls",
    version="0.0.1",
    author="Cristian Klein",
    author_email="cristian.klein@elastisys.com",
    description="Use tags to capture ISMS controls and group them by source.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=["mkdocs>=1.2", "natsort>=8.2.0"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "mkdocs.plugins": [
            "ciso-controls = ciso_controls:CisoControlsPlugin"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Documentation",
    ],
)
