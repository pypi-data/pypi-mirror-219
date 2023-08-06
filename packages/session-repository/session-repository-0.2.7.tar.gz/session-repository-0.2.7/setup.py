from setuptools import setup

version = "0.2.7"

setup(
    name="session-repository",
    version=version,
    packages=[
        "session_repository",
    ],
    install_requires=[
        "sqlalchemy==1.4.41",
    ],
    license="MIT",
    author="Maxime MARTIN",
    author_email="maxime.martin02@hotmail.fr",
    description="A project to have a base repository class to permform select/insert/update/delete with dynamtic syntaxe",
    url="https://github.com/Impro02/session-repository",
    download_url="https://github.com/Impro02/session-repository/archive/refs/tags/%s.tar.gz"
    % version,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
