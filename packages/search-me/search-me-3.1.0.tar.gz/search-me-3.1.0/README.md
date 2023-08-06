<p align="center">
    <a href="https://bit.ly/search--me"><img src="https://bit.ly/sm-logo" alt="SEARCH-ME"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/pypi/v/search-me.svg?style=flat-square&logo=appveyor" alt="Version"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/pypi/l/search-me.svg?style=flat-square&logo=appveyor&color=blueviolet" alt="License"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/pypi/pyversions/search-me.svg?style=flat-square&logo=appveyor" alt="Python"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/pypi/status/search-me.svg?style=flat-square&logo=appveyor" alt="Status"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/pypi/format/search-me.svg?style=flat-square&logo=appveyor&color=yellow" alt="Format"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/pypi/wheel/search-me.svg?style=flat-square&logo=appveyor&color=red" alt="Wheel"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://img.shields.io/bitbucket/pipelines/deploy-me/search-me/master?style=flat-square&logo=appveyor" alt="Build"></a>
    <a href="https://pypi.org/project/search-me"><img src="https://bit.ly/sm-cov" alt="Coverage"></a>
    <a href="https://pepy.tech/project/search-me"><img src="https://static.pepy.tech/personalized-badge/search-me?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
    <br><br><br>
</p>

# SEARCH-ME

Search in Google, Bing, Brave, Mojeek, Moose, Yahoo, Searx. See more in [documentation](https://deploy-me.bitbucket.io/search-me/index.html)

## INSTALL

```bash
pip install search-me
```

## USAGE

```python
import asyncio
import logging
import itertools
import aiohttp
from search_me import Google, Bing, Brave, Mojeek, Moose, Yahoo, Searx


logging.basicConfig(level=logging.DEBUG)

s, b, g = Searx(retry=10), Brave(), Google()


async def main():
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers={"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"}
        ) as session:
            results = await asyncio.gather(
                s.search(session=session, q="社會信用體系"),
                b.search(session=session, q="python 3.12"),
                g.search(session=session, q="0x0007ee")
                )
            for x in itertools.chain(*results):
                print(x)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
