import setuptools

setuptools.setup(
    name="jilei",
    version="0.2.1",
    author="jilei",
    author_email="developer@jlzn.cc",
    description="For internal use.",
    long_description="python setup.py bdist_wheel\ntwine upload ./dist/*",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)