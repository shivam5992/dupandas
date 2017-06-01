from setuptools import setup

setup(
	name='dupandas',    
	version='0.1.2',                          
	scripts=['dupandas'],
	description = 'python package to deduplicate text data in pandas dataframe using flexible string matching and cleaning',
  	author = 'Shivam Bansal',
  	author_email = 'shivam5992@gmail.com',
  	url = 'https://github.com/shivam5992/dupandas', 
  	keywords = ['pandas', 'deduplication', 'text cleaning', 'flexible matching'],
    long_description=open('README.md').read(),
    license='MIT',
    classifiers=(
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        ),
)