import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='ezeval',  
     version='0.0.1',
     author="philencegold",
     author_email="",
     description="Library for easy marking.",
     long_description=long_description,

     long_description_content_type="text/markdown",
     url="https://github.com/philencegold/ezeval",
     packages=setuptools.find_packages(),
     install_requires=['PyPDF2', 'openpyxl', 'unidecode'],

     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License"
     ],

 )