from setuptools import setup, find_packages

setup(
    name="langchain_model",
    version="0.0.4",
    description="Populate Pydantic Models with LangChain",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        "langchain",
        "pydantic<2",
    ],
)
