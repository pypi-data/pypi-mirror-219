from setuptools import setup

setup(
    name="flake8-eol",
    version="0.0.1",
    description="Flake8 plugin to enforce EOL consistency",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/claudioscheer/flake8-eol",
    author="Claudio Scheer",
    author_email="claudioscheer@protonmail.com",
    install_requires=["flake8"],
    classifiers=[
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
    ],
)
