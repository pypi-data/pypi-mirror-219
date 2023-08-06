import setuptools

setuptools.setup(
    name="qcloud_user",
    python_requires='>=3.7',
    version="1.0.3",
    url="https://q-chem.com",
    author="Andrew Gilbert",
    author_email="suppor@q-chem.com",
    description="CLI for interacting with Q-Cloud clusters",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['qcloud_user'],
    package_dir={'qcloud_user': 'src/qcloud_user'},

    install_requires=[
        "boto3==1.21.33",
        "botocore==1.24.33",
        "demjson3==3.0.6",
        "paramiko==3.1.0",
        "pick>=2.2.0",
        "PyYAML>=5.3",
        "python-jose>=3.3.0",
        "pyopenssl>=22.1.0",
        "jose>=1.0",
        "Requests==2.31.0",
    ],
    scripts=['src/qcloud_user/qcloud_user.py'],
)
