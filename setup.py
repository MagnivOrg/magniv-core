from setuptools import find_packages, setup

setup(
    name="magniv",
    description="Magniv Core Library",
    author_email="hello@magniv.io",
    url="https://www.magniv.io",
    project_urls={
        "Documentation": "https://docs.magniv.io",
    },
    version="0.1.46",
    py_modules=["magniv"],
    packages=find_packages(),
    install_requires=["Click", "docker", "python-dotenv", "requests"],
    entry_points={
        "console_scripts": [
            "magniv-cli = magniv.scripts.magniv:cli",
        ],
    },
    include_package_data=True,
)
