from setuptools import setup, find_packages

install_requires = [
    "numpy",
    "matplotlib",
    "datetick @ git+https://github.com/rweigel/datetick@main"
]

setup(
    name='stackplot',
    version='0.0.1',
    author='Bob Weigel',
    author_email='rweigel@gmu.edu',
    packages=find_packages(),
    description='Time series stack plots using Matplotlib',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    include_package_data=True,
)
