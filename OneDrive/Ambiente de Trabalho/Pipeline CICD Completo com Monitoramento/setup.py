#!/usr/bin/env python3
"""
Setup configuration for Pipeline CI/CD REST API
Package for distributing via GitHub Packages
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pipeline-cicd-api",
    version="1.0.0",
    author="Paulo Ramos",
    author_email="paulo@example.com",
    description="REST API for Pipeline CI/CD with Flask, featuring task management and Kubernetes integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PauloRamos38/pipeline-cicd-monitoramento",
    project_urls={
        "Bug Tracker": "https://github.com/PauloRamos38/pipeline-cicd-monitoramento/issues",
        "Documentation": "https://github.com/PauloRamos38/pipeline-cicd-monitoramento#readme",
        "Source Code": "https://github.com/PauloRamos38/pipeline-cicd-monitoramento",
    },
    py_modules=["main"],
    python_requires=">=3.9",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="flask api rest ci-cd kubernetes pipeline monitoring",
    include_package_data=True,
    zip_safe=False,
)
