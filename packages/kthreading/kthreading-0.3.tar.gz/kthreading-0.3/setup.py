import setuptools

with open("README.md", "r", encoding="utf-8", errors="IGNORE") as file:
    readme_contents = file.read()

with open("LICENSE.md", "r", encoding="utf-8", errors="IGNORE") as file:
    license_contents = file.read()

setuptools.setup(
    name="kthreading",
    version="0.3",
    description="Get more controls over threads",
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.5",
    packages=["kthreading"],
)
