from setuptools import setup, find_packages

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf-8")

VERSION = '0.1.1'
DESCRIPTION = 'A cross-platform design theme framework.'



# Setting up
setup(
    name="blendedux",
    version=VERSION,
    author="Himanshu",
    author_email="<hbhadu@cognam.com>",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data = True,
    packages=find_packages(),
    install_requires=[
        'certifi==2022.5.18.1',
        'click==8.1.3',
        'colorama==0.4.6',
        'Flask==2.2.3',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.2',
        'Pillow==9.5.0',
        'python-dateutil==2.8.2',
        'six==1.16.0',
        'urllib3==1.26.15',
        'Werkzeug==2.2.3',
        'blinker==1.6.2',
        'blendedUx-Lang==1.1.0'
    ]
)