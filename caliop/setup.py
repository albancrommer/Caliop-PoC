import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pyramid_jinja2',
    'cornice',
    'simplejson',
    'sphinx',
    'sphinxcontrib-httpdomain',
    'dateutils',
    'requests',
    'bcrypt',
    'PyYAML',
    # 'git+https://github.com/gdchamal/cqlengine.git',
    # 'git+https://github.com/ekini/gsmtpd.git'  # OK I shouldn't, or not ...
    ]

setup(name='caliop',
      version='0.0.1',
      description='A poc for the Caliop project.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="caliop",
      entry_points={
          'paste.app_factory': ['main = caliop:main'],
          'console_scripts': 'caliop = caliop.bin.cli:main',
      })
