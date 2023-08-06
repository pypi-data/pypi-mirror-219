# setup.py
from setuptools import setup

setup(
    name="lensauto",
    version="0.1",
    packages=["lensauto"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        lensauto=lensauto.cli:main
    """,
)
