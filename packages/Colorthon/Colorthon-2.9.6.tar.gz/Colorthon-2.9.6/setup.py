from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Colorthon",
    version="2.9.6",
    author="Mohammadreza Fekri",
    author_email="Pymmdrza@gmail.com",
    description="Colorthon Best and Fast Package For Generating Color For Text Color and Back Color Text Format",
    keywords=['color', 'colorthon', 'color package', 'text color', 'python color', 'color text', 'print color',
              'back color', 'format color', 'colorthon package'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/colorthon/colorthon",
    project_urls={
        "Documentation": "https://colorthon.gitbook.io/colorthon/",
        "Personal Website": "https://mmdrza.com",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
