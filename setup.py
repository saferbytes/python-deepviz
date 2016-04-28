import setuptools

setuptools.setup(
        name='python-deepviz',
        version='1.2.0',
        author='Saferbytes',
        author_email='info@saferbytes.it',
        url="https://github.com/saferbytes/python-deepviz",
        description='Deepviz Threat Intelligence API Client Library for python',
        keywords="deepviz API SDK",
        license='MIT',
        packages=['deepviz'],
        install_requires=[
            'requests>=2.5.1',
            'simplejson>=3.8.1'
        ]
)