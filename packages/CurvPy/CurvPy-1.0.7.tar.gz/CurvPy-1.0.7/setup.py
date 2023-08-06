from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='CurvPy',
    version='1.0.7',
    author='sidharth',
    author_email='sidharthss2690@gmail.com',
    description='A regression analysis library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib',
    ],
)
