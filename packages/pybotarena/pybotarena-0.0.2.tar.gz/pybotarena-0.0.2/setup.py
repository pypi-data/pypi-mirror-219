from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'RobotAR Python package'

setup(
       # the name must match the folder name
        name="robotar", 
        version=VERSION,
        author="Chung Zhi Wei",
        author_email="zhiweichung@gmail.com",
        description=DESCRIPTION,
        packages=find_packages(),
        #install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'RobotAR'],
        classifiers= [
            "Development Status :: Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
