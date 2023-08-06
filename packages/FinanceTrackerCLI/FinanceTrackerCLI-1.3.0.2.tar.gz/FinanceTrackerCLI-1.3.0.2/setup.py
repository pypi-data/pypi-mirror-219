from setuptools import setup, find_packages

setup(
    name='FinanceTrackerCLI',
    version='1.3.0.2',
    author='Vladimir Kobranov',
    author_email='josephclturok@gmail.com',
    description='Finance tracker CLI app',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VladimirKobranov/FinanceTrackerCLI',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.11',
    install_requires=[
        'forex-python==1.8',
    ],
)
