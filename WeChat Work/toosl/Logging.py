# coding:utf-8

import logging
import os


path = os.path.split(os.getcwd())
file = 'log\system.log'
new_path = os.path.join(path[0], file)


def logs():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
                        filename=new_path,
                        filemode='a'
                        )
    return logging
