import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="klldFN",
    version="1.0.7",
    author="klld",
    description="klldFN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.klld.42web.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'crayons',
          'PirxcyPinger==5.0.0',
          'fortnitepy==3.6.7',
          'BenBotAsync==3.0.1',
          'FortniteAPIAsync==0.1.6',
          'sanic==20.6.3',
          'aiohttp',
          'uvloop',
          'requests'  
      ],
)