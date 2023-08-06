from setuptools import setup, Extension

with open("README.md",'r') as fh:
    long_description=fh.read()

setup(
  name = 'RangeSlider',         # How you named your package folder (MyLib)
  packages = ['RangeSlider'],   # Chose the same as "name"
  version = '2023.07.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python tkinter widget for range selection in slider widget structure with two handles',   # Give a short description about your library
  author = 'Harsh Agarwal',                   # Type in your name
  author_email = 'harshvinay752@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/harshvinay752/RangeSlider',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/harshvinay752/RangeSlider/archive/refs/tags/2023.07.1.tar.gz',    # I explain this later on
  keywords = ['Python','tkinter','range','slider','two handle','selector','widget'],   # Keywords that define your package best
  install_requires=[],
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
