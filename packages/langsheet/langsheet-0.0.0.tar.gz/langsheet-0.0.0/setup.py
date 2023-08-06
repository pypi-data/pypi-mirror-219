from setuptools import setup

LONG_DESCRIPTION = "MyTrip.AI python package for Langsheet"

setup(
    name="langsheet",
    version="0.0.0",
    description="Langhseet python package",
    long_description_content_type = "text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/nikhilkumarsingh/weather-reporter",
    author="MyTrip.AI",
    author_email="info@mytrip.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["langsheet_package"],
    include_package_data=True,
    install_requires=[]
)