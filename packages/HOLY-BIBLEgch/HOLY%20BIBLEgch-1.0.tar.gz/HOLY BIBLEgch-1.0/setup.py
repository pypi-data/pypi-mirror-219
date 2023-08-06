from setuptools import setup

setup(
    name='HOLY BIBLEgch',
    version='1.0',
    packages=['HOLY BIBLEgch'],
    entry_points={
        'console_scripts': [
            'holybible=holy_bible.__main__:main',
        ],
    },
    author='C. Praiseline Christina',
    author_email='praiseline2021@outlook.com',
    description="HOLY BIBLE",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
