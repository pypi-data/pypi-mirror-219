# const $request = require('request-promise-native')
# const log4jsApi = require('@log4js-node/log4js-api')
# const logger = log4jsApi.getLogger('node.cloud.lifecycle')

import os
import time
import requests

from log4py import logging

log = logging.getLogger('python.discovery.lifecycle')


def before_start():
    # 等待sidecar准备好
    _wait_sidecar_ready()


def _wait_sidecar_ready():
    """
    容器中运行时检查sidecar准备好状态

    每秒检查一次， 每5秒输出一条日志
    """

    k8s = os.environ.get('KUBERNETES_SERVICE_HOST')
    sidecar = os.environ.get('ISTIO_INJECT_STATUS')

    if not k8s or not sidecar:
        return

    count = 0
    while True:
        try:
            url = 'http://localhost:15020/healthz/ready'
            res = requests.get(url, timeout=(0.1, 0.5))
            res.raise_for_status()
            break
        except Exception:
            if count % 5 == 0:
                log.info('Waiting for sidecar ready......')
            count = count + 1
            time.sleep(1)
