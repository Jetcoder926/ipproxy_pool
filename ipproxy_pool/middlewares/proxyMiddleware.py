# -*- coding: utf-8 -*-

import logging

from ..db.model.proxymodel import proxy_operating


def set_header(request, _proxy_ip):

    proxy_ip = _proxy_ip.split('//')[1:][0]
    ip = proxy_ip.split(':')[0]
    # request.headers['X-Originating-IP'] = ip
    # request.headers['REMOTE_ADDR'] = ip
    # request.headers['X-Remote-IP'] = ip
    # request.headers['X-Remote-Addr'] = ip
    # request.headers['HTTP_CLIENT_IP'] = ip
    # request.headers['X-Client-IP'] = ip
    request.headers['http_x_forwarded_for'] = ip
    request.headers['X-Forwarded-For'] = ip
    request.headers['X-Forwarded-Port'] = proxy_ip.split(':')[1]

class SetProxyMiddleware(object):

    def process_request(self, request, spider):
        if 'proxy' in request.meta:

            proxy_address = proxy_operating().choice_proxy_ip()
            if proxy_address:
                logging.info("=====  ProxyMiddleware get a random_proxy:【 {} 】 =====".format(proxy_address))
                request.meta['proxy'] = proxy_address
                set_header(request, proxy_address)

            else:
                logging.info("ip库暂无ip可用 sorry")




class MyRetryMiddleware(object):

    def process_responce(self, request, response, spider):

        if request.meta.get('dont_retry', False):
            return response

        if response.status in spider.settings.get('RETRY_HTTP_CODES'):
            reason = "===  代理IP：%s 访问URL: %s 返回错误码: %s  ===" % (request.meta['proxy'], request.url, response.status)
            logging.info(reason)

            proxy = request.meta['proxy']
            if 'http://' in proxy:
                proxy = proxy.replace('http://', '')
            else:
                proxy = proxy.replace('https://', '')

            proxy_operating().plus_proxy_failure_time(proxy)
            proxy_operating().reduce_proxy_score(proxy)
            if not request.meta.get('dont_retry', False):
                requests = request.copy()
                proxy_address = proxy_operating().choice_proxy_ip()
                requests.meta['proxy'] = proxy_address
                if proxy_address:
                    set_header(requests, proxy_address)
                return requests
        return response

    def process_exception(self, request, exception, spider):

        logging.info("===  代理IP: %s 访问URL: %s 超时或失败.详情: %s ===" % (request.meta['proxy'], request.url, exception))

        if request.meta.get('dont_retry', False):
            return

        proxy = request.meta['proxy']
        if 'http://' in proxy:
            proxy = proxy.replace('http://', '')
        else:
            proxy = proxy.replace('https://', '')

        proxy_operating().delete_proxy(proxy)

        if not request.meta.get('dont_retry', False):
            requests = request.copy()
            proxy_address = proxy_operating().choice_proxy_ip()
            requests.meta['proxy'] = proxy_address
            if proxy_address:
                set_header(requests, proxy_address)
            return requests
