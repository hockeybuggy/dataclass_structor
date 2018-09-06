from setuptools import setup

from _version import VERSION

with open('README.md') as readme:
    README = readme.read()

setup(
    name='dataclass_structor',
    version=VERSION,
    description='A type aware structor/destructor for python value objects.',
    long_description=README,
    url='https://github.com/hockeybuggy/dataclass_structor',
    author='Douglas Anderson',
    author_email='hockeybuggy@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    py_modules=['dataclasses']
)
