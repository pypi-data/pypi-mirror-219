from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='whoi_uwapm',
    version='0.0.3',
    description='WHOI Acomms Group uwapm',
    long_description=readme,
    long_description_content_type = "text/markdown",
    author='WHOI Acomms Group',
    url='https://git.whoi.edu/acomms/whoi_uwapm',
    license='BSD (3-clause)',
    install_requires=['numpy', 'pandas', 'scipy'],
    package_data={"whoi_uwapm": ["bellhopcxx"]},
)
