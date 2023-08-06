import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="task_multiprocess",
    version="0.0.6",
    author="raymond",
    author_email="lei20190123@gmail.com",
    description="run tasks in parallel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['task_multiprocess'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)