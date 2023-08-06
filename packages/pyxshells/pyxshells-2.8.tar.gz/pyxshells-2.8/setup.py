#!/usr/bin/python

try:
    from setuptools import setup
except:
    from distutils.core import setup

with open('README.md', 'r') as f:
    long_desc = f.read()

def get_ver():
    with open('pyproject.toml', 'r') as f:
        for l in f:
            s=l.find('version =')
            if s>=0:
                return l[s+9:].strip().strip('"').strip("'")
    return 'unknown'

setup(name='pyxshells',
    version=get_ver(),
    description='python tools for handling output of xshells code',
    url='https://nschaeff.bitbucket.io/xshells',
    project_urls={
        "Documentation": "https://nschaeff.bitbucket.io/xshells/manual.html",
        "Source": "https://bitbucket.org/nschaeff/xshells/",
        "Changelog": "https://bitbucket.org/nschaeff/xshells/src/master/CHANGELOG.md",
    },
    author='Nathanael Schaeffer',
    author_email='nathanael.schaeffer@univ-grenoble-alpes.fr',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    py_modules=['pyxshells','xsplot'],
    requires=['numpy','matplotlib','shtns'],
)
