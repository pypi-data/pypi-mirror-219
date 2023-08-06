from setuptools import setup, find_packages
from readme_renderer.markdown import render

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="motipy",
    version="1.0.0",
    author="Coding Team",
    author_email="codingteam@telegmail.com",
    license='MIT',
    description='Un package Python pour obtenir des messages de motivation.',
    long_description=render(long_description),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["testing"]),
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
)
