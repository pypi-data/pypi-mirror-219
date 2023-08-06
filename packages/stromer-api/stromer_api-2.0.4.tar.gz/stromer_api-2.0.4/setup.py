from setuptools import setup

setup(
    name='stromer_api',
    version='2.0.4',
    packages=['stromer_api'],
    keywords=['Stromer', 'EBike', 'Python', 'API'],
    url='https://github.com/elnkosc/stromer_api',
    license='GPL',
    author='Koen',
    author_email='koen@schilders.org',
    description='Stromer API for accessing data from your Stromer Speed Bike.',
    long_description=open('README.md', 'rt').read(),
    long_description_content_type='text/markdown'
)
