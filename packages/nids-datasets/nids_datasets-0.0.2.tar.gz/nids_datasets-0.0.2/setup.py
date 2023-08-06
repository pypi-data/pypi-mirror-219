import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='nids_datasets',
    version='0.0.2',
    description="Download UNSW-NB15 and CIC-IDS2017 Datasets for Network Intrusion Detection (NIDS)",
    keywords="Dataset NIDS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author="Pahalavan R D",
    author_email='rdpahalavan24@gmail.com',
    packages=['nids_datasets'],
    python_requires='>=3.7.0',
    url='https://github.com/rdpahalavan/BERTSimilarWords',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements
)