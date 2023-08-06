from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'grassmanntn',         # How you named your package folder (MyLib)
  packages = ['grassmanntn'],   # Chose the same as "name"
  version = '1.2.2',      # Start with a small number and increase it with every change you make
  license='Apache',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a Python library for Grassmann tensor network computation',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Atis Yosprakob',                   # Type in your name
  author_email = 'yosprakob2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ayosprakob/grassmanntn',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ayosprakob/grassmanntn/archive/refs/tags/v_122.tar.gz',    # I explain this later on
  keywords = ['physics', 'lattice', 'gauge theory', 'tensor network', 'grassmann'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'sparse',
          'opt_einsum',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
  ],
)
