from distutils.core import setup
setup(
  name = 'jaime38130',         # How you named your package folder (MyLib)
  packages = ['jaime38130'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='-',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'second package test',   # Give a short description about your library
  author = 'Jaime Silva',                   # Type in your name
  author_email = 'jaimedcsilva@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JaimeSilva/jaime38130/archive/refs/tags/v_02.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
