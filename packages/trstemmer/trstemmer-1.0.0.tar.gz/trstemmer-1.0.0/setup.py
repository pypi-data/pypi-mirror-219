from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'A simple Turkish stemmer'

with open('README.md') as f:
    long = f.read()
setup(
        name="trstemmer", 
        version=VERSION,
        author="Mehmet Utku OZTURK",
        author_email="<contact@ælphard.tk>",
        description=DESCRIPTION,
        long_description=long,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=["spacy"],
        python_requires='>3.9.13',
        keywords=['stemmer', 'machine learning', 'nlp'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: Turkish",
            "Programming Language :: Python :: 3"
        ]
)