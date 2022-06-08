from setuptools import setup, find_packages

try:
    with open("proj_description.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except:
    long_description = ""

setup(
    name="magniv",
    description="Magniv Core Library",
    author_email="hello@magniv.io",
    url="https://www.magniv.io",
    project_urls={"Documentation": "https://docs.magniv.io",},
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.36",
    py_modules=["magniv"],
    packages=find_packages(),
    install_requires=["Click", "docker"],
    entry_points={"console_scripts": ["magniv-cli = magniv.scripts.magniv:cli",],},
    include_package_data=True,
)
