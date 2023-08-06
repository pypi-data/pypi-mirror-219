from setuptools import setup, find_packages

def get_requires():
    reqs = []
    for line in open("requirements.txt", "r").readlines():
        reqs.append(line)
    return reqs

setup(
    name="kirkwoodnight",
    version="0.30",
    packages=find_packages(),

    # Metadata
    author="Armaan Goyal, Brandon Radzom, Jessica Ranshaw, Xian-Yu Wang",
    author_email="armgoyal@iu.edu, bradzom@iu.edu, jranshaw@iu.edu, xwa5@iu.edu",
    description="Interactive command line tool to assist with observations at Kirkwood Observatory.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://packages.python.org/kirkwoodnight",
    license_files = ('LICENSE.txt',),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],

    # Specify console scripts
    entry_points={
        'console_scripts': [
            'kirkwoodnight = kirkwoodnight.command_line:main',
        ],
    },

    # Include additional files into the package
    package_data={'': ['data/*.csv']},

    install_requires= get_requires(),
)