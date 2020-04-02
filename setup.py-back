from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='nhl_scraper',
      version='0.0.3',
      description='Scrape hockey data from various websites',
      long_description=readme(),
      url='http://github.com/spilchen/nhl_scraper',
      author='Matt Spilchen',
      author_email='matt.spilchen@gmail.com',
      license='MIT',
      packages=['nhl_scraper'],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
      ],
      install_requires=['pandas', 'objectpath', 'requests'],
      python_requires='>=3',
      include_package_data=True,
      zip_safe=True)
