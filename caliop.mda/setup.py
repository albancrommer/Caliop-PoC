import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'dateutils',
    'PyYAML',
    'caliop'
    ]

setup(name='caliop-mda',
      version='0.0.1',
      description='Mail delivery agent for Caliop',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Daemon",
        ],
      author='',
      author_email='',
      url='',
      keywords='caliop mda mail delivery agent',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="caliop.mda",
      entry_points="""\
      """,
      )
