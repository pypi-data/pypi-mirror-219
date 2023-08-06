from setuptools import find_packages, setup
import os

def get_long_description():
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

setup(
    name='openirt',
    packages = find_packages(include=['openirt', 
                                      'openirt.item_models', 
                                      'openirt.mmle']),
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/pleased/...',
    version='0.1.8',
    description='Item response theory toolkit',
    author='Johan Hay',
    license='MIT',
)

