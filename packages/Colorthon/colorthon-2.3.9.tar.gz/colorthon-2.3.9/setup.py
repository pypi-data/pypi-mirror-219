from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='colorthon',
    version='2.3.9',
    author='Mohammadreza Fekri',
    author_email='Pymmdrza@Gmail.Com',
    description='Python package for coloring text and background text',
    keywords=['colorthon', 'text color', 'console', 'python color', 'color print', 'text color', 'back color'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/colorthon/colorthon",
    project_urls={
        "Documentation": "https://colorthon.github.io/colorthon/",
        "Personal Website": "https://mmdrza.com"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
