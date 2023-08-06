# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weaver']

package_data = \
{'': ['*']}

install_requires = \
['artefactlink>=0.4.1', 'pyarrow>=9,<=12']

setup_kwargs = {
    'name': 'weaver-json',
    'version': '0.0.2',
    'description': 'Serialize and Deserialize Python Classes using JSON',
    'long_description': '# Weaver - Read and Write Python Objects\n\n![Green Python in a Woven Basket](./imgs/PythonImage.png)\n\nWeaver writes Python objects to a JSON format, storing the larger items as binary blobs on the local filesystem. \n\n## Why?\n\nI wanted a way of saving Python objects that could still be examined in a common, human-readable, format, while still containing all the original data.\nAlso it\'s nice to be able to load and save from different versions of a library for breaking changes.\n\n## How?\nSame things as Pickle really. Save all the object state to a dictionary, throw it into JSON. When it comes to load, \ncreate a new object via `__new__` and add the state back in. Then do that recursively both ways. \n\n## What are the requirements for loading them back?\nYou need the same libraries loaded. Maybe not the same versions of those libraries though. If you have a data format \nthat you need to save in one version, and load in the other, you can implement serializers for it;\n\nLet\'s write a serializer for a class that looks like `set` from base python.\n\n```python\nfrom weaver.registry import WeaverSerializer, WeaverRegistry\nfrom weaver.data import WovenClass, ItemMetadataWithVersion\nfrom weaver.version import Version\nfrom my_package import MySet\nfrom typing import Any, Callable\n\nclass WeaverSetSerializer(WeaverSerializer[set]):\n    _metadata = ItemMetadataWithVersion(\n        module=tuple(["MyLibrary"]), name="MySet", version=Version(0, 1, 1)\n    )\n\n    @classmethod\n    def weave(\n            cls,\n            item: MySet,\n            registry: WeaverRegistry,\n            cache: dict[int, Any],\n            weave_fn: Callable,\n    ) -> WovenClass:\n        return WovenClass(\n            pointer=id(item),\n            metadata=cls._metadata,\n            artefacts=set(),\n            documentation={cls._metadata: MySet.__doc__},\n            method_source={},\n            json={"__inner__": [weave_fn(i) for i in item]},\n        )\n```\n\n\nAnd a deserializer on the other side for our custom class that looks a lot like `set`.\n```python\nfrom weaver.registry import WeaverDeserializer, WeaverRegistry\nfrom weaver.data import WovenClass, ItemMetadataWithVersion\nfrom weaver.version import Version\nfrom my_package import MySet\nfrom typing import Any, Callable\n\nclass WeaverSetDeserializer(WeaverDeserializer[MySet]):\n    _metadata = ItemMetadataWithVersion(\n        module=tuple(["MyLibrary"]), name="MySet", version=Version(0, 1, 1)\n    )\n\n    @classmethod\n    def unweave(\n            cls,\n            item: WovenClass,\n            registry: WeaverRegistry,\n            cache: dict[int, Any],\n            unweave_fn: Callable,\n    ) -> MySet:\n        return MySet({unweave_fn(i) for i in item.json["__inner__"]})\n```\n\nSo we can read from Version 0.1.1 and write to Version 0.1.1. We can also specify that we can read from \'AllVersions\', although \nmore complex constraints don\'t exist yet.\n\n### Isn\'t this [Camel](https://github.com/eevee/camel), but for JSON?\nYes, but with tweaks. We fall back to Pickle, they had a clear philosophy against it. ',
    'author': 'Lissa Hyacinth',
    'author_email': 'lissa@shareableai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
