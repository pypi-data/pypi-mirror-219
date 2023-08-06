# from distutils.core import setup
from setuptools import setup, find_packages
version = '1.4'
setup(
    # How you named your package folder (MyLib)
    name='maxia_pipedrive',
    packages=find_packages(),   # Chose the same as "name"
    version=version,      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Maxia Pipedrive API handler',
    author='Max.ia Education',                   # Type in your name
    author_email='luiz@maxia.education',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Max-ia-Education/maxia_pipedrive_api',
    # I explain this later on
    download_url=f'https://github.com/Max-ia-Education/maxia_pipedrive_api/archive/refs/tags/v1.3.tar.gz',
    #   keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'numpy',
        'pandas',
        'tqdm'
    ],
    classifiers=[
        #     # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        #     # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        #     # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
