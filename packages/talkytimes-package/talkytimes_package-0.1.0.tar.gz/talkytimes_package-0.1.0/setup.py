import setuptools

setuptools.setup(
    name='talkytimes_package',
    author='Steven Correa',
    author_email='brayancorrea78@gmail.com',
    description='Talkytimes package',
    url='https://github.com/Steven339/talkytimes-package',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.10',
    install_requires=[
        "selenium==4.10.0",
        "beautifulsoup4==4.12.2",
        "html5lib==1.1"
        "boto3==1.28.3"
    ]
)
