import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="habaform",
    version="0.0.1",
    author="Nova Kwok",
    author_email="noc@nova.moe",
    description="Manage Harbor projects and members with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n0vad3v/habaform",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "pyyaml"
    ],
    entry_points={
        'console_scripts': [
            'habaform=habaform.main:main',
        ],
    }
)