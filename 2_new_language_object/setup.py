
from setuptools import setup
setup(
    name="efk",
    entry_points={
        "spacy_languages": ["efk = efk:Efik"],
    }
)
