from setuptools import setup, find_packages

setup(
    name='git_dl',
    version='0.0.2',
    author='the runtime',
    author_email='theruntime7@gmail.com',
    description='Cli app to download github repo folders',
    long_description='A longer description of your app',
    url='https://github.com/the-runtime/git_dl',
    packages=find_packages(),
    package_data={
        'git_dl': ['data/*.yml']
    },
    entry_points={
        'console_scripts': [
            'git_dl = git_dl.cli_main:start'
        ]
    },
    install_requires=[
        'requests>=2.25.1',
        'selectorlib'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
