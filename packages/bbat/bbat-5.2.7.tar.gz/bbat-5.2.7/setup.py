import setuptools

name = "bbat"
version = "5.2.7"

setuptools.setup(
    name=name,
    version=version,
    author="zlge",
    author_email="test@test.com",
    description="",
    long_description="testModule",
    long_description_content_type="text",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["bbat = bbat.zcli:main"]},
)
