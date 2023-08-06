import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
    requirements = [l for l in requirements if not l.startswith('#')]

setuptools.setup(
    name="righty",
    version="0.1.0",
    author="Jasper Phelps",
    author_email="jasper.s.phelps@gmail.com",
    description='Code to interact with the "righty" fly CNS GridTape-TEM dataset',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jasper-tms/righty",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
