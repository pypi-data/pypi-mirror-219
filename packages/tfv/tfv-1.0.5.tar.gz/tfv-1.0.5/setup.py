import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

setup = \
    {
        'name': "tfv",
        'version': '1.0.5',
        'description': "Post processing tools for TUFLOW FV results",
        'long_description': long_description,
        'long_description_content_type': "text/markdown",
        'url': "https://gitlab.com/TUFLOW/tfv",

        'author': "TUFLOW Support",
        'author_email': "support@tuflow.com",

        'packages': ['tfv'],

        'classifiers':
            [
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],

        'python_requires': '>=3.9',
        'install_requires':
            [
                'numpy>=1.19.0',
                'matplotlib>3.2.2',
                'netCDF4>=1.5.3',
                'xarray>=v2022.03.0',
                'dask>=2022.01.0',
                'scipy>=1.6.0',
                'tqdm>=4.50.0'
            ],
        'extras_require':{
            'viewer': ["PyQt5>=5.15.0"]
        }
    }

setuptools.setup(**setup)
