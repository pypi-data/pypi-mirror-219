from setuptools import setup, find_packages

setup(
    name='stackviz', 
    version='0.0.18', 
    packages=find_packages(),
    package_data={
        'stackviz': ['stackviz/resources/*'],
    },
    include_package_data=True,
    url='https://github.com/cador/stackviz',
    author='Haolin You',
    author_email='cador.ai@aliyun.com', 
    description='Quick development framework for visualization dashboards based on Python', 
    install_requires=[
        'ipython'
    ],
)
