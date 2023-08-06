import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgn2neo4j",
    version="0.0.2",
    description="Convert chess games (PGN:s) to a Neo4j database",
    author="Anton Forsman",
    url="https://github.com/chess-opening-trainer/pgn2neo4j",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"pgn2neo4j":"./pgn2neo4j/src"},
    py_modules=["pgn2neo4j"],
    packages=["pgn2neo4j"],
    python_requires='>=3.6',
    install_requires=[
        "tqdm",
        "chess",
    ]
)