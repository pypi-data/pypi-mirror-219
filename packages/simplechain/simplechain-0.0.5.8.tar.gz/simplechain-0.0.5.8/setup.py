from setuptools import setup, find_packages

VERSION = '0.0.5.8'
DESCRIPTION = 'A package of AI services in modular form'
LONG_DESCRIPTION = 'A package of AI services in modular form easily configurable and deployable'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="simplechain", 
        version=VERSION,
        author="Rahel Gunaratne",
        author_email="rahel.gunaratne@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)