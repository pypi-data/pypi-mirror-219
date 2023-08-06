import logging
from setuptools import setup

# Configure the logging
logging.basicConfig(level=logging.INFO)

setup(
    name='vg-commons-pkg',
    version='2.0.2',
    packages=['vanguardpkg'],
    url='https://github.com/Syed-Shah-Fahad/https://github.com/TridentMarketing/vanguard-common.git',
    author='Syed-Shah-Fahad',
    author_email='syed.fahad009@gmail.com',
    description='A package for Vanguard Commons',
    long_description='Detailed description of the package and its features.',
    long_description_content_type='text/markdown',
    keywords='vanguard commons package',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/Syed-Shah-Fahad/https://github.com/TridentMarketing/vanguard-common/issues',
        'Source': 'https://github.com/Syed-Shah-Fahad/https://github.com/TridentMarketing/vanguard-common',
    },
)
