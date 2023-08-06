import setuptools

setuptools.setup(
    name="searchy",
    version="1.0.2",
    author="lactua",
    author_email="lactua@lactua.com",
    description="Python package that allows you to search on google from commands",
    long_description="",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['google'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'searchy = searchy:main'
        ]
    }
)