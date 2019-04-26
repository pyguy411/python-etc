import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thought-pad",
    version="0.0.1",
    author="PyGuy",
    author_email="pyguy411@gmail.com",
    description="CLI to access information you might need quickly.",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/davidj411/thought-pad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)