from setuptools import find_packages, setup


def get_long_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="EyeTrackFatigue",
    version="0.2.3",
    description="EyeTrackFatigue description",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="...",
    author_email="anton.mamonov.golohvastogo@mail.ru",
    url="https://github.com/AI-group-72/FAEyeTON",
    project_urls={
        "GitHub Project": "https://github.com/AI-group-72/FAEyeTON",
        "Issue Tracker": "https://github.com/AI-group-72/FAEyeTON/Meta/issues",
    },
    packages=['EyeTrackFatigue', 'EyeTrackFatigue.Analise',
              'EyeTrackFatigue.DeviceManager', 'EyeTrackFatigue.Input'],
    install_requires=[''],
    keywords=[
        "EyeTrackFatigue",
    ],
    license="MIT",
)


'''
find_packages(
        include=["DeviceManager", "DeviceManager.*",
                 "Input", "Input.*",
                 "Analise", "Analise.*",
                 "Emulate", "Emulate.*",
                 "Evaluate", "Evaluate.*",
                 "UI.DataGather"],
    ),



package_data={
    "EyeTrackFatigue_client": ["data/*.cfg"],
    },
    install_requires=[
        "requests==2.27.1",
    ],
    setup_requires=[
        "pytest-runner",
        "flake8==4.0.1",
    ],
    tests_require=[
        "pytest==7.1.2",
        "requests-mock==1.9.3",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
'''

'''from setuptools import setup, find_packages

import json
import os

def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]

if __name__ == '__main__':
    setup(
        name='ETF',
        version=os.getenv('PACKAGE_VERSION', '0.2.dev0'),
        package_dir={'': 'src'},
        packages=find_packages('Analise', include=[
            '*.py'
        ]),
        description='A demo package.',

    )
install_requires=[
              *read_pipenv_dependencies('Analise.ParsedData'),
        ]

'''
