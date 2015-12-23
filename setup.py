import setuptools

setuptools.setup(
        name='python-deepviz',
        version='1.0.0',
        author='Saferbytes',
        author_email='info@saferbytes.it',
        url='https://www.deepviz.com/',
        description='Deepviz API Client Library',
        keywords="deepviz api sdk",
        license='MIT',
        packages=['deepviz'],
        install_requires=[
            'requests>=2.5.1',
            'simplejson>=3.8.1'
        ]
)
