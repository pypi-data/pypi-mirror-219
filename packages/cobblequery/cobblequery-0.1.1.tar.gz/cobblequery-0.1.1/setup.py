from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'cobblequery',
    scripts=['bin/cobble'],
    packages=['cobblelib'],
    version = '0.1.1',
    description = 'CLI tool for doing data joining',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'KJ',
    author_email = 'jdotpy@users.noreply.github.com',
    url = 'https://github.com/jdotpy/cobble',
    download_url = 'https://github.com/jdotpy/cobble/tarball/master',
    keywords = ['tools'],
    install_requires=[],
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
)
