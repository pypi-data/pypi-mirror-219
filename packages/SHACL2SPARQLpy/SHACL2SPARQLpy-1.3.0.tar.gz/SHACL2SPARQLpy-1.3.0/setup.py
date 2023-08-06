from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.3.0'

setup(
    name='SHACL2SPARQLpy',
    version=VERSION,
    packages=['SHACL2SPARQLpy', 'SHACL2SPARQLpy.constraints', 'SHACL2SPARQLpy.core', 'SHACL2SPARQLpy.sparql', 'SHACL2SPARQLpy.utils'],
    license='MIT',
    author='Mónica Figuera, Philipp D. Rohde',
    author_email='philipp.rohde@tib.eu',
    url='https://github.com/SDM-TIB/SHACL2SPARQLpy',
    download_url='https://github.com/SDM-TIB/SHACL2SPARQLpy/archive/refs/tags/v' + VERSION + '.tar.gz',
    description='Python reference implementation of SHACL2SPARQL',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['SPARQLWrapper>=1.8.5', 'rdflib>=6.0.0'],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research'
      ]
)
