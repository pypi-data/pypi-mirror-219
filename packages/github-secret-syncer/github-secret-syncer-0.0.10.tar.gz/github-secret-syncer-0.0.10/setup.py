import setuptools
from pathlib import Path

base_dir = Path(__file__).parent.resolve()
long_description = (base_dir / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="github-secret-syncer",
    version="0.0.10",
    install_requires=[
        "PyNaCl==1.5.0",
    ],
    author="thejimmylin",
    author_email="b00502013@gmail.com",
    description="Github Secret Syncer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thejimmylin/github-secret-syncer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
