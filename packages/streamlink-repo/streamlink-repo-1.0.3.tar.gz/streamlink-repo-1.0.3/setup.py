from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='streamlink-repo',
    version='1.0.3',
    author='Parrot Developers',
    description='Unofficial Plugin repository implementation for streamlink-cli.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['streamlink_repo'],
    install_requires=[
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