# -*- coding: utf-8 -*-


class ProxyMiddleware(object):
    def process_request(self, request, spider):

        if request.url.startswith("http://"):
            request.meta['proxy'] = "http://180.96.27.12:88"  # http代理
        elif request.url.startswith("https://"):
            request.meta['proxy'] = "http://109.108.87.136:53281"  # https代理

#         # proxy authentication
#         proxy_user_pass = "USERNAME:PASSWORD"
#         encoded_user_pass = base64.encodestring(proxy_user_pass)
#         request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass