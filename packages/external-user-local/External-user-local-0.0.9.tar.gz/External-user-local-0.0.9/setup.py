import setuptools
# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
     name='External-user-local',  
     version='0.0.9',
     author="Circles",
     author_email="info@circles.life",
     # TODO: Please update the description and delete this line
     description="PyPI Package for Circles access token library Local/Remote Python",
     # TODO: Please update the long description and delete this line    
     long_description="This is a package for sharing common access tokens function used in different repositories",
     long_description_content_type="text/markdown",
     url="https://github.com/circles",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )
