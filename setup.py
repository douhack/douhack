from setuptools import setup, find_packages

install_requires = ['SQLAlchemy', 'yuicompressor', 'webassets', 'Routes', ]

setup(name='douhack',
      version='1.0',
      author='Sviatoslav Sydorenko',
      author_email='wk@sydorenko.org.ua',
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=["test**"]),
      install_requires=install_requires,
      zip_safe=False)
