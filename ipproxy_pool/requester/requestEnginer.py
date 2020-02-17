# -*- coding: utf-8 -*-

import logging
import requests
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from requests.adapters import HTTPAdapter
from ..config.config import Validated_url
from ..config.config import THREADPOOL_NUM
import concurrent.futures
from ..db.model.proxymodel import proxy_operating
from apscheduler.schedulers.background import BackgroundScheduler

# 全局变量
session = requests.Session()
# 经过过滤之后的代理地址
available_proxy_list = []


def do_get(url, headers, proxies):
    """
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    """
    timeout = 2

    session.mount('http://', HTTPAdapter(max_retries=2))
    session.mount('https://', HTTPAdapter(max_retries=2))

    if headers is None:
        if proxies is None:
            response = session.get(url, timeout=timeout)
            return response
        else:
            response = session.get(url, proxies=proxies, timeout=timeout)
            return response
    else:
        if proxies is None:
            response = session.get(url, headers=headers, timeout=timeout)
            return response
        else:
            response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
            return response


def check_proxy_ip_task():

    scheduler = BackgroundScheduler()
    scheduler.add_job(__check_ip_availability, 'interval', seconds=5, args=proxy_operating().find_limit())

    scheduler.start()


def __check_ip_availability(proxy_list):
    logging.info('开始定时任务')
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADPOOL_NUM) as executor:
        future_data = {executor.submit(filter_proxy, proxy_data): proxy_data for proxy_data in proxy_list}
        for i in concurrent.futures.as_completed(future_data):
            f = future_data[i]
            proxy_ip = '%s:%s' % (f['ip_addr'], f['port'])
            try:
                data = i.result()
            except Exception as e:
                logging.error('代理ip %r 线程任务产生了错误: %s' % (f, e))
            else:
                if data is None:
                    logging.info('代理ip %s 在检查连接任务时失败而被Kill掉' % proxy_ip)
                    proxy_operating().delete_proxy(proxy_ip)


def filter_unavailable_proxy(proxy_list: list):
    """
    验证代理地址,目的是过滤掉无用的代理
    """
    available_proxy_list.clear()

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADPOOL_NUM) as executor:
        future_data = {executor.submit(filter_proxy, proxy_data): proxy_data for proxy_data in proxy_list}
        for i in concurrent.futures.as_completed(future_data):
            f = future_data[i]
            try:
                data = i.result()
            except Exception as e:
                logging.error('%r 数据产生了错误: %s' % (f, e))
            else:
                if data is not None:
                    available_proxy_list.append(data)

    logging.info("=====  经过过滤后剩下 " + str(len(available_proxy_list)) + " 个代理  =====")
    return available_proxy_list


def filter_proxy(proxy_data):
    """
    线程池中线程验证代理地址
    """
    url = Validated_url

    http_type = proxy_data['protocol']
    ip = proxy_data['ip_addr']
    port = proxy_data['port']
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    proxies = {
        'http': http_type.lower() + "://" + ip + ":" + str(port)
    }
    try:
        response = do_get(url, headers=header, proxies=proxies)

        if response.status_code == 200:
            return proxy_data
        else:
            return None
    except Exception as e:
        logging.error('验证代理ip失败 : %s' % e)
