from setuptools import setup

setup(
    name='airflowconversion',
    version='1.0.0',
    description='Converting Oozie workflows in XML to Python (Airflow Syntax)',
    py_modules=["ParseXML"],
    package_dir={'': 'airflowconversion'},
    )
