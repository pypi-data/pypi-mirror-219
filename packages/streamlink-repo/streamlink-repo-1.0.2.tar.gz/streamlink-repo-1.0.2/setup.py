from setuptools import setup

setup(
    name='streamlink-repo',
    version='1.0.2',
    author='Parrot Developers',
    description='Unofficial Plugin repository implementation for streamlink-cli.',
    packages=['streamlink_repo'],
    install_requires=[
        'streamlink',  # Add any dependencies here
        'pyinquirer',
        'colorama',
        'tqdm',
        # Add more dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'streamlink-repo = streamlink_repo:app'
        ]
    },
)