from setuptools import setup

long_description = """vap
=======================

Apple postback verifier. See `readme`_

Installation
------------

    $ pip install vap

.. _readme: https://github.com/d-ganchar/vap
"""


setup(
    name='vap',
    version='1.1.0',
    description='Apple postback verifier',
    long_description=long_description,
    url='https://github.com/d-ganchar/vas',
    author='Danila Ganchar',
    author_email='danila.ganchar@gmail.com',
    license='MIT',
    keywords='verify apple signature postback',
    packages=['vap'],
    install_requires=['fastecdsa==2.1.2'],
    entry_points={
        'console_scripts': [
            'vap = vap.cli:run',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
