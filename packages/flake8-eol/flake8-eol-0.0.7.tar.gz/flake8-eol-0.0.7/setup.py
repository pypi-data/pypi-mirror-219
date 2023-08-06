from setuptools import setup


setup(
    name="flake8-eol",
    version="0.0.7",
    author="Claudio Scheer",
    author_email="claudioscheer@protonmail.com",
    description="Flake8 plugin to enforce EOL consistency",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
