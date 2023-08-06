from setuptools import setup
setup(
  name = 'upstox',
  packages = ['upstox_api', 'upstox_api.constants'],
  version = '2.0.3',
  include_package_data=True,
  description = 'DEPRECATED - Official Python library for Upstox APIs',
  long_description = 'DEPRECATED - The Upstox Python SDK is in its end-of-life stage and has been deprecated. We strongly encourage you to transition to the updated package, upstox-python-sdk. This can be installed via pip install upstox-python-sdk (find further details at https://pypi.org/project/upstox-python-sdk/). The new package ensures full compatibility with Upstox API v2.0, as well as subsequent versions, and will receive ongoing updates and support.',
  author = 'Upstox Development Team',
  author_email = 'support@upstox.com',
  url = 'https://github.com/upstox/upstox-python',
  install_requires=['future', 'requests', 'websocket_client'],
  keywords = ['upstox', 'python', 'sdk', 'trading', 'stock markets'],
  classifiers=[
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
)