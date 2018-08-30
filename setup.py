from setuptools import setup

with open('README.md') as readme:
    README = readme.read()

setup(
    name='dataclass_structor',
    version='0.1',
    description='A type aware structor/destructor for python value objects.',
    long_description=README,
    url='https://github.com/hockeybuggy/dataclass_structor',
    author='Douglas Anderson',
    author_email='hockeybuggy@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT Software License',
        'Programming Language :: Python :: 3.7',
    ],
    py_modules=['dataclasses']
)
