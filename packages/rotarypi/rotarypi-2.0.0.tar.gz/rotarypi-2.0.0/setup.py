import pathlib
from setuptools import find_packages, setup


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='rotarypi',
    version='2.0.0',
    description="Reading the rotary dial of an old phone with a RaspberryPi",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    author='Martin Obrist',
    author_email='martin.obrist@buero.io',
    url='https://gitlab.com/rotaryphone/rotarypi',
    project_urls={
        'Documentation': 'https://rotarypi.readthedocs.io',
        'Source Code': 'https://gitlab.com/rotaryphone/rotarypi',
        'Issue Tracker': 'https://gitlab.com/rotaryphone/rotarypi/-/issues'
    },
    packages=find_packages(where='.', exclude=['tests', 'tasks']),
    python_requires='>=3.9, <4',
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=[
        "RPi.GPIO"
    ],
    extras_require={
        'dev': ['twine', 'invoke']
    }
)
