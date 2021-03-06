from setuptools import setup

setup(
    name='tinyserv',
    description="A tiny http server to transfer files between computers.",
    version='0.0.0',
    packages=['tinyserv'],
    scripts=['scripts/tinyserv'],
    include_package_data=True,
    install_requires=['Jinja2>=2.11.2,<2.12.0', 'segno==1.3.1', 'zipstream-new==1.1.8'],
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
)
