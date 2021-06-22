from setuptools import setup, find_packages

VERSION = '1.0.1'
NAME = "fenix_alpha_vantage"
DESCRIPTION = 'Proprietary Fenix package to interact with Alpha Vantage APIs.'

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author="Ricardo Pedrotti",
    author_email="rpedrottivf@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "pandas >= 1.2.4",
        "matplotlib >= 3.4.2",
        "scikit-learn >= 0.24.2",
        "seaborn >= 0.11.1",
        "convertdate >= 2.3.2",
        "pystan >= 2.18.0.0",
        "plotly >= 5.0.0",
        "notebook >= 6.4.0",
        "pyyaml >= 5.4.1",
        "requests >= 2.25.1",
    ],
    python_requires='>=3',
    keywords=['python', 'alpha vantage', 'fenix'],
)
