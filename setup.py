import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='pyzoopla',
    version='0.1.6',
    author='Imran Khan',
    author_email='imrankhan17@hotmail.co.uk',
    description='A Python package to access information about properties from Zoopla',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/imrankhan17/pyzoopla',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'lxml',
        'numpy',
        'pandas',
        'pymysql',
        'requests'
    ],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
