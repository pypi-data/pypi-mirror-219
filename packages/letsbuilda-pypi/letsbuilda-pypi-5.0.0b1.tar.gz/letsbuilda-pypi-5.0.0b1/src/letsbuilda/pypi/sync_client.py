"""The sync client."""

from http import HTTPStatus
from io import BytesIO
from typing import Final, Self

import xmltodict
from requests import Session

from .exceptions import PackageNotFoundError
from .models import JSONPackageMetadata, Package, RSSPackageMetadata


class PyPIServices:
    """A class for interacting with PyPI."""

    NEWEST_PACKAGES_FEED_URL: Final[str] = "https://pypi.org/rss/packages.xml"
    PACKAGE_UPDATES_FEED_URL: Final[str] = "https://pypi.org/rss/updates.xml"

    def __init__(self: Self, http_session: Session) -> None:
        self.http_session = http_session

    def get_rss_feed(self: Self, feed_url: str) -> list[RSSPackageMetadata]:
        """Get the new packages RSS feed."""
        response_text = self.http_session.get(feed_url).text
        rss_data = xmltodict.parse(response_text)["rss"]["channel"]["item"]
        return [RSSPackageMetadata.build_from(package_data) for package_data in rss_data]

    def get_package_json_metadata(
        self: Self,
        package_title: str,
        package_version: str | None = None,
    ) -> JSONPackageMetadata:
        """Get metadata for a package."""
        if package_version is not None:
            url = f"https://pypi.org/pypi/{package_title}/{package_version}/json"
        else:
            url = f"https://pypi.org/pypi/{package_title}/json"
        response = self.http_session.get(url)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise PackageNotFoundError(package_title, package_version)
        return JSONPackageMetadata.from_dict(response.json())

    def get_package_metadata(
        self: Self,
        package_title: str,
        package_version: str | None = None,
    ) -> Package:
        """Get metadata for a package."""
        return Package.from_json_api_data(self.get_package_json_metadata(package_title, package_version))

    def fetch_bytes(
        self: Self,
        url: str,
    ) -> BytesIO:
        """Fetch bytes from a URL."""
        response = self.http_session.get(url)
        buffer = BytesIO(response.content)
        buffer.seek(0)
        return buffer
