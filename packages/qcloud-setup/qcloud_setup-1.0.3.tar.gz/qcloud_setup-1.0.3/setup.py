from setuptools import setup, find_namespace_packages

setup(
    name="qcloud_setup",
    python_requires='>=3.7',
    version="1.0.3",
    url="https://q-chem.com",
    author="Andrew Gilbert",
    author_email="support@q-chem.com",
    description="Utility for setting up Q-Cloud administrators",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(where="src"), 
    package_dir={'qcloud_setup': 'src/qcloud_setup'},
    package_data={'qcloud_setup': ['*.yaml']},
    include_package_data=True,

    install_requires=[
        "boto3==1.21.33",
        "botocore==1.24.33",
        "demjson3==3.0.6",
        "paramiko==3.1.0",
        "pick>=2.2.0",
        "PyYAML>=5.3",
        "pyopenssl>=22.1.0",
        "Requests>=2.27.0",
        "aws-parallelcluster>=3.1.5"
    ],
    scripts=['src/qcloud_setup/qcloud_admin.py'],
)
