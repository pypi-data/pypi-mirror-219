from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    
    name="testmedium",  # Required
    
    version="2.0.0",  # Required
    
    description="A sample Python project",  # Optional
    
    long_description=long_description,  # Optional
    
    long_description_content_type="text/markdown",  # Optional (see note above)

    # package_dir={"": "src"},  # Optional
 
    # packages=find_packages(where="src"),  # Required
    
    packages = ['testmedium',],
    
    python_requires=">=3.7",
    
    install_requires=["mysql-connector-python"],  # Optional
)


