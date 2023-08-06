import setuptools
long_description=""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="Perfole",
    version="0.0.6",
    author="breeze-testing",
    description="Measure performance",
    packages=["Perfole"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'license.txt',
    license_files=['license.txt'],
    install_requires=["requests"],
    setup_requires=["requests"]
)