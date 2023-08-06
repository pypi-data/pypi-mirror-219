from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="GaussianCovariances",
    version="1.0.2",
    author="Alfonso Veropalumbo",
    author_email="alfonso.veropalumbo@inaf.it",
    description="Python Module to compute the gaussian covariance of two-point clustering probes.",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/veropalumbo.alfonso/gaussiancovariance",
    package_dir={"": "."},
    packages=['GaussianCovariance'],
    python_requires=">=3.6",
    install_requires=["numpy", "scipy"]
)
