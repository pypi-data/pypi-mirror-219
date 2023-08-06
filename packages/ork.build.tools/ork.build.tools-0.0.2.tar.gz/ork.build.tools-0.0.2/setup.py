from setuptools import setup, find_packages
import glob, os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            filter = False
            if filename.endswith('.pyc'):
                filter = True
            if not filter:
                full_path = os.path.join(path, filename)
                relative_path = os.path.relpath(full_path, directory)
                destination = directory + '/' + os.path.dirname(relative_path)
                paths.append((destination, [full_path]))
    return paths

module_files = package_files('modules')
example_files = package_files('examples')
test_files = package_files('tests')

setup(
    name="ork.build.tools",
    version="0.0.2",
    packages=find_packages(where=["scripts"]),
    package_dir={
        "": "scripts",
    },
    package_data={
        "": ["*"],
    },
    scripts=glob.glob('bin_pub/*'),
    data_files=module_files + example_files + test_files,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
