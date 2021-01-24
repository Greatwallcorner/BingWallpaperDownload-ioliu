import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    lines = [line.strip() for line in f]
    requirements = [line for line in lines if line and not line.startswith('#')]

setup(
    name='bingwp',
    version='1.1',
    description='download bing.ioliu.cn wallpaper',
    author='heatdesert',
    author_email='wall.corner@outlook.com',
    url='https://github.com/Greatwallcorner/BingWallpaperDownload-ioliu/',
    packages=find_packages(),
    platforms='any',
    license='MIT',
    keywords='bing wallpaper download',
    install_requires=requirements,
    entry_point={
        'console_scripts': [
            'bingwp=ioliu.core:main'
        ]
    }
)
