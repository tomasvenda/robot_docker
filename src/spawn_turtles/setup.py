from setuptools import find_packages, setup

package_name = 'spawn_turtles'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tomas',
    maintainer_email='tomasreisvenda@gmail.com',
    description='Spawning turtles',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'spawn_turtles = spawn_turtles.client_spawn:main',
        ],
    },
)