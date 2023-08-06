from setuptools import setup

setup(
    name="dock-py-selenium",
    version="2.1.4",
    author="Bishal Shrestha",
    author_email="iambstha@gmail.com",
    description="A startup / mockup folder for a selenium project with custom methods.",
    long_description="# A startup / mockup folder for a selenium project with custom methods.",
    long_description_content_type="text/markdown",
    url="https://github.com/iambstha/dock-py-selenium",
    packages=["dock_py_selenium.dock"],
    license="MIT",
    keywords=["selenium", "automation", "testing"],
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