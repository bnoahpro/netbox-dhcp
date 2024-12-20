from setuptools import find_packages, setup

setup(
    name='netbox-dhcp',
    version='0.1',
    description='Manage Dnsmasq DHCP with NetBox',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)