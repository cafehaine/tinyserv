from setuptools import setup

setup(
    name="tinyserv",
    description="A tiny http server to transfer files between computers.",
    version="0.0.0",
    packages=["tinyserv"],
    scripts=["scripts/tinyserv"],
    install_requires=["Jinja2>=2.11.2,<2.12.0"],
    license='GPLv3',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3',
    ],
)
