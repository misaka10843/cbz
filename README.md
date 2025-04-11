# CBZ

This repository optimizes some of the content of the upstream repository for features such as better compression

## Compare upstream repository modifications

- Remove superfluous functionality and just compress it
- Optimized series number with support for floating points

## Installation

Install cbz from GitHub using git:

```shell
pip install git+https://github.com/misaka10843/cbz.git
```

or use mirrors:

```shell
pip install git+https://ghproxy.net/https://github.com/misaka10843/cbz.git
```

## Quick Start

Here's a quick example of how to create a CBZ file from a series of images:

````python
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
from cbz.page import PageInfo

PARENT = Path(__file__).parent

if __name__ == '__main__':
    paths = list(Path('path/to/your/images').iterdir())

    # Load each page from the 'images' folder into a list of PageInfo objects
    pages = [
        PageInfo.load(
            path=path,
            type=PageType.FRONT_COVER if i == 0 else PageType.BACK_COVER if i == len(paths) - 1 else PageType.STORY
        )
        for i, path in enumerate(paths)
    ]

    # Create a ComicInfo object using ComicInfo.from_pages() method
    comic = ComicInfo.from_pages(
        pages=pages,
        title='Your Comic Title',
        series='Your Comic Series',
        number=1,
        language_iso='en',
        format=Format.WEB_COMIC,
        black_white=YesNo.NO,
        manga=Manga.NO,
        age_rating=AgeRating.PENDING
    )

    # Pack the comic book content into a CBZ file format
    cbz_content = comic.pack()

    # Define the path where the CBZ file will be saved
    cbz_path = PARENT / 'your_comic.cbz'

    # Write the CBZ content to the specified path
    cbz_path.write_bytes(cbz_content)
````

## Detailed Usage

### Creating a ComicInfo Object

The `ComicInfo` class represents a comic book with metadata and pages. It supports initialization from a list of `PageInfo` objects:

```python
from cbz.comic import ComicInfo
from cbz.page import PageInfo

# Example usage:
pages = [
    PageInfo.load(path='/path/to/page1.jpg', type=PageType.FRONT_COVER),
    PageInfo.load(path='/path/to/page2.jpg', type=PageType.STORY),
    PageInfo.load(path='/path/to/page3.jpg', type=PageType.BACK_COVER),
]

comic = ComicInfo.from_pages(
    pages=pages,
    title='My Comic',
    series='Comic Series',
    number=1,
    language_iso='en',
    format=Format.WEB_COMIC,
    black_white=YesNo.NO,
    manga=Manga.NO,
    age_rating=AgeRating.PENDING
)
```

### Packing into CBZ Format

Pack the comic into a CBZ file format:

```python
cbz_content = comic.pack()
```

## Contributors

<a href="https://github.com/hyugogirubato"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/65763543?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="hyugogirubato"/></a>
<a href="https://github.com/piskunqa"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/38443069?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="piskunqa"/></a>
<a href="https://github.com/OleskiiPyskun"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/75667382?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="OleskiiPyskun"/></a>
<a href="https://github.com/domenicoblanco"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/9018104?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="domenicoblanco"/></a>
<a href="https://github.com/RivMt"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/40086827?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="RivMt"/></a>
<a href="https://github.com/flolep2607"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/24566964?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="flolep2607"/></a>
<a href="https://github.com/gokender"><img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/3709740?v=4&h=25&w=25&fit=cover&mask=circle&maxage=7d" alt="gokender"/></a>


## Licensing

This software is licensed under the terms of [MIT License](https://github.com/hyugogirubato/cbz/blob/main/LICENSE).  
You can find a copy of the license in the LICENSE file in the root folder.

* * * 

© hyugogirubato 2024