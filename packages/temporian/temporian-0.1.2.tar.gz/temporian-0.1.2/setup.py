# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temporian',
 'temporian.beam',
 'temporian.beam.operators',
 'temporian.beam.operators.test',
 'temporian.beam.operators.window',
 'temporian.beam.operators.window.test',
 'temporian.beam.test',
 'temporian.core',
 'temporian.core.data',
 'temporian.core.data.test',
 'temporian.core.operators',
 'temporian.core.operators.binary',
 'temporian.core.operators.calendar',
 'temporian.core.operators.scalar',
 'temporian.core.operators.test',
 'temporian.core.operators.window',
 'temporian.core.test',
 'temporian.implementation',
 'temporian.implementation.numpy',
 'temporian.implementation.numpy.data',
 'temporian.implementation.numpy.data.test',
 'temporian.implementation.numpy.operators',
 'temporian.implementation.numpy.operators.binary',
 'temporian.implementation.numpy.operators.calendar',
 'temporian.implementation.numpy.operators.scalar',
 'temporian.implementation.numpy.operators.test',
 'temporian.implementation.numpy.operators.window',
 'temporian.implementation.numpy.test',
 'temporian.implementation.numpy_cc',
 'temporian.implementation.numpy_cc.operators',
 'temporian.io',
 'temporian.io.test',
 'temporian.proto',
 'temporian.test',
 'temporian.utils',
 'temporian.utils.test']

package_data = \
{'': ['*'],
 'temporian.test': ['test_data/*', 'test_data/io/*', 'test_data/prototype/*']}

install_requires = \
['absl-py>=1.3.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'protobuf>=4.21.12,<5.0.0']

extras_require = \
{'beam': ['apache-beam>=2.48.0,<3.0.0']}

setup_kwargs = {
    'name': 'temporian',
    'version': '0.1.2',
    'description': 'Temporian is a Python package for feature engineering of temporal data, focusing on preventing common modeling errors and providing a simple and powerful API, a first-class iterative development experience, and efficient and well-tested implementations of common and not-so-common temporal data preprocessing functions.',
    'long_description': '<img src="docs/src/assets/banner.png" width="100%" alt="Temporian logo">\n\n[![pypi](https://img.shields.io/pypi/v/temporian?color=blue)](https://pypi.org/project/temporian/)\n[![docs](https://readthedocs.org/projects/temporian/badge/?version=stable)](https://temporian.readthedocs.io/en/stable/?badge=stable)\n![tests](https://github.com/google/temporian/actions/workflows/test.yaml/badge.svg)\n![formatting](https://github.com/google/temporian/actions/workflows/formatting.yaml/badge.svg)\n![publish](https://github.com/google/temporian/actions/workflows/publish.yaml/badge.svg)\n\n**Temporian** is a Python library for **feature engineering** 🛠 and **data augmentation** ⚡ of **temporal data** 📈 (e.g. time-series, transactions) in **machine learning applications** 🤖.\n\n> **Warning**\n> Temporian development is in alpha.\n\n## Key features\n\n- Temporian operates natively on **multivariate** and **multi-index time-series** and **time-sequences** data. With Temporian, all temporal data processing is unified.\n\n- Temporian favors **iterative** and **interactive** development in Colab, where users can **easily visualize intermediate results** 📊 each step of the way.\n\n- Temporian introduces a novel mechanism to **prevent unwanted future leakage** and **training/serving skew** 😰. Temporian programs always return the same result in batch and in streaming mode.\n\n- Temporian programs can run seamlessly **in-process** in Python, on **large datasets using [Apache Beam](https://beam.apache.org/)** ☁️, and in **streaming for continuous** data ingestion.\n\n- Temporian\'s core is implemented **in C++** and **highly optimized** 🔥, so large amounts of data can be handled in-process. In some cases, Temporian can provide a speed-up in the order of 1000x compared to other libraries.\n\n## Installation\n\nTemporian is available on [PyPI](https://pypi.org/project/temporian/). To install it, run:\n\n```shell\npip install temporian\n```\n\n## Minimal example\n\nConsider the following dataset.\n\n```shell\n$ head sales.csv\ntimestamp,store,price,count\n2022-01-01 00:00:00+00:00,CA,27.42,61.9\n2022-01-01 00:00:00+00:00,TX,98.55,18.02\n2022-01-02 00:00:00+00:00,CA,32.74,14.93\n2022-01-02 00:00:00+00:00,TX,48.69,83.99\n...\n```\n\nWe compute the weekly sales per store as follows.\n\n```python\nimport temporian as tp\n\ninput_data = tp.from_csv("sales.csv")\n\n# Define a Temporian program\ninput_node = input_data.node()\nper_store = tp.set_index(input_node, "store")\nweekly_sum = tp.moving_sum(per_store["price"], window_length=tp.duration.days(7))\n\n# Execute Temporian program\noutput_data = weekly_sum.run({input_node: input_data})\n\n# Plot the result\noutput_data.plot()\n```\n\n![](docs/src/assets/frontpage_plot.png)\n\nCheck the [Getting Started tutorial](https://temporian.readthedocs.io/en/stable/tutorials/getting_started/) to try it out!\n\n## Documentation\n\nThe documentation 📚 is available at [temporian.readthedocs.io](https://temporian.readthedocs.io/en/stable/). The [3 minutes to Temporian ⏰️](https://temporian.readthedocs.io/en/stable/3_minutes/) is the best way to start.\n\n## Contributing\n\nContributions to Temporian are welcome! Check out the [contributing guide](CONTRIBUTING.md) to get started.\n\n## Credits\n\nTemporian is developed in collaboration between Google and [Tryolabs](https://tryolabs.com/).\n',
    'author': 'Mathieu Guillame-Bert, Braulio Ríos, Guillermo Etchebarne, Ian Spektor, Richard Stotz',
    'author_email': 'gbm@google.com',
    'maintainer': 'Mathieu Guillame-Bert',
    'maintainer_email': 'gbm@google.com',
    'url': 'https://github.com/google/temporian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}
from config.build import *
build(setup_kwargs)

setup(**setup_kwargs)
