# -*- coding: utf-8 -*-
import re
import sys
import time

import oss2
import requests
import shortuuid
import urllib3
from oss2 import determine_part_size, SizedFileAdapter
from oss2.models import PartInfo

from .baidu_disk import ApiException
from .baidu_disk.utils.auth import oauthtoken_devicecode, oauthtoken_devicetoken, oauthtoken_refreshtoken
from .baidu_disk.utils.fileinfo import filelist
from .baidu_disk.utils.filemanager import move, copy, rename, delete
from .baidu_disk.utils.multimedia_file import listall, filemetas

HTTP_POOL = urllib3.PoolManager(cert_reqs='CERT_NONE')
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Baidudisk(object):
    def __init__(self, app_key, secret_key, **kwargs):
        # self.__dict__.update(locals())

        self.app_key = kwargs.get("app_key", app_key)
        self.secret_key = kwargs.get("secret_key", secret_key)
        self.scope = kwargs.get("scope", "basic netdisk")

        self.device_code = None
        self.access_token = None

        self.refresh_token = None
        self.expires_at = None

    def __encode_path(self, path, kwargs_key="path",**kwargs):
        path = kwargs.get(kwargs_key, path)
        # 对path进行url编码
        path = urllib.parse.quote(path)
        if kwargs.get(kwargs_key):
            kwargs[kwargs_key] = path
    def __refresh_token(self):
        if self.expires_at is None or self.expires_at < time.time():
            raise TokenExpiredException(reason=f"token is expired，please login again")
        # refresh_token=None, client_id=None, client_secret=None
        res = oauthtoken_refreshtoken(self.refresh_token, self.app_key, self.secret_key)
        # {'access_token': '126.2ec0ffa6456c0e5515cbe46e4297f014.Ymbb6R_6H8pWSBVcD2Fit-wGES4JZq7fXHft0SQ.mp6MJQ',
        #  'expires_in': 2592000,
        #  'refresh_token': '127.134b97eabe45b32566c3d1303410c824.YQZeqmaL4hSEwkAM41Kt1njmUlo28zYGv9e-4iQ.ScjUbg',
        #  'scope': 'basic netdisk',
        #  'session_key': '',
        #  'session_secret': ''}
        self.access_token = res["access_token"]
        self.refresh_token = res["refresh_token"]
        self.expires_at = time.time() + res["expires_in"]

    def show_qr(self):
        # 1.扫码登录
        res = oauthtoken_devicecode(self.app_key)
        # {'device_code': '0993010f33712ad7ff2de4ff76db2f2e',
        #  'expires_in': 300,
        #  'interval': 5,
        #  'qrcode_url': 'https://openapi.baidu.com/device/qrcode/6ad8f3eb08e1f9ceb1e3d9958c6e9807/bhaq4ptd',
        #  'user_code': 'bhaq4ptd',
        #  'verification_url': 'https://openapi.baidu.com/device'}
        device_code = res["device_code"]
        self.device_code = device_code
        return res

    def auth_by_qr(self):
        p = {
            "code": self.device_code,
            "app_key": self.app_key,
            "secret_key": self.secret_key
        }
        res = oauthtoken_devicetoken(**p)
        # {'access_token': '126.6f1888128811faed7a5a45b19d079d25.YBgHQjzHXZ8h9iS8RnQWSoTIHJSVq6zQurCOA4S.LpU-Rw',
        #  'expires_in': 2592000,
        #  'refresh_token': '127.5bc340f665c2c68e1af7a72f12932054.YsjmXD3Dhe55NRkMBLxyFLUWgNKYIq0SJ0f6Qk5.7Cz82A',
        #  'scope': 'basic netdisk',
        #  'session_key': '',
        #  'session_secret': ''}
        self.access_token = res["access_token"]
        self.refresh_token = res["refresh_token"]
        self.expires_at = int(time.time()) * 1000 + res["expires_in"]
        return res

    def filelist(self, dir="/", folder="1",  start=0, limit=1000, order="time", desc=1, web="1",**kwargs):
        """
        :param dir	需要list的目录，以/开头的绝对路径, 默认为/
                    路径包含中文时需要UrlEncode编码
                    给出的示例的路径是/测试目录的UrlEncode编码
        :param folder	是否只返回文件夹，0 返回所有，1 只返回文件夹，且属性只返回path字段
        :param web	    值为1时，返回dir_empty属性和缩略图数据
        :param start	起始位置，从0开始
        :param limit	查询数目，默认为1000，建议最大不超过1000
        :param order	排序字段：默认为name；
                time表示先按文件类型排序，后按修改时间排序；
                name表示先按文件类型排序，后按文件名称排序；(注意，此处排序是按字符串排序的，如果用户有剧集排序需求，需要自行开发)
                size表示先按文件类型排序，后按文件大小排序。
        :param desc	默认为升序，设置为1实现降序 （注：排序的对象是当前目录下所有文件，不是当前分页下的文件）
        :param showempty	是否返回dir_empty属性，0 不返回，1 返回

        :return:
            {'errno': 0,
             'guid': 0,
             'guid_info': '',
             'list': [
                      {'dir_empty': 1,
                       'fs_id': 0,
                       'path': '/betterme/0200董晨宇的传播学课_L6798',
                       'share': 0}
                      ],
             'request_id': 9105102554915445232}
        """
        self.__encode_path(dir,"dir", **kwargs)
        self.__refresh_token()
        # dir="/", folder="0", start="0", limit=2, order="time", desc=1, web="web"
        return filelist(self.access_token, dir, folder, str(start), limit, order, desc, web, **kwargs)

    def filelist_by_page(self, dir="/", folder="1", page_no=1, page_size=1000, order="name", desc=0, web="1",**kwargs):
        """
        :param dir: 需要list的目录，以/开头的绝对路径, 默认为/
                    路径包含中文时需要UrlEncode编码
                    给出的示例的路径是/测试目录的UrlEncode编码
        :param folder: 是否只返回文件夹，0 返回所有，1 只返回文件夹，且属性只返回path字段
        :param page_no: 页码
        :param page_size: 每页数量
        :param order: 排序字段：默认为name；
        :param desc: 默认为升序，设置为1实现降序 （注：排序的对象是当前目录下所有文件，不是当前分页下的文件）
        :param web: 值为1时，返回dir_empty属性和缩略图数据
        :return:
            {'errno': 0,
             'guid': 0,
             'guid_info': '',
             'list': [
                      {'dir_empty': 1,
                       'fs_id': 0,
                       'path': '/betterme/0200董晨宇的传播学课_L6798',
                       'share': 0}
                      ],
             'request_id': 9105102554915445232}
        """
        start = (page_no - 1) * page_size
        limit = page_size
        return self.filelist(dir, folder, start, limit, order, desc,web, **kwargs)


    def listall(self, path="/", recursion=1, web="1", start=0, limit=2, order="time", desc=1, **kwargs):
        self.__encode_path(path, **kwargs)
        self.__refresh_token()
        return listall(self.access_token, path, recursion, web, start, limit, order, desc, **kwargs)

    def filemetas(self, fsids, thumb=1, extra=1, dlink=1, needmedia=1, **kwargs):
        self.__refresh_token()
        return filemetas(self.access_token, fsids, thumb, extra, dlink, needmedia, **kwargs)

    def move(self, filelist, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123456.docx","ondup":"overwrite"}]'
        self.__refresh_token()
        # filelist, ondup="overwrite",_async=1
        return move(self.access_token, filelist, ondup, _async, **kwargs)

    def copy(self, filelist, _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123.docx","ondup":"overwrite"}]'
        self.__refresh_token()
        return copy(self.access_token, filelist, _async, **kwargs)

    def rename(self, filelist, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","newname":"123.docx"}]'  # str | filelist
        self.__refresh_token()
        return rename(self.access_token, filelist, ondup, _async, **kwargs)

    def rename1(self, path, newname, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","newname":"123.docx"}]'  # str | filelist
        self.__encode_path(path, **kwargs)

        filelist = [{"path": path, "newname": newname}]
        return self.rename(self.access_token, filelist, ondup, _async, **kwargs)

    def delete(self, filelist, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx"}]'  # str | filelist
        self.__refresh_token()
        return delete(self.access_token, filelist, ondup, _async=1, **kwargs)

    def delete1(self, path, ondup="overwrite", _async=1, **kwargs):

        filelist = [{"path": path}]
        return self.delete(self.access_token, filelist, ondup, _async=1, **kwargs)


class TokenExpiredException(ApiException):
    """
    class UnauthorizedException
    """

    def __init__(self, status=None, reason=None, http_resp=None):
        """
        __init__
        """
        super(TokenExpiredException, self).__init__(status, reason, http_resp)
