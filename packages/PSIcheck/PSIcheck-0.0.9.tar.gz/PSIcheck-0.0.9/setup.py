from setuptools import setup, find_packages

setup(
    name='PSIcheck',
    version='0.0.9',
    description="check PSI-Blast result",
    author='Runjia Ji',
    author_email='jirunjia@gmail.com',
    # py_modules=["magcluster", 'args', 'capture_args', 'maga', 'magm', 'magsc', 'main'],
    # package_dir={'': 'src'},
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
    ],
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    install_requires=[
        "biopython",
        'pandas>1.3',
    ],
    entry_points={
        'console_scripts':[
            'PSIcheck = PSIcheck:main',
        ]
    },
    # package_data={
    #     'magcluster':['data/*.fasta'],
    # }
)