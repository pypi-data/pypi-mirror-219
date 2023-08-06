# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scaneo', 'scaneo.cli', 'scaneo.routers', 'scaneo.src', 'scaneo.src.image']

package_data = \
{'': ['*'],
 'scaneo': ['ui/*',
            'ui/_app/*',
            'ui/_app/immutable/assets/*',
            'ui/_app/immutable/chunks/*',
            'ui/_app/immutable/entry/*',
            'ui/_app/immutable/nodes/*',
            'ui/icons/*']}

install_requires = \
['cachetools>=5.3.1,<6.0.0',
 'fastapi>=0.90.0,<0.91.0',
 'geopandas>=0.9.0,<0.10.0',
 'mercantile>=1.2.1,<2.0.0',
 'minio>=7.1.15,<8.0.0',
 'rasterio>=1.2.0,<2.0.0',
 'segment-geospatial>=0.8.4,<0.9.0',
 'shapely>=1.7.1,<2.0.0',
 'typer>=0.9.0,<0.10.0',
 'uvicorn>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['scaneo = scaneo.main:app']}

setup_kwargs = {
    'name': 'scaneo',
    'version': '2023.7.12',
    'description': 'A labelling tool for satellite imagery',
    'long_description': '# scan\n\nThis repo contains the code for SCAN\n\n- scaneo: includes the cli, lib and api\n- ui: includes the web ui\n\nThe CLI runs the API, which in turns servers the static files for the UI.\n\nThe library can be installed with\n\n```\npip install scaneo\n```\n\n## Instructions\n\n### Developement\n\nRun the api with the cli\n\n```\ncd scaneo\npython main.py run --reload --data <<folder>>\n```\n\nThen, run the ui\n\n```\ncd ui\nyarn dev\n```\n\n### Production\n\nBuild the ui, copy the build inside scaneo and build the python package\n\n```\nmake build v=<version>\nmake publish\n```\n\n## Notes\n\nDo not add scaneo/ui to gitignore since the build process will fail (missing entry folder)\n',
    'author': 'earthpulse',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
