from distutils.core import setup
import os

OS_SEPARATOR = os.path.sep

version = '0.0.6'
name = 'databricks_helper'
packageName = name
repositoryName = name.replace("_", "-")
url = f'https://github.com/SamuelJansen/{repositoryName}/'


setup(
    name = name,
    packages = [
        packageName,
        f'{packageName}{OS_SEPARATOR}api',
        f'{packageName}{OS_SEPARATOR}api{OS_SEPARATOR}src'
    ],
    version = version,
    license = 'MIT',
    description = 'databricks helper package',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = url,
    download_url = f'{url}archive/v{version}.tar.gz',
    keywords = ['helper', 'databricks helper package', 'databricks helper', 'helper package'],
    install_requires = [
        'pyspark<4.0.0,>=3.0.0',
        'python_helper<1.0.0,>=0.3.67'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7'
)
