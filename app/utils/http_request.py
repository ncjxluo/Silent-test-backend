# -*- coding: utf-8 -*-
# @Time    : 2026/3/25 18:28
# @Author  : lwc
# @File    : http_request.py
# @Description :

import httpx
from app.utils.http_content_type_enum import HttpContentTypeEnum


async def api_request(headers, method, url, req_content_type, params):

    if method == 'GET':
        async with httpx.AsyncClient() as client:
            print('get请求')
            res = await client.get(url=url, params=params, headers=headers )
    elif method == 'POST':
        dic = {
            "url": url,
            "headers": headers,
            HttpContentTypeEnum[req_content_type].req_method: params
        }
        print('post请求')
        async with httpx.AsyncClient() as client:
           res = await client.post(**dic)
    return res.text