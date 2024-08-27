# setup.py

from setuptools import setup, find_packages

setup(
    name="ellis",
    version="0.1.0",
    description="A package for managing email conversations and storing them in a database.",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "python-dotenv",
        "josephroulin",
    ],
    entry_points={
        "console_scripts": [
            "ellis=ellis.main:get_messages",
        ],
    },
)
