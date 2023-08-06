from setuptools import setup

setup(
    name="Dock Py Selenium",
    version="2.0.0",
    author="Bishal Shrestha",
    author_email="iambstha@gmail.com",
    description="A startup / mockup folder for a selenium project with custom methods.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/iambstha/dock-py-selenium",
    packages=["dock_py_selenium.dock"],
    install_requires=[
        "selenium",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)