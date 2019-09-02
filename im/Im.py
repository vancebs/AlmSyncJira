#!/usr/bin/python
# -*- coding: UTF-8 -*-

from subprocess import Popen
import subprocess


class Im(object):
    _CODEC_CHECK_LIST = (
        'GBK',
        'utf-8'
        'ascii',
        'ISO-8859-2',
        'windows-1252',
        'GB2312'
    )

    @staticmethod
    def execute(cmd):
        # run command
        p = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

        (out, err) = p.communicate()
        return p.returncode, Im.decode_str(out), Im.decode_str(err)

    @staticmethod
    def decode_str(str_src):
        # try decode with known types
        exception = None
        for codec in Im._CODEC_CHECK_LIST:
            # print('try codec: %s' % codec)
            try:
                return str_src.decode(codec)
            except UnicodeDecodeError as e:
                exception = e
        raise exception
