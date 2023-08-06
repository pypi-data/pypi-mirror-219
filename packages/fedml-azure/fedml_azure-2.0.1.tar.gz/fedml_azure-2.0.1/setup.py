import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="fedml_azure",
    version="2.0.1",
    author="SAP SE",
    description="A python library for building machine learning models on AzureML using a federated data source",
    license='Apache License 2.0',
    license_files = ['LICENSE.txt'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "hdbcli","ruamel.yaml"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    package_data={'fedml_azure':['internal_config.json']},
    scripts=['src/fedml_azure/install_validate.sh', 'src/fedml_azure/kyma_deploy.sh'],
    include_package_data=True
)