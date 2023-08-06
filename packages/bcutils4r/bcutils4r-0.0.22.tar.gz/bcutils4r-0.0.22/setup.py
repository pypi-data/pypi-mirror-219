import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bcutils4r", # Replace with your own username
    version="0.0.22",
    author="Rutuja Gurav",
    author_email="rutujagurav100@gmail.com",
    description="Wrapper around some basic sklearn and scikit-plot utilities for binary classification.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rutujagurav/bcutils4r",
    project_urls={
        "Bug Tracker": "https://github.com/rutujagurav/bcutils4r/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'deprecation', 'seaborn', 'scikit-learn', 'scikit-plot'
      ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)