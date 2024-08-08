# setup.py
from setuptools import setup, find_packages

setup(
    name='md2indexhtml',
    version='0.1.1',
    description='Convert Markdown files to index.html',
    author='Your Name',
    author_email='fasilwdr@hotmail.com',
    url='https://github.com/fasilwdr/md2indexhtml',
    packages=find_packages(),
    install_requires=[
        'markdown',
    ],
    readme="README.md",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'md2indexhtml=md2indexhtml.converter:main',
        ],
    },
    package_data={
        'md2indexhtml': ['templates/*.html'],
    },
    include_package_data=True,
)
