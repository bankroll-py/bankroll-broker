from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bankroll-broker",
    version="0.4.1",
    author="Justin Spahr-Summers",
    author_email="justin@jspahrsummers.com",
    description="Brokerage plugin interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/bankroll-py/bankroll-broker",
    packages=["bankroll.broker"],
    package_data={"bankroll.broker": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial :: Investment",
        "Typing :: Typed",
    ],
    install_requires=["bankroll-model ~= 0.4.0"],
    keywords="trading investing finance portfolio",
)

