from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Hashable dict/list - subclasses of list/dict with a custom hash function based on alternating addition and subtraction of element hashes - pure Python'''

# Setting up
setup(
    name="hashlistdict",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/hashlistdict',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['flatten_any_dict_iterable_or_whatsoever'],
    keywords=['nested', 'list', 'dict', 'hash', 'hashable'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['flatten_any_dict_iterable_or_whatsoever'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*