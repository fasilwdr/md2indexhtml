from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='md2indexhtml',
    version='0.1.5',
    description='Convert Markdown files to index.html for Odoo modules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fasil',
    author_email='fasilwdr@hotmail.com',
    url='https://github.com/fasilwdr/md2indexhtml',
    packages=find_packages(),
    install_requires=[
        'markdown>=3.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup :: HTML',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='markdown, html, odoo, documentation',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'md2indexhtml=md2indexhtml.converter:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/fasilwdr/md2indexhtml/issues',
        'Source': 'https://github.com/fasilwdr/md2indexhtml',
    },
)