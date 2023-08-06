from setuptools import setup

setup(
    name='censoredzz',
    version='1.0.0',
    description='Python package for censoring profane words in Nepali-(Roman) text',
    author='Kuber Budhathoki',
    author_email='koobear99@gmail.com',
    url='https://github.com/12-Twelvve/pypi_censored_text',
    packages=['censoredzz'],
    package_data={
        'censoredzz': ['models/rf_model.pkl', 'models/vocabulary.pkl'],
    },
    install_requires=[
        'regex',
        'sklearn',
    ],
) 