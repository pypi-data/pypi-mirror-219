# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['train_lib',
 'train_lib.clients',
 'train_lib.clients.fhir',
 'train_lib.docker_util',
 'train_lib.security',
 'train_lib.tests']

package_data = \
{'': ['*']}

install_requires = \
['cryptography',
 'docker',
 'fhir-kindling',
 'loguru',
 'pandas',
 'pendulum',
 'requests',
 'requests_oauthlib']

setup_kwargs = {
    'name': 'pht-train-container-library',
    'version': '2.0.6',
    'description': 'Python library for handling containerized PHT trains',
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/train-container-library/badge/?version=latest)](https://train-container-library.readthedocs.io/en/latest/?badge=latest)\n[![CodeQL](https://github.com/PHT-Medic/train-container-library/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/PHT-Medic/train-container-library/actions/workflows/codeql-analysis.yml)\n[![main-ci](https://github.com/PHT-EU/train-container-library/actions/workflows/main.yml/badge.svg)](https://github.com/PHT-EU/train-container-library/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/PHT-Medic/train-container-library/branch/master/graph/badge.svg?token=11RYRZK2FO)](https://codecov.io/gh/PHT-Medic/train-container-library)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pht-train-container-library)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/pht-train-container-library)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# &#128646; Train Container Library\n\nPython library for validating and interacting with pht-train images/containers.\n\n## Installation\n\n```shell\npip install pht-train-container-library\n```\n\n\n## Setup development environment\nMake sure you have [poetry](https://python-poetry.org/docs/#installation) and [pre-commit](https://pre-commit.com/#install) installed.\n\nInstall the dependencies and pre-commit hooks:\n```shell\npoetry install --with dev\n```\n\n```shell\npoetry run pre-commit install\n```\n\n### Run tests\n\n```shell\npoetry run pytest\n```\n\n### Linting and formatting\n\nThese commands are also run as pre-commit hooks.\n\nLinting with ruff:\n```shell\npoetry run ruff . --fix\n```\n\nFormatting with black:\n```shell\npoetry run black .\n```\n\n## Security Protocol\n\nThe pht security protocol adapted from `docs/Secure_PHT_latest__official.pdf` performs two main tasks:\n\n1. Before executing a train-image on the local machine, unless the station is the first station on the route, the\n   previous results need to be decrypted and the content of the image needs to be validated based on the configuration\n   of the individual train -> `pre-run`.\n2. After executing the train the updated results need to be encrypted and the train configuration needs to be updated to\n   reflect the current state ->`post-run`.\n\n### Train image structure\n\nTo ensure the protocol is working correctly train docker images are required to keep the following structure:\n\n- `/opt/train_config.json`: Stores the configuration file of the train.\n- `/opt/pht_train/`: Stores all the files containing code or other things required for the train algorithm to run. The\n  contents of this directory can never change and is validated by the `pre-run` step.\n- `/opt/pht_results/`: Stores the results of the train. Which will be decrypted in the `pre-run` step and encrypted in\n  the `post-run` step.\n\nNo files in the image outside the `/opt/pht_results/` directory should change during the execution of the algorithm.\n\n### Usage - Python Script\n\nTo use the protocol in your own python application, after installing the library\nwith `pip install pht-train-container-library` an instance of the protocol can be to validate docker images as follows:\n\n```python\nfrom train_lib.security.protocol import SecurityProtocol\nfrom train_lib.docker_util.docker_ops import extract_train_config\n\nimage_name = '<image-repo>:<image-tag>'\nstation_id = '<station-id>'\n\n# Get the train configuration from the image\nconfig = extract_train_config(image_name)\n# Initialize the protocol with the extracted config and station_id\nprotocol = SecurityProtocol(station_id=station_id, config=config)\n\n# execute one of the protocol steps\nprotocol.pre_run_protocol(image_name, private_key_path='<path-to-private-key>')\n# protocol.post_run_protocol(image_name, private_key_path='<path-to-private-key>')\n```\n\n### Usage - Container\n\nA containerized version of the protocol is also available it can be used with the following command:\n\n```shell\ndocker run -e STATION_ID=<station_id> -e PRIVATE_KEY_PATH=/opt/private_key.pem -v /var/run/docker.sock:/var/run/docker.sock -v <path_to_your_key>:/opt/private_key.pem ghcr.io/pht-medic/protocol <pre-run/post-run> <image-repo>:<image-tag>\n```\n\n`STATION_ID` and `PRIVATE_KEY_PATH` are required to be set in the environment variables. As well as passing the docker\nsocket `/var/run/docker.sock` to the container as a volume to enable docker-in-docker functionality.\n\n### Pre-run protocol\n\nThe pre-run protocol consists of the following steps\n\n1. The hash of the immutable files (train definition) is verified making sure that the executable files did not change\n   during the the train definition.\n2. The digital signature is verified ensuring the correctness of the results at each stop of the train.\n3. The symmetric key is decrypted using the provided station private key\n4. The mutable files in `/opt/pht_results` are decrypted using the symmetric key obtained in the previous step\n5. The decrypted files are hashed and the hash is compared to the one stored in the train configuration file.\n\nOnce these steps have been completed the image is ready to be executed.\n\n### Post-run protocol\n\n1. Calculate the hash of the newly generated results\n2. Sign the hash of the results using the provided `PRIVATE_KEY_PATH`\n3. Update the the train signature using the session id that is randomly generated at each execution step\n4. Encrypt the resulting files using a newly generated symmetric key\n5. Encrypt the generated symmetric key with the public keys of the train participants\n6. Update the train configuration file\n\nWith the completion of these steps the train is ready to be pushed into the registry for further processing\n\n## Tests\n\nRun the tests to validate the security protocol is working as intended. From this projects root directory run\n`pytest train_lib`\n\n\n\n\n\n\n\n",
    'author': 'Michael Graf',
    'author_email': 'michael.graf@uni-tuebingen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
