# coding:utf-8

import logging
import os


def logs():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
                        filename='log/system_log.log',
                        filemode='w'
                        )
    return logging
