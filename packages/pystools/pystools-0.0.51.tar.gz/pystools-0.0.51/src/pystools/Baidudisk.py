# -*- coding: utf-8 -*-
import json
import os
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
from .baidu_disk.utils.filemanager import move, copy, rename, delete, create_folder
from .baidu_disk.utils.multimedia_file import listall, filemetas

HTTP_POOL = urllib3.PoolManager(cert_reqs='CERT_NONE')
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Baidudisk(object):
    def __init__(self, app_key, secret_key, tenant=None,cache_path = "./tmp", **kwargs):
        # self.__dict__.update(locals())

        self.cache_path = kwargs.get("cash_path", cache_path)
        # 如果cache_path不存在，创建cache_path
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        self.tenant = tenant
        self.app_key = kwargs.get("app_key", app_key)
        self.secret_key = kwargs.get("secret_key", secret_key)
        self.scope = kwargs.get("scope", "basic netdisk")

        self.device_code = self.__get_cahced_token("device_code")
        self.access_token = self.__get_cahced_token("access_token")
        self.refresh_token = self.__get_cahced_token("refresh_token")
        expires_at_str = self.__get_cahced_token("expires_at")
        self.expires_at = int(expires_at_str) if expires_at_str else None

    def __refresh_cached_properties(self):
        self.device_code = self.__get_cahced_token("device_code")
        self.access_token = self.__get_cahced_token("access_token")
        self.refresh_token = self.__get_cahced_token("refresh_token")
        expires_at_str = self.__get_cahced_token("expires_at")
        self.expires_at = int(expires_at_str) if expires_at_str else None

    def __get_cahced_token(self,key):
        file = os.path.join(self.cache_path, f"baidunetdisk_{self.tenant}.json")
        if not os.path.exists(file):
            return None
        else:
            with open(file, "r") as f:
                property = json.loads(f.read())
                return property.get(key, None)

    def __cahce_property(self, key, value):
        file = os.path.join(self.cache_path, f"baidunetdisk_{self.tenant}.json")
        property = {}
        if not os.path.exists(file):
            property[key] = value
            with open(file, "w") as f:
                f.write(json.dumps(property, indent=4, ensure_ascii=False))
        else:
            with open(file, "r") as f:
                property = json.loads(f.read())
                property[key] = value
            with open(file, "w") as f:
                f.write(json.dumps(property, indent=4, ensure_ascii=False))
        self.__refresh_cached_properties()


    def is_auth(self):
        # 如果expires_at大于当前时间，说明token还有效，self.is_auth = True
        now = int(time.time())
        print("expires_at", self.expires_at, "now", now,  self.expires_at-now)
        is_auth = self.expires_at is not None and self.expires_at > int(time.time())
        return is_auth


    def __check_token(self):
        # 刷新token
        now = int(time.time())
        # print("expires_at", self.expires_at, "now", now, self.expires_at - now)
        if self.expires_at is None:
            raise TokenExpiredException(reason=f"token is expired，please login again")
        if self.expires_at < int(time.time()):
            self.__refresh_token()
        # refresh_token=None, client_id=None, client_secret=None


    def __refresh_token(self):
        res = oauthtoken_refreshtoken(self.refresh_token, self.app_key, self.secret_key)
        # {'access_token': '126.2ec0ffa6456c0e5515cbe46e4297f014.Ymbb6R_6H8pWSBVcD2Fit-wGES4JZq7fXHft0SQ.mp6MJQ',
        #  'expires_in': 2592000,
        #  'refresh_token': '127.134b97eabe45b32566c3d1303410c824.YQZeqmaL4hSEwkAM41Kt1njmUlo28zYGv9e-4iQ.ScjUbg',
        #  'scope': 'basic netdisk',
        #  'session_key': '',
        #  'session_secret': ''}
        # self.access_token = res["access_token"]
        self.__cahce_property("access_token", res["access_token"])
        # self.refresh_token = res["refresh_token"]
        self.__cahce_property("refresh_token", res["refresh_token"])
        # self.expires_at = time.time() + res["expires_in"]
        self.__cahce_property("expires_at", time.time() + res["expires_in"])

    def show_qr(self):
        # 1.扫码登录
        res = oauthtoken_devicecode(self.app_key)
        # {'device_code': '0993010f33712ad7ff2de4ff76db2f2e',
        #  'expires_in': 300,
        #  'interval': 5,
        #  'qrcode_url': 'https://openapi.baidu.com/device/qrcode/6ad8f3eb08e1f9ceb1e3d9958c6e9807/bhaq4ptd',
        #  'user_code': 'bhaq4ptd',
        #  'verification_url': 'https://openapi.baidu.com/device'}
        self.__cahce_property("device_code",res["device_code"])
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
        # self.access_token = res["access_token"]
        self.__cahce_property("access_token",res["access_token"])
        # self.refresh_token = res["refresh_token"]
        self.__cahce_property("refresh_token",res["refresh_token"])
        # self.expires_at = int(time.time())  + res["expires_in"]
        self.__cahce_property("expires_at",int(time.time()) + res["expires_in"])
        return res

    def filelist(self, dir="/", folder="1", start=0, limit=1000, order="time", desc=1, web="1", **kwargs):
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
        self.__check_token()
        # dir="/", folder="0", start="0", limit=2, order="time", desc=1, web="web"
        return filelist(self.access_token, dir, folder, str(start), limit, order, desc, web, **kwargs)

    def filelist_by_page(self, dir="/", folder="1", page_no=1, page_size=1000, order="name", desc=0, web="1", **kwargs):
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
        return self.filelist(dir, folder, start, limit, order, desc, web, **kwargs)

    def listall(self, path="/", recursion=1, web="1", start=0, limit=2, order="time", desc=1, **kwargs):
        self.__encode_path(path, **kwargs)
        self.__check_token()
        return listall(self.access_token, path, recursion, web, start, limit, order, desc, **kwargs)

    def filemetas(self, fsids, thumb=1, extra=1, dlink=1, needmedia=1, **kwargs):
        self.__check_token()
        return filemetas(self.access_token, fsids, thumb, extra, dlink, needmedia, **kwargs)

    def move(self, filelist, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123456.docx","ondup":"overwrite"}]'
        self.__check_token()
        # filelist, ondup="overwrite",_async=1
        return move(self.access_token, filelist, ondup, _async, **kwargs)

    def move1(self, path, dest, newname=None, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123456.docx","ondup":"overwrite"}]'
        if newname is None:
            newname = os.path.basename(path)
        filelist = [{"path": path, "dest": dest, "newname": newname, "ondup": ondup}]
        return self.move(filelist, ondup, _async, **kwargs)

    def copy(self, filelist, _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123.docx","ondup":"overwrite"}]'
        self.__check_token()
        return copy(self.access_token, filelist, _async, **kwargs)

    def copy1(self, path, dest, newname=None, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123.docx","ondup":"overwrite"}]'
        if newname is None:
            newname = os.path.basename(path)
        filelist = [{"path": path, "dest": dest, "newname": newname, "ondup": ondup}]
        return self.copy(filelist, _async, **kwargs)

    def rename(self, filelist, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","newname":"123.docx"}]'  # str | filelist
        self.__check_token()
        return rename(self.access_token, filelist, ondup, _async, **kwargs)

    def rename1(self, path, newname, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx","newname":"123.docx"}]'  # str | filelist
        filelist = [{"path": path, "newname": newname}]
        return self.rename(filelist, ondup, _async, **kwargs)

    def rename_folder(self, path, new_path, ondup="overwrite", _async=1, **kwargs):
        """
        将旧的文件夹中所有文件移动到新的文件夹中，然后删除旧的文件夹
        :param path:
        :param new_path:
        :param ondup:
        :param _async:
        :param kwargs:
        :return:
        """
        # filelist = '[{"path":"/test/123456.docx","newname":"123.docx"}]'  # str | filelist
        self.__check_token()
        return rename(self.access_token, filelist, ondup, _async, **kwargs)

    def create_folder(self, path, local_ctime=None, local_mtime=None, **kwargs):
        self.__encode_path(path, **kwargs)
        self.__check_token()
        return create_folder(self.access_token, path, isdir=1, rtype=0, local_ctime=local_ctime,
                             local_mtime=local_mtime, mode=1, **kwargs)

    def delete(self, filelist, ondup="overwrite", _async=1, **kwargs):
        # filelist = '[{"path":"/test/123456.docx"}]'  # str | filelist
        self.__check_token()
        return delete(self.access_token, filelist, ondup, _async, **kwargs)

    def delete1(self, path, ondup="overwrite", _async=1, **kwargs):

        filelist = [{"path": path}]
        return self.delete(filelist, ondup, _async, **kwargs)


class TokenExpiredException(ApiException):
    """
    class UnauthorizedException
    """

    def __init__(self, status=None, reason=None, http_resp=None):
        """
        __init__
        """
        super(TokenExpiredException, self).__init__(status, reason, http_resp)
