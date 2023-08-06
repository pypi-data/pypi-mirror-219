# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['remarshal']
install_requires = \
['PyYAML>=6.0,<7.0',
 'cbor2>=5.4,<6.0',
 'pytest>=7.4.0,<8.0.0',
 'python-dateutil>=2.8,<3.0',
 'tomlkit>=0.11,<0.12',
 'u-msgpack-python>=2.8,<3.0']

entry_points = \
{'console_scripts': ['cbor2cbor = remarshal:main',
                     'cbor2json = remarshal:main',
                     'cbor2msgpack = remarshal:main',
                     'cbor2toml = remarshal:main',
                     'cbor2yaml = remarshal:main',
                     'json2cbor = remarshal:main',
                     'json2json = remarshal:main',
                     'json2msgpack = remarshal:main',
                     'json2toml = remarshal:main',
                     'json2yaml = remarshal:main',
                     'msgpack2cbor = remarshal:main',
                     'msgpack2json = remarshal:main',
                     'msgpack2msgpack = remarshal:main',
                     'msgpack2toml = remarshal:main',
                     'msgpack2yaml = remarshal:main',
                     'remarshal = remarshal:main',
                     'toml2cbor = remarshal:main',
                     'toml2json = remarshal:main',
                     'toml2msgpack = remarshal:main',
                     'toml2toml = remarshal:main',
                     'toml2yaml = remarshal:main',
                     'yaml2cbor = remarshal:main',
                     'yaml2json = remarshal:main',
                     'yaml2msgpack = remarshal:main',
                     'yaml2toml = remarshal:main',
                     'yaml2yaml = remarshal:main']}

setup_kwargs = {
    'name': 'remarshal',
    'version': '0.15.1',
    'description': 'Convert between CBOR, JSON, MessagePack, TOML, and YAML',
    'long_description': '# Remarshal\n\nConvert between CBOR, JSON, MessagePack, TOML, and YAML. When installed,\nprovides the command line command `remarshal` as well as the short commands\n`{cbor,json,msgpack,toml,yaml}2{cbor,json,msgpack,toml,yaml}`. These commands\ncan be used for format conversion, reformatting, and error detection.\n\n## Known limitations\n\n* CBOR, MessagePack, and YAML with binary fields can not be converted to JSON\nor TOML. Binary fields are converted between CBOR, MessagePack, and YAML.\n* TOML containing values of the\n[Local Date-Time](https://toml.io/en/v1.0.0-rc.1#local-date-time) type can not\nbe converted to CBOR. The Local Date type can only be converted to JSON and\nYAML. The Local Time type can not be converted to any other format. Offset\nDate-Time and its equivalents can be converted between CBOR, MessagePack, TOML,\nand YAML.\n* Date and time types are converted to JSON strings. They can\'t be safely\nroundtripped through JSON.\n* A YAML timestamp with only a date becomes a TOML Local Date-Time for the\nmidnight of that date.\n\n## Installation\n\nYou will need Python 3.8 or later. Earlier versions of Python 3 may work but\nare not supported.\n\nYou can install the latest release from PyPI using pip.\n\n```sh\npython3 -m pip install --user remarshal\n```\n\nAlternatively, clone the `master` branch to install the development version.\nInstall [Poetry](https://github.com/python-poetry/poetry) then run\n\n```sh\ngit clone https://github.com/dbohdan/remarshal\ncd remarshal\npoetry build\npython3 -m pip install --user dist/remarshal-0.??.?-py2.py3-none-any.whl\n```\n\n## Usage\n\n```\nusage: remarshal.py [-h] [-i input] [-o output]\n                    [--if {cbor,json,msgpack,toml,yaml}]\n                    [--of {cbor,json,msgpack,toml,yaml}]\n                    [--indent-json n]\n                    [--yaml-style {,\',",|,>}]\n                    [--wrap key] [--unwrap key]\n                    [--preserve-key-order] [-v]\n                    [input] [output]\n```\n\n```\nusage: {cbor,json,msgpack,toml,yaml}2json [-h] [-i input] [-o output]\n                                          [--indent-json n]\n                                          [--wrap key] [--unwrap key]\n                                          [--preserve-key-order] [-v]\n                                          [input] [output]\n```\n\n```\nusage: {cbor,json,msgpack,toml,yaml}2msgpack [-h] [-i input] [-o output]\n                                             [--wrap key] [--unwrap key]\n                                             [--preserve-key-order] [-v]\n                                             [input] [output]\n```\n\n```\nusage: {cbor,json,msgpack,toml,yaml}2toml [-h] [-i input] [-o output]\n                                          [--wrap key] [--unwrap key]\n                                          [--preserve-key-order] [-v]\n                                          [input] [output]\n```\n\n```\nusage: {cbor,json,msgpack,toml,yaml}2yaml [-h] [-i input] [-o output]\n                                          [--yaml-style {,\',",|,>}]\n                                          [--wrap key] [--unwrap key]\n                                          [--preserve-key-order] [-v]\n                                          [input] [output]\n```\n\n```\nusage: {cbor,json,msgpack,toml,yaml}2cbor [-h] [-i input] [-o output]\n                                          [--wrap key] [--unwrap key]\n                                          [--preserve-key-order] [-v]\n                                          [input] [output]\n```\n\n\nAll of the commands above exit with status 0 on success, 1 on operational\nfailure, and 2 when they fail to parse the command line.\n\nIf no input argument `input`/ `-i input` is given or its value is `-` or\na blank string the data to convert is read from the standard input. Similarly,\nwith no `output`/`-o output` or an output argument that is `-` or a blank\nstring the result of the conversion is written to the standard output.\n\n### Wrappers\n\nThe arguments `--wrap` and `--unwrap` are there to solve the problem of\nconverting CBOR, JSON, MessagePack, and YAML data to TOML if the top-level\nelement of that data is not of a dictionary type (i.e., not a map in CBOR and\nMessagePack, an object in JSON, or an associative array in YAML).\nSuch data can not be represented as TOML directly; it must be wrapped in a\ndictionary first. Passing the flag `--wrap someKey` to `remarshal` or one of\nits short commands wraps the input data in a "wrapper" dictionary with one key,\n"someKey", with the input data as its value. The flag `--unwrap someKey` does\nthe opposite: if it is specified only the value stored under the key "someKey"\nin the top-level dictionary element of the input data is converted to the\ntarget format and output; all other data is ignored. If the top-level element\nis not a dictionary or does not have the key "someKey" then `--unwrap someKey`\nreturns an error.\n\nThe following shell transcript demonstrates the problem and how `--wrap` and\n`--unwrap` solve it:\n\n```\n$ echo \'[{"a":"b"},{"c":[1,2,3]}]\' | ./remarshal.py --if json --of toml\nError: cannot convert non-dictionary data to TOML; use "wrap" to wrap it in a dictionary\n\n$ echo \'[{"a":"b"},{"c":[1,2,3]}]\' \\\n  | ./remarshal.py --if json --of toml --wrap main\n[[main]]\na = "b"\n\n[[main]]\nc = [1, 2, 3]\n\n$ echo \'[{"a":"b"},{"c":[1,2,3]}]\' \\\n  | ./remarshal.py --if json --wrap main - test.toml\n\n$ ./remarshal.py test.toml --of json\n{"main":[{"a":"b"},{"c":[1,2,3]}]}\n\n$ ./remarshal.py test.toml --of json --unwrap main\n[{"a":"b"},{"c":[1,2,3]}]\n```\n\n## Examples\n\n```\n$ ./remarshal.py example.toml --of yaml\nclients:\n  data:\n  - - gamma\n    - delta\n  - - 1\n    - 2\n  hosts:\n  - alpha\n  - omega\ndatabase:\n  connection_max: 5000\n  enabled: true\n  ports:\n  - 8001\n  - 8001\n  - 8002\n  server: 192.168.1.1\nowner:\n  bio: \'GitHub Cofounder & CEO\n\n    Likes tater tots and beer.\'\n  dob: 1979-05-27 07:32:00+00:00\n  name: Tom Preston-Werner\n  organization: GitHub\nproducts:\n- name: Hammer\n  sku: 738594937\n- color: gray\n  name: Nail\n  sku: 284758393\nservers:\n  alpha:\n    dc: eqdc10\n    ip: 10.0.0.1\n  beta:\n    country: 中国\n    dc: eqdc10\n    ip: 10.0.0.2\ntitle: TOML Example\n\n$ curl -s http://api.openweathermap.org/data/2.5/weather\\?q\\=Kiev,ua \\\n  | ./remarshal.py --if json --of toml\nbase = "cmc stations"\ncod = 200\ndt = 1412532000\nid = 703448\nname = "Kiev"\n\n[clouds]\nall = 44\n\n[coord]\nlat = 50.42999999999999972\nlon = 30.51999999999999957\n\n[main]\nhumidity = 66\npressure = 1026\ntemp = 283.49000000000000909\ntemp_max = 284.14999999999997726\ntemp_min = 283.14999999999997726\n\n[sys]\ncountry = "UA"\nid = 7358\nmessage = 0.24370000000000000\nsunrise = 1412481902\nsunset = 1412522846\ntype = 1\n\n[[weather]]\ndescription = "scattered clouds"\nicon = "03n"\nid = 802\nmain = "Clouds"\n\n[wind]\ndeg = 80\nspeed = 2\n```\n\n## License\n\nMIT. See the file `LICENSE`.\n\n`example.toml` from <https://github.com/toml-lang/toml>. `example.json`,\n`example.msgpack`, `example.cbor`, `example.yml`, `tests/bin.msgpack`,\nand `tests/bin.yml` are derived from it.\n',
    'author': 'D. Bohdan',
    'author_email': 'dbohdan@dbohdan.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/remarshal-project/remarshal',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
