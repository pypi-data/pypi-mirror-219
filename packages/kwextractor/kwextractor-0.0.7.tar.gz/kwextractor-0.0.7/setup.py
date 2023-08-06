from pathlib import Path
from kwextractor.version import get_kwextractor_version
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text(encoding='utf-8')

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="kwextractor",
    version=get_kwextractor_version(),
    packages=find_packages(
        include=['kwextractor', 'kwextractor.*']
    ),
    install_requires=requirements,
    package_dir={'kwextractor': 'kwextractor'},
    package_data={
        'kwextractor':['data/*'],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    description="Extract keywords for vietnamese text.",
    author="Trinh Do Duy Hung",
    author_email="trinhhungsss492@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
