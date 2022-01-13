
from setuptools import setup
setup(
    name="efi",
    entry_points={
        "spacy_languages": ["efi = efi:Efik"],
    }
)
