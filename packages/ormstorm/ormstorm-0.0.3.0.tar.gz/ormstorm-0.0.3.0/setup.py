from setuptools import setup, find_packages


VERSION = "0.0.3.0"
DESCRIPTION = "Small library for easy work with databases."

with open("READ ME.md", mode="r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

setup(
    name="ormstorm",
    version=VERSION,
    author="Molchaliv",
    author_email="molchaliv666@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    keywords=["python", "orm", "database", "sql", "sqlite3"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
