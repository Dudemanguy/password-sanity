import sys
from pathlib import Path
from setuptools import setup

def main():
   setup(
      name='password-sanity',
      version='0.2',
      description='Simple, secure, commandline password management',
      author='Dudemanguy',
      author_email='random342@airmail.cc',
      url='https://github.com/Dudemanguy/password-sanity',
      packages=['password-sanity'],
      install_requires=['python-gnupg'],
      scripts=['password-sanity/pws',],
      package_data={'password-sanity': ['completions/bash/pws', 'completions/zsh/_pws']}
   )

if __name__ == '__main__':
    main()
