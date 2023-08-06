from setuptools import setup

with open('README.rst', 'r', encoding='utf-8') as f:
    ln = f.read()

setup(
    name="PyRandomNameGenerator",
    version="0.2",
    description="This is a simple name generator package",
    long_description= ln,
    long_description_content_type='text/x-rst',
    license="MIT",
    author="Md. Ismiel Hossen Abir",
    packages=["PyRandomNameGenerator"],
    url="https://pypi.org/project/PyRandomNameGenerator/",
    install_requires=[]
    
)