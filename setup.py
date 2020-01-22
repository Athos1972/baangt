import setuptools

if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="baangt", # Replace with your own username
        version="2020.1.1b12",
        author="Bernhard Buhl",
        author_email="buhl@buhl-consulting.com.cy",
        description="Basic And Advanced NextGeneration Testing",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://baangt.org",
        packages=setuptools.find_packages(),
        install_requires=["pandas", "numpy", "pySimpleGui", "beautifulsoup4", "schwifty"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
