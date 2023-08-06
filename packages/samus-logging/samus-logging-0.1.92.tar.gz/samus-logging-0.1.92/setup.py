from pathlib import Path
from setuptools import setup, find_packages


def read_file(filepath: str) -> str | None:
    if Path(filepath).is_file():
        with open(filepath, 'r') as file:
            content = file.read().strip()
        file.close()

        if len(content) >= 1:
            return content

    return ''


setup(
    name='samus-logging',
    version=read_file(f'VERSION'),
    python_requires='>=3.10',
    package_dir={'': '.'},
    packages=find_packages(where='.'),
    install_requires=[],
    extras_require={'dev': ['twine==4.0.2']},
    license='',  # TODO
    description='A minimal Logging-controller.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Samu Rabin',
    author_email='samus_codes@samusoft.net',
    maintainer='Samu Rabin',
    maintainer_email='samus_codes@samusoft.net',
    url='https://github.com/samuscodes/Samus-Logging',
    download_url='https://github.com/samuscodes/Samus-Logging',
    keywords=['python', 'logging', 'logger', 'minimal'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
