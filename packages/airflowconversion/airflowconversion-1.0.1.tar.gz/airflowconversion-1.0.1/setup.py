from setuptools import setup

with open("README.md","r") as fh:
    long_description=fh.read()
setup(
    name='airflowconversion',
    version='1.0.1',
    description='Converting Oozie workflows in XML to Python (Airflow Syntax)',
    py_modules=["ParseXML"],
    package_dir={'': 'airflowconversion'},
    url="https://repo1.uhc.com/artifactory/api/pypi/pypi-virtual/simple",
    author="Rashi Agarwal",
    author_email="rashi_agarwal@optum.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    )
