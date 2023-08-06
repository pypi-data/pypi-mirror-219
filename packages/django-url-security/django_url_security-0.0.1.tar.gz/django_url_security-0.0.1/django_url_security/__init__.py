"""Django URL Security namespace."""

from importlib_metadata import PackageNotFoundError, version

__author__ = 'Matt Fisher'
__email__ = 'm@ttfisher.com'

# Used to automatically set version number from github actions
# as well as not break when being tested locally
try:
    __version__ = version(__package__)  # type: ignore
except PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
