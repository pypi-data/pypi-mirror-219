## Setup.py for codeastro project
from setuptools import setup, find_packages

setup(
	name = "platos_closet",

	version = "1.0.0",
 
	author = "Fernando Gutierrez Canales and John Hood",
 
	author_email = "fernando.canales@obspm.fr",
 
	description = "Package that tells you if a planet can be detected by PLATO space mission",

	license = "MIT",
 
 	url = "https://github.com/Fernando-Canales/platos_closet",
 
	packages=find_packages(),
     classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

	)