# -*- coding: utf-8 -*-
# Time       : 2023/7/7 3:42
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
from loguru import logger

from clashbyte import ClashMetaAPI
from clashbyte import project, init_log

# 快速生成密钥，添加到 Clash-Verge 外部控制组件
# python -c "import secrets;print(secrets.token_hex())"
CONTROLLER_SECRET = os.environ.get("CLASH_SECRET")
CONTROLLER_URL = "http://127.0.0.1:9090"

cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)

init_log(
    stdout_level="DEBUG",
    error=project.logs.joinpath("error.log"),
    runtime=project.logs.joinpath("runtime.log"),
    serialize=project.logs.joinpath("serialize.log"),
)

clash = ClashMetaAPI(CONTROLLER_SECRET, CONTROLLER_URL)

def write_result(result, fp: Path):
    cache = json.dumps(result, indent=4)
    fp.write_text(cache)


def test_is_alive():
    logger.debug(clash.is_alive)


@logger.catch()
def test_get_dns_query():
    clash.flush_fakeip_cache()
    names = ["www.bilibili.com", "www.baidu.com", "www.google.com", "www.youtube.com"]
    for name in names:
        try:
            result = clash.dns_query(name=name, dns_type="A")
        except httpx.RequestError as err:
            logger.warning("TEST - DNS Query", name=name, err=err)
        else:
            write_result(result, cache_dir.joinpath("dns_query_{name}.json"))
            logger.debug("TEST - DNS Query", name=name, result=result)


def test_get_connections():
    result = clash.connections
    write_result(result, cache_dir.joinpath("connections.json"))
    logger.debug("TEST - Get Connections", conns=result)


def test_get_configs():
    result = clash.configs
    write_result(result, cache_dir.joinpath("configs.json"))
    logger.debug("TEST - GET Configuration", type=type(result), configs=result)


def test_get_proxies():
    result = clash.proxies
    write_result(result, cache_dir.joinpath("proxies.json"))
    logger.info("TEST - GET Proxies", configs=result)
