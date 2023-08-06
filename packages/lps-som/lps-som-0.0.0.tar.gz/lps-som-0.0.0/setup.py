import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lps-som",
    version="0.0.0",
    author="Rodrigo Coura Torres",
    author_email="torres.rc@gmail.com",
    description="Self Organizing Maps with GPU Support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rctorres/lps-som",
    project_urls={
        "Bug Tracker": "https://github.com/rctorres/lps-som/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
