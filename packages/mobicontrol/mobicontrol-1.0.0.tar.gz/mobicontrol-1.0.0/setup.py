from setuptools import setup

setup(
    name="mobicontrol",
    version="1.0.0",
    packages=["mobicontrol", "mobicontrol.cli"],
    include_package_data=True,
    install_requires=["Click", "requests"],
    entry_points={"console_scripts": ["mc = mobicontrol.cli:mobicontrol"]},
)
