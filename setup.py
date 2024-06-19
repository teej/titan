from setuptools import find_packages, setup

setup(
    name="titan",
    version=open("version.md", encoding="utf-8").read().split(" ")[2],
    description="Titan Core: Snowflake infrastructure as code",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Titan-Systems/titan",
    author="TJ Murphy",
    packages=find_packages(include=["titan", "titan.*"]),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: SQL",
        "Topic :: Database",
        "Framework :: Titan",
    ],
    install_requires=[
        "click>=8.1.7",
        "inflection>=0.5.1",
        "pygithub==1.55",
        "pyparsing>=3.0.9",
        "pyyaml",
        "snowflake-connector-python>=3.7.0",
        "snowflake-snowpark-python>=1.14.0",
    ],
    extras_require={
        "dev": [
            "black",
            "codespell==2.2.6",
            "pytest-cov",
            "pytest-profiling",
            "pytest-xdist",
            "pytest>=6.0",
            "ruff",
            "snowflake-cli-labs",
            "tabulate",
        ]
    },
)
