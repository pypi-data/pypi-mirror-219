import os
import re
from setuptools import find_packages, setup

package="dsmlibrary_viz"

def get_version():
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
    
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dsmlibrary_viz',
    version=get_version(),
    url='https://github.com/storemesh/dsmlibrary-viz',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple way to use Dataset. for dsm',
    long_description=README,
    long_description_content_type='text/markdown',
    author='DigitalStoreMesh Co.,Ltd',
    author_email='contact@storemesh.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

    ],
    install_requires=[
        'requests',
        's3fs',
        'duckdb',
        'pandas',
        'matplotlib'
    ],    
)