from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='md2indexhtml',
    version='0.1.4',
    description='Convert Markdown files to index.html',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fasil',
    author_email='fasilwdr@hotmail.com',
    url='https://github.com/fasilwdr/md2indexhtml',
    packages=find_packages(),
    install_requires=[
        'markdown',
    ],
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
