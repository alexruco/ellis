from setuptools import setup, find_packages

setup(
    name='ellis',  # This will be the name of your package
    version='0.3',
    packages=find_packages(),
    install_requires=[
        # Add any external dependencies here
        'nltk>=3.6.7,<3.8.0',
        'requests',
        'python-dotenv',  # For environment variable management
        # 'sqlite3' is built-in and should not be listed here
    ],
    entry_points={
        'console_scripts': [
            'ellis-get-history=ellis.main:get_history',
            'ellis-get-messages=ellis.main:get_new_messages',
        ]
    },
    description='A package to handle new emails and retrieve history',
    author='Alex Ruco',
    author_email='alex@ruco.pt',
    url='https://github.com/alexruco/ellis',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
