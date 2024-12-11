"""
This type stub file was generated by pyright.
"""

from typing import List
from marimo._runtime.packages.package_manager import CanonicalizingPackageManager, PackageDescription

class CondaPackageManager(CanonicalizingPackageManager):
    name = ...
    docs_url = ...


class PixiPackageManager(CondaPackageManager):
    name = ...
    async def uninstall(self, package: str) -> bool:
        ...

    def list_packages(self) -> List[PackageDescription]:
        ...
