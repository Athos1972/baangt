import setuptools

if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="baangt",
        version="2020.5.2rc5",
        author="Bernhard Buhl",
        author_email="info@baangt.org",
        description="Open source Test Automation Suite for MacOS, Windows, Linux",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://baangt.org",
        packages=setuptools.find_packages(),
        data_files=[('baangt', ["baangt/ressources/baangtLogo.png", "baangt/ressources/baangtLogo2020Small.png"])],
        package_data={"baangt.ressources": ['*.png',]},
        install_requires=["Appium-Python-Client", "beautifulsoup4", "browsermob-proxy","dataclasses", "dataclasses-json",
                          "faker",  "gevent", "lxml",
                          "openpyxl",
                          "Pillow", "pluggy", "pyperclip",  "pyQT5",
                          "requests", "requests-toolbelt",
                          "schwifty", "selenium", "sqlalchemy",
                          "urllib3",
                          "xl2dict", "xlrd", "xlsxwriter",
                           ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
        python_requires='>=3.6',
    )
