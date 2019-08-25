from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bankroll-broker",
    version="0.4.0",
    author="Justin Spahr-Summers",
    author_email="justin@jspahrsummers.com",
    description="TODO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/bankroll-py/bankroll-broker",
    packages=find_packages(),
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
    install_requires=[
        "bankroll-model @ https://github.com/bankroll-py/bankroll-model@d14670914229b558b42739176b031b03d93f261e#egg=bankroll-model"
    ],
    keywords="trading investing finance portfolio",
)

