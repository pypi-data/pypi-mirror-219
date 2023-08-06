"""The async client."""

from http import HTTPStatus
from io import BytesIO
from typing import Final, Self

import xmltodict

try:
    from aiohttp import ClientSession
except ImportError as error:
    msg = "Please install letsbuilda[async] for async support!"
    raise ImportError(msg) from error

from .exceptions import PackageNotFoundError
from .models import JSONPackageMetadata, Package, RSSPackageMetadata


class PyPIServices:
    """A class for interacting with PyPI."""

    NEWEST_PACKAGES_FEED_URL: Final[str] = "https://pypi.org/rss/packages.xml"
    PACKAGE_UPDATES_FEED_URL: Final[str] = "https://pypi.org/rss/updates.xml"

    def __init__(self: Self, http_session: ClientSession) -> None:
        self.http_session = http_session

    async def get_rss_feed(self: Self, feed_url: str) -> list[RSSPackageMetadata]:
        """Get the new packages RSS feed."""
        async with self.http_session.get(feed_url) as response:
            response_text = await response.text()
            rss_data = xmltodict.parse(response_text)["rss"]["channel"]["item"]
            return [RSSPackageMetadata.build_from(package_data) for package_data in rss_data]

    async def get_package_json_metadata(
        self: Self,
        package_title: str,
        package_version: str | None = None,
    ) -> JSONPackageMetadata:
        """Get metadata for a package."""
        if package_version is not None:
            url = f"https://pypi.org/pypi/{package_title}/{package_version}/json"
        else:
            url = f"https://pypi.org/pypi/{package_title}/json"
        async with self.http_session.get(url) as response:
            if response.status == HTTPStatus.NOT_FOUND:
                raise PackageNotFoundError(package_title, package_version)
            return JSONPackageMetadata.from_dict(await response.json())

    async def get_package_metadata(
        self: Self,
        package_title: str,
        package_version: str | None = None,
    ) -> Package:
        """Get metadata for a package."""
        return Package.from_json_api_data(await self.get_package_json_metadata(package_title, package_version))

    async def fetch_bytes(
        self: Self,
        url: str,
    ) -> BytesIO:
        """Fetch bytes from a URL."""
        buffer = BytesIO()
        async with self.http_session.get(url) as response:
            buffer.write(await response.content.read())
        buffer.seek(0)
        return buffer
