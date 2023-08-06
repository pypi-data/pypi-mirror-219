# """Collect backports and version-dependent imports in a single module."""
# import sys

# if sys.version_info >= (3, 11):
#     import tomllib  # pylint: disable=no-member,unused-import
# else:
#     import tomli as tomllib  # pylint: disable=W0611

# if sys.version_info >= (3, 8):
#     from typing import Literal  # pylint: disable=no-member,unused-import
# else:
#     from typing_extensions import Literal

# if sys.version_info >= (3, 11):
#     from typing import Self  # pylint: disable=no-member,unused-import
# else:
#     from typing_extensions import Self

# # importlib.metadata.packages_distributions() was introduced in v3.10, but it
# # is not able to infer import names for modules lacking a top_level.txt until
# # v3.11. Hence we prefer importlib_metadata in v3.10 as well as pre-v3.10.
# if sys.version_info >= (3, 11):
#     import importlib.metadata as importlib_metadata
# else:
#     import importlib_metadata
# packages_distributions = importlib_metadata.packages_distributions
