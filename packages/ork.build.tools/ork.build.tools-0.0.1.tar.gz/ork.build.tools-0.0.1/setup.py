from setuptools import setup, find_packages
import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ork.build.tools',
    version = '0.0.1',
    packages=find_packages(where='scripts'),
    package_dir={'': 'scripts'},
    package_data={'ork.build.tools': ['bin_priv/*']},
    scripts=glob.glob('bin_pub/*'),
    long_description=long_description,
    long_description_content_type='text/markdown')
