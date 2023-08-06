from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="material-va-lighthouse",
    version="1.2.1",
    description="A MKDocs plugin which extends the material theme with styles from the VA design system",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Alastair Dawson",
    author_email="alastair.j.dawson@gmail.com",
    license="CC0 1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"material_va_lighthouse": ["va_lighthouse.css", "va_lighthouse_logo.png"]},
    install_requires=[
        "mkdocs==1.4.3",
        "mkdocs-material==8.1.11",
        "mkdocs-techdocs-core==1.1.7",
    ],
    entry_points={
        "mkdocs.plugins": [
            "material-va-lighthouse = material_va_lighthouse.plugin:MaterialVALighthousePlugin"
        ],
    },
)
