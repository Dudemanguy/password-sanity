import sys
from pathlib import Path
from setuptools import setup

def get_completions():
   data_files = []
   bash_dir = Path(sys.prefix) / "share" / "bash-completion" / "completions"
   zsh_dir = Path(sys.prefix) / "share" / "zsh" / "site-functions"
   if bash_dir.is_dir():
      data_files.append((str(bash_dir), ["completions/bash/pws"]))
   if zsh_dir.is_dir():
      data_files.append((str(zsh_dir), ["completions/zsh/_pws"]))
   return data_files

def main():
   completions = get_completions()

   setup(
      name='password-sanity',
      version='0.1',
      description='Simple, secure, commandline password management',
      author='Dudemanguy',
      author_email='random342@airmail.cc',
      url='https://github.com/Dudemanguy/password-sanity',
      packages=['password-sanity'],
      install_requires=['python-gnupg'],
      scripts=['password-sanity/pws',],
      data_files = completions
   )

if __name__ == '__main__':
    main()
