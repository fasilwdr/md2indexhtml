# setup.py

from setuptools import setup, find_packages

setup(
    name='md2indexhtml',
    version='0.1.0',
    description='Convert Markdown files to index.html for Odoo modules',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/md2indexhtml',
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
        'md2indexhtml': ['templates/*.html'],  # Include all HTML files in the templates directory
    },
    include_package_data=True,  # This flag is needed to include the data specified in package_data
)
