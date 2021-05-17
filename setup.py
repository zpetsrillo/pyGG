import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyGG",
    version="0.1.0",
    author="Zachariah Petsrillo",
    author_email="zpetsrillo@gmail.com",
    description="Easily retrieve op.gg data for use in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zpetsrillo/pyGG",
    project_urls={
        "Bug Tracker": "https://github.com/zpetsrillo/pyGG/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["pyGG"],
    install_requires=["requests", "bs4", "lxml", "pandas"],
)
