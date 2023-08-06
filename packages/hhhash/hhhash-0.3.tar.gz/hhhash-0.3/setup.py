# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hhhash']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'hhhash',
    'version': '0.3',
    'description': 'HHHash library is calculate HHHash from HTTP servers.',
    'long_description': '# HTTP Headers Hashing (HHHash)\n\nHTTP Headers Hashing (HHHash) is a technique used to create a fingerprint of an HTTP server based on the headers it returns. HHHash employs one-way hashing to generate a hash value for the set of header keys returned by the server.\n\nFor more details about HHHash background, [HTTP Headers Hashing (HHHash) or improving correlation of crawled content](https://www.foo.be/2023/07/HTTP-Headers-Hashing_HHHash).\n\n## Calculation of the HHHash\n\nTo calculate the HHHash, we concatenate the list of headers returned by the HTTP server. This list is ordered according to the sequence in which the headers appear in the server\'s response. Each header value is separated with `:`. \n\nThe HHHash value is the SHA256 of the list.\n\n## HHHash format\n\n`hhh`:`1`:`20247663b5c63bf1291fe5350010dafb6d5e845e4c0daaf7dc9c0f646e947c29`\n\n`prefix`:`version`:`SHA 256 value`\n\n## Example\n\n### Calculating HHHash from a curl command\n\n~~~\n$ curl -s -D - https://www.circl.lu/ -o /dev/null  | awk \'NR != 1\' | cut -f1 -d: | sed \'/^[[:space:]]*$/d\' | sed -z \'s/\\n/:/g\' | sed \'s/.$//\' | sha256sum | cut -f1 -d " " | awk {\'print "hhh:1:"$1\'}\n~~~\n\nOutput value\n~~~\nhhh:1:78f7ef0651bac1a5ea42ed9d22242ed8725f07815091032a34ab4e30d3c3cefc\n~~~\n\n## Limitations \n\nHHHash is an effective technique; however, its performance is heavily reliant on the characteristics of the HTTP client requests. Therefore, it is important to note that correlations between a set of hashes are typically established when using the same crawler or HTTP client parameters.\n\n### hhhash - Python Library\n\nThe [hhhash package](https://pypi.org/project/hhhash/) can be installed via a `pip install hhhash` or build with Poetry from this repository `poetry build` and `poetry install`.\n\n#### Usage\n\n~~~ipython\nIn [1]: import hhhash\n\nIn [2]: hhhash.buildhash(url="https://www.misp-lea.org", debug=False)\nOut[2]: \'hhh:1:adca8a87f2a537dbbf07ba6d8cba6db53fde257ae2da4dad6f3ee6b47080c53f\'\n\nIn [3]: hhhash.buildhash(url="https://www.misp-project.org", debug=False)\nOut[3]: \'hhh:1:adca8a87f2a537dbbf07ba6d8cba6db53fde257ae2da4dad6f3ee6b47080c53f\'\n\nIn [4]: hhhash.buildhash(url="https://www.circl.lu", debug=False)\nOut[4]: \'hhh:1:334d8ab68f9e935f3af7c4a91220612f980f2d9168324530c03d28c9429e1299\'\n\nIn [5]:\n~~~\n\n## Other libraries\n\n- [c-hhhash](https://github.com/hrbrmstr/c-hhhash) - C++ HTTP Headers Hashing CLI\n- [go-hhhash](https://github.com/hrbrmstr/go-hhhash) - golang HTTP Headers Hashing CLI\n- [R hhhash](https://github.com/hrbrmstr/hhhash) - R library HHHash\n',
    'author': 'Alexandre Dulaunoy',
    'author_email': 'a@foo.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adulau/HHHash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
