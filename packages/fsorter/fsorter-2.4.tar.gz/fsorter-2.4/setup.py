import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="fsorter",  
    version="2.4",
    author="Kadir Barut",
    author_email="kadirrbrtt@gmail.com",
    description="File sorting program according to the numbers in the file name.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kadirrbrtt/fsorter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)