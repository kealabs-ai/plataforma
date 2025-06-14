from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="kognia-one",
    version="0.1.0",
    author="Kognia",
    author_email="kogniaone@gmail.com",
    description="Plataforma integrada Kognia One com suporte a múltiplos modelos de IA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kogniaone/kognia-one",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kognia-api=api.main:run_app",
            "kognia-frontend=frontend.app:run_app",
        ],
    },
)