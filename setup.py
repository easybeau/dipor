from setuptools import setup
setup(
    name='dipor',
    version='1.0',
    description='Static Site Generator written in Python for ease of processes',
    url="https://github.com/vidhibagadia/dipor",
    author="Vidh Bagadia",
    author_email="vidbagadia@gmail.com",
    license="MIT",
    packages=['dipor'],
    install_requires = ['markdown==3.2.2', 'Jinja2==2.11.2', 'html5print==0.1.2', 'Pygments==2.6.1'],
)