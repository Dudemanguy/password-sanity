from setuptools import setup
setup(
   name='password-sanity',
   version='0.1',
   description='Simple, secure, commandline password management',
   author='Dudemanguy',
   author_email='random342@airmail.cc',
   url='https://github.com/Dudemanguy/password-sanity',
   packages=['password-sanity'],
   install_requires=['python-gnupg'],
   scripts=[
            'password-sanity/pws',
           ]
)
