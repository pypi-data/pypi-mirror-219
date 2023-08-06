from setuptools import setup, find_packages
setup(
    name = 'antgen',
    packages = find_packages(),
    # Non-python files to include in pypi
    package_data={'antgen': ['requirements.txt', 'antgen/mapping.conf', 'antgen/default.conf']},
    include_package_data=True,
)