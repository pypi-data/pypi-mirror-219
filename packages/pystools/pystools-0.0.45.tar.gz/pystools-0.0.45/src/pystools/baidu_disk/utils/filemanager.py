# -*- coding: utf-8 -*-
"""
    xpan filemanager 
    include:
        filemanager move
        filemanager copy
        filemanager remove
        filemanager delete
"""
import os,sys

from .. import ApiClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from pprint import pprint
from ..api import filemanager_api


def move(access_token,  filelist, ondup="overwrite",_async=1,**kwargs):
    """
    filemanager move
    """
    access_token = kwargs.get("access_token", access_token)
    _async = kwargs.get("_async", _async)
    filelist = kwargs.get("filelist", filelist)
    ondup = kwargs.get("ondup", ondup)

    # Enter a context with an instance of the API client
    with ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = filemanager_api.FilemanagerApi(api_client)
        # access_token = "123.56c5d1f8eedf1f9404c547282c5dbcf4.YmmjpAlsjUFbPly3mJizVYqdfGDLsBaY5pyg3qL.a9IIIQ"  # str |
        # _async = 1  # int | async
        # # str | filelist
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123456.docx","ondup":"overwrite"}]'
        # ondup = "overwrite"  # str | ondup (optional)
        api_response = api_instance.filemanagermove(
            access_token, _async, filelist, ondup=ondup,**kwargs)
        return api_response

        # example passing only required values which don't have defaults set
        # and optional values
        # try:
        #     api_response = api_instance.filemanagermove(
        #         access_token, _async, filelist, ondup=ondup)
        #     print(api_response)
        # except ApiException as e:
        #     print("Exception when calling FilemanagerApi->filemanagermove: %s\n" % e)


def copy(access_token,  filelist, _async=1,**kwargs):
    """
    filemanager copy
    """
    access_token = kwargs.get("access_token", access_token)
    _async = kwargs.get("_async", _async)
    filelist = kwargs.get("filelist", filelist)

    # Enter a context with an instance of the API client
    with ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = filemanager_api.FilemanagerApi(api_client)
        # access_token = "123.56c5d1f8eedf1f9404c547282c5dbcf4.YmmjpAlsjUFbPly3mJizVYqdfGDLsBaY5pyg3qL.a9IIIQ"  # str |
        # _async = 1  # int | async
        # # str | filelist
        # filelist = '[{"path":"/test/123456.docx","dest":"/test/abc","newname":"123.docx","ondup":"overwrite"}]'
        api_response = api_instance.filemanagercopy(access_token, _async, filelist,**kwargs)
        return api_response
        # example passing only required values which don't have defaults set
        # try:
        #     api_response = api_instance.filemanagercopy(access_token, _async, filelist)
        #     print(api_response)
        # except baidu_disk_openapi.ApiException as e:
        #     print("Exception when calling FilemanagerApi->filemanagercopy: %s\n" % e)


def rename(access_token,  filelist, ondup="overwrite",_async=1,**kwargs):
    """
    filemanager rename
    """
    access_token = kwargs.get("access_token", access_token)
    _async = kwargs.get("_async", _async)
    filelist = kwargs.get("filelist", filelist)
    ondup = kwargs.get("ondup", ondup)

    # Enter a context with an instance of the API client
    with ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = filemanager_api.FilemanagerApi(api_client)
        # access_token = "123.56c5d1f8eedf1f9404c547282c5dbcf4.YmmjpAlsjUFbPly3mJizVYqdfGDLsBaY5pyg3qL.a9IIIQ"  # str |
        # _async = 1  # int | async
        # filelist = '[{"path":"/test/123456.docx","newname":"123.docx"}]'  # str | filelist
        # ondup = "overwrite"  # str | ondup (optional)
        api_response = api_instance.filemanagerrename(
            access_token, _async, filelist, ondup=ondup,**kwargs)
        return api_response
        # example passing only required values which don't have defaults set
        # and optional values
        # try:
        #     api_response = api_instance.filemanagerrename(
        #         access_token, _async, filelist, ondup=ondup)
        #     pprint(api_response)
        # except baidu_disk_openapi.ApiException as e:
        #     print("Exception when calling FilemanagerApi->filemanagerrename: %s\n" % e)


def delete(access_token,  filelist, ondup="overwrite",_async=1,**kwargs):
    """
    filemanager delete
    """
    access_token = kwargs.get("access_token", access_token)
    _async = kwargs.get("_async", _async)
    filelist = kwargs.get("filelist", filelist)
    ondup = kwargs.get("ondup", ondup)

    with ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = filemanager_api.FilemanagerApi(api_client)
        # access_token = "123.56c5d1f8eedf1f9404c547282c5dbcf4.YmmjpAlsjUFbPly3mJizVYqdfGDLsBaY5pyg3qL.a9IIIQ"  # str |
        # _async = 1  # int | async
        # filelist = '[{"path":"/test/123456.docx"}]'  # str | filelist
        # ondup = "overwrite"  # str | ondup (optional)
        api_response = api_instance.filemanagerdelete(
            access_token, _async, filelist, ondup=ondup,**kwargs)
        return api_response
        # example passing only required values which don't have defaults set
        # and optional values
        # try:
        #     api_response = api_instance.filemanagerdelete(
        #         access_token, _async, filelist, ondup=ondup)
        #     print(api_response)
        # except baidu_disk_openapi.ApiException as e:
        #     print("Exception when calling FilemanagerApi->filemanagerdelete: %s\n" % e)


if __name__ == '__main__':
    copy()
    move()
    rename()
    delete()
