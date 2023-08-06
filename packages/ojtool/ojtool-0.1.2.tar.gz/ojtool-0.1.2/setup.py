import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ojtool",
    version="0.1.2",
    author="elecraft",
    author_email="elecraft@outlook.com",
    description="Online Judge Test Data Generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ElementCraft/python-ojtool",
    project_urls={
        "Bug Tracker": "https://github.com/ElementCraft/python-ojtool/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)