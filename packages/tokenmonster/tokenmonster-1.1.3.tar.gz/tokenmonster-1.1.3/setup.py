from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='tokenmonster',
    version='1.1.3',
    py_modules=['tokenmonster'],
    author='Alasdair Forsythe',
    author_email='77910352+alasdairforsythe@users.noreply.github.com',
    description='Tokenize and decode text with TokenMonster vocabularies.',
    url='https://github.com/alasdairforsythe/tokenmonster',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
