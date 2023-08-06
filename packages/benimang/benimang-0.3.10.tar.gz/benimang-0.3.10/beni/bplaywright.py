import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from playwright.async_api import async_playwright
from playwright.sync_api import BrowserContext, sync_playwright

from beni import bpath
from beni.btype import Null

_context: BrowserContext = Null


def run(*, url: str = '', storage_state: str | Path | None = None):
    global _context
    if not _context:
        import nest_asyncio
        nest_asyncio.apply()
        os.environ['PWDEBUG'] = 'console'
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False, channel='chrome')
        _context = browser.new_context(storage_state=storage_state)
    page = _context.new_page()
    if url:
        page.goto(url)
    return page


def save_storage_state(storage_state: str | Path | None = None):
    if _context:
        _context.storage_state(path=storage_state or bpath.desktop('storage_state.dat'))


@asynccontextmanager
async def page(
    *,
    browser: dict[str, Any] = {},
    context: dict[str, Any] = {},
    page: dict[str, Any] = {},
):
    '''```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    },
    context={
        'storage_state': STATE_FILE,
    },
    ```'''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            async with await b.new_context(**context) as c:
                async with await c.new_page(**page) as p:
                    yield p


@asynccontextmanager
async def context(
    *,
    browser: dict[str, Any] = {},
    context: dict[str, Any] = {},
):
    '''```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    },
    context={
        'storage_state': STATE_FILE,
    },
    ```'''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            async with await b.new_context(**context) as c:
                yield c


@asynccontextmanager
async def browser(
    *,
    browser: dict[str, Any] = {},
):
    '''```py
    browser={
        'headless': False,    # 显示浏览器UI
        'channel': 'chrome',  # 使用系统 Chrome 浏览器
    }
    ```'''
    async with async_playwright() as p:
        async with await p.chromium.launch(**browser) as b:
            yield b
