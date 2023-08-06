import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="j2config",
    version="0.0.6",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="configuration generation using jinja2 - for Networking Geeks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliasgar1978/j2config",
    # package_data={
    #     'facts_finder': [
    #         'generators/commands/*',   ## j2config not have any as such
    #         ],
    # },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['pandas', 'jinja2', 'xlrd', 'openpyxl', 'nettoolkit'],
)

