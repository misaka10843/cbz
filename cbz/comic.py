import zipfile
from datetime import datetime, timezone
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Union, List

import xmltodict

from cbz.constants import XML_NAME, COMIC_FIELDS, PAGE_FIELDS
from cbz.models import ComicModel
from cbz.page import PageInfo
from cbz.utils import repr_attr


class ComicInfo(ComicModel):
    """
    ComicInfo class that represents the comic book information and pages.
    """

    def __init__(self, pages: List[PageInfo], **kwargs):
        """
        Initialize the ComicInfo instance with pages and additional attributes.

        Args:
            pages (List[PageInfo]): List of PageInfo objects representing the comic pages.
            **kwargs: Additional attributes for the comic.

        Attributes:
            pages (List[PageInfo]): Stores the comic pages.
        """
        super(ComicInfo, self).__init__(**kwargs)
        self.pages = pages

    @classmethod
    def from_pages(cls, pages: List[PageInfo], **kwargs) -> 'ComicInfo':
        """
        Create a ComicInfo instance from pages and additional attributes.

        Args:
            pages (List[PageInfo]): List of PageInfo objects representing the comic pages.
            **kwargs: Additional attributes for the comic.

        Returns:
            ComicInfo: An instance of ComicInfo.
        """
        return cls(pages, **kwargs)

    def get_info(self) -> dict:
        """
        Get the comic information as a dictionary.

        Returns:
            dict: Dictionary containing comic information.
        """

        def __info(items: dict, fields: dict) -> dict:
            """
            Extract and convert field information from the provided items and fields.

            Args:
                items (dict): Dictionary containing item attributes.
                fields (dict): Dictionary containing field mappings and types.

            Returns:
                dict: Dictionary with extracted and converted field information.
            """
            content = {}
            for key, (field_key, _) in fields.items():
                item = items.get(key)
                if item and not (isinstance(item, Enum) and item.name == 'UNKNOWN' or item == -1):
                    content[field_key] = repr_attr(item)
            return content

        comic_info = __info(
            items={k: v for k, v in self.__dict__.items() if not k.startswith('_')},
            fields=COMIC_FIELDS)

        comic_pages = []
        for i, page in enumerate(self.pages):
            page_info = __info(
                items={k: v for k, v in page.__dict__.items() if not k.startswith('_')},
                fields=PAGE_FIELDS)
            page_info['@Image'] = i
            comic_pages.append(dict(sorted(page_info.items())))

        # https://github.com/anansi-project/rfcs/issues/3#issuecomment-671631676
        utcnow = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        comic_info.update({
            '@xmlns:xsd': 'http://www.w3.org/2001/XMLSchema',
            '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'FileSize': comic_info.get('FileSize', sum(p.image_size for p in self.pages)),
            'FileCreationTime': comic_info.get('FileCreationTime', utcnow),
            'FileModifiedTime': comic_info.get('FileModifiedTime', utcnow),
            'PageCount': len(self.pages),
            'Pages': {'Page': comic_pages}
        })
        return comic_info

    def pack(self, rename: bool = True) -> bytes:
        """
        Pack the comic information and pages into a CBZ file format.

        Args:
            rename (bool): Whether to rename pages to a sequential format (e.g., 'page-001.jpg').

        Returns:
            bytes: Bytes representing the packed CBZ file.
        """
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zf:
            content = xmltodict.unparse({'ComicInfo': self.get_info()}, pretty=True)
            zf.writestr(
                XML_NAME,
                content.replace('></Page>', ' />').encode('utf-8')
            )
            for i, page in enumerate(self.pages):
                name = page.name
                if not name or rename:
                    name = f'page-{i + 1:03d}{page.suffix}'
                zf.writestr(name, page.content)

        packed = zip_buffer.getvalue()
        zip_buffer.close()
        return packed

    def save(self, path: Union[Path, str]) -> None:
        """
        Save the comic book as a CBZ file to the specified path.

        Args:
            path (Union[Path, str]): Path where the CBZ file will be saved.
        """
        with Path(path).open(mode='wb') as f:
            f.write(self.pack())
