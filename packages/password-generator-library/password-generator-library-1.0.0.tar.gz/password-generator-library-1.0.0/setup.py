from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="password-generator-library",
    version="1.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="A password generating library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/password-generator-library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
