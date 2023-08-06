from setuptools import setup, find_packages
import re

# auto-updating version code stolen from RadVel
def get_property(prop, project):
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(project + "/__init__.py").read(),
    )
    return result.group(1)

def get_requires():
    reqs = []
    for line in open("requirements.txt", "r").readlines():
        reqs.append(line)
    return reqs

setup( 
    name = "SpaceShare",
    version=get_property("__version__", "SpaceShare"),
    packages = find_packages(),
    description="Package to schedule ride and hotel sharing",
    long_description=open("README.md").read(),
    url="https://github.com/sheydenreich/SpaceShare",
    install_requires=get_requires(),
)