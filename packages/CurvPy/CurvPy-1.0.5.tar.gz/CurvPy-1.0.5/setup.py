from setuptools import setup

setup(
    name='CurvPy',
    version='1.0.5',
    author='sidharth',
    author_email='sidharthss2690@gmail.com',
    description='A regression analysis library',
    packages=['curvpy'],
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib',
    ],
)
