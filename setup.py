from setuptools import setup

setup(
	name='dupandas',    
	packages=[
          'dupandas',
      ],
	version='0.3.2',                          
	description = 'python package to deduplicate text data in pandas dataframe using flexible string matching and cleaning',
  	author = 'Shivam Bansal',
  	author_email = 'shivam5992@gmail.com',
  	url = 'https://github.com/shivam5992/dupandas', 
  	keywords = ['pandas', 'deduplication', 'text cleaning', 'flexible matching'],
    long_description=open('README.md').read(),
    license='MIT',
    classifiers=(
        "Programming Language :: Python"
        ),
)