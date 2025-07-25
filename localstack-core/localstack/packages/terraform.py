import os
import platform
from typing import List

from localstack.packages import InstallTarget, Package
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.utils.files import chmod_r
from localstack.utils.platform import get_arch

TERRAFORM_VERSION = os.getenv("TERRAFORM_VERSION", "1.5.7")
TERRAFORM_URL_TEMPLATE = (
    "https://releases.hashicorp.com/terraform/{version}/terraform_{version}_{os}_{arch}.zip"
)
TERRAFORM_CHECKSUM_URL_TEMPLATE = (
    "https://releases.hashicorp.com/terraform/{version}/terraform_{version}_SHA256SUMS"
)


class TerraformPackage(Package["TerraformPackageInstaller"]):
    def __init__(self) -> None:
        super().__init__("Terraform", TERRAFORM_VERSION)

    def get_versions(self) -> List[str]:
        return [TERRAFORM_VERSION]

    def _get_installer(self, version: str) -> "TerraformPackageInstaller":
        return TerraformPackageInstaller("terraform", version)


class TerraformPackageInstaller(ArchiveDownloadAndExtractInstaller):
    def _get_install_marker_path(self, install_dir: str) -> str:
        return os.path.join(install_dir, "terraform")

    def _get_download_url(self) -> str:
        system = platform.system().lower()
        arch = get_arch()
        return TERRAFORM_URL_TEMPLATE.format(version=TERRAFORM_VERSION, os=system, arch=arch)

    def _install(self, target: InstallTarget) -> None:
        super()._install(target)
        chmod_r(self.get_executable_path(), 0o777)  # type: ignore[arg-type]

    def _get_checksum_url(self) -> str | None:
        return TERRAFORM_CHECKSUM_URL_TEMPLATE.format(version=TERRAFORM_VERSION)


terraform_package = TerraformPackage()
