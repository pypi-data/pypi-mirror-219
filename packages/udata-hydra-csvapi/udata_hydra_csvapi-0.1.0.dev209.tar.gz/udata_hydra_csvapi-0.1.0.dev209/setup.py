# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_tabular']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'sentry-sdk>=1.25.1,<2.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'udata-hydra-csvapi',
    'version': '0.1.0.dev209',
    'description': 'API for CSV converted by udata-hydra',
    'long_description': '# Api-tabular\n\nThis connects to [udata-hydra](https://github.com/etalab/udata-hydra) and serves the converted CSVs as an API.\n\n## Run locally\n\nStart [udata-hydra](https://github.com/etalab/udata-hydra) via `docker compose`.\n\nLaunch this project:\n\n```shell\ndocker compose up\n```\n\nYou can now access the raw postgrest API on http://localhost:8080.\n\nNow you can launch the proxy (ie the app):\n\n```\npoetry install\npoetry run adev runserver -p8005 api_tabular/app.py        # Api related to apified CSV files by udata-hydra\npoetry run adev runserver -p8005 api_tabular/metrics.py    # Api related to udata\'s metrics\n```\n\nAnd query postgrest via the proxy using a `resource_id`, cf below. Test resource_id is `27d469ff-9908-4b7e-a2e0-9439bb38a395`\n\n## API\n\n### Meta informations on resource\n\n```shell\ncurl http://localhost:8005/api/resources/27d469ff-9908-4b7e-a2e0-9439bb38a395/\n```\n\n```json\n{\n  "created_at": "2023-02-11T11:44:03.875615+00:00",\n  "url": "https://data.toulouse-metropole.fr//explore/dataset/boulodromes/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false",\n  "links": [\n    {\n      "href": "/api/resources/27d469ff-9908-4b7e-a2e0-9439bb38a395/profile/",\n      "type": "GET",\n      "rel": "profile"\n    },\n    {\n      "href": "/api/resources/27d469ff-9908-4b7e-a2e0-9439bb38a395/data/",\n      "type": "GET",\n      "rel": "data"\n    }\n  ]\n}\n```\n\n### Profile (csv-detective output) for a resource\n\n```shell\ncurl http://localhost:8005/api/resources/27d469ff-9908-4b7e-a2e0-9439bb38a395/profile/\n```\n\n```json\n{\n  "profile": {\n    "header": [\n        "geo_point_2d",\n        "geo_shape",\n        "ins_nom",\n        "ins_complexe_nom_cplmt",\n        "ins_codepostal",\n        "secteur",\n        "..."\n    ]\n  },\n  "...": "..."\n}\n```\n\n### Data for a resource (ie resource API)\n\n```shell\ncurl http://localhost:8005/api/resources/27d469ff-9908-4b7e-a2e0-9439bb38a395/data/\n```\n\n```json\n{\n  "data": [\n    {\n      "__id": 1,\n      "geo_point_2d": "43.58061543292057,1.401751073689455",\n      "geo_shape": {\n        "coordinates": [\n          [\n              1.401751073689455,\n              43.58061543292057\n            ]\n          ],\n          "type": "MultiPoint"\n        },\n      "ins_nom": "BOULODROME LOU BOSC",\n      "ins_complexe_nom_cplmt": "COMPLEXE SPORTIF DU MIRAIL",\n      "ins_codepostal": 31100,\n      "secteur": "Toulouse Ouest",\n      "quartier": 6.3,\n      "acces_libre": null,\n      "ins_nb_equ": 1,\n      "ins_detail_equ": "",\n      "ins_complexe_nom": "",\n      "ins_adresse": "",\n      "ins_commune": "",\n      "acces_public_horaires": null,\n      "acces_club_scol": null,\n      "ins_nom_cplmt": "",\n      "ins_id_install": ""\n    }\n  ],\n  "links": {\n    "next": "/api/resources/60963939-6ada-46bc-9a29-b288b16d969b/data/?page=2&page_size=1",\n    "prev": null,\n    "profile": "/api/resources/60963939-6ada-46bc-9a29-b288b16d969b/profile/"\n  },\n  "meta": {"page": 1, "page_size": 1, "total": 2}\n}\n```\n\nThis endpoint can be queried with the following operators as query string:\n\n```\n# sort by column\ncolumn_name__sort=asc\ncolumn_name__sort=desc\n\n# contains\ncolumn_name__contains=word\n\n# exacts\ncolumn_name__exact=word\n\n# less\ncolumn_name__less=12\n\n# greater\ncolumn_name__greater=12\n```\n\nPagination is made throught queries with `page` `and page_size`:\n```\ncurl http://localhost:8005/api/resources/27d469ff-9908-4b7e-a2e0-9439bb38a395/data/?page=2&page_size=30\n```\n',
    'author': 'Etalab',
    'author_email': 'opendatateam@data.gouv.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
