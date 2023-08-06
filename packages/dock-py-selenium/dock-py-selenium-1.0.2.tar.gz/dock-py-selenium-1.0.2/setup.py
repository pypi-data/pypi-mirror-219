from setuptools import setup

setup(
    name="dock-py-selenium",
    version="1.0.2",
    author="Bishal Shrestha",
    author_email="iambstha@gmail.com",
    description="A startup / mockup folder for a selenium project with custom methods.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/iambstha/dockSelenium",
    packages=["dock_py_selenium.dock"],
    install_requires=[
        "selenium",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)