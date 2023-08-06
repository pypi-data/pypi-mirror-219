from setuptools import setup
with open('readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ML-Algo',
    version='1.2.8',
    author='Mr Raj',
    author_email='arunraj14092002@gmail.com',
    description='A package for calculating Series Time Data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['ML_Algo'],
    install_requires=['pandas','requests'],
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
)