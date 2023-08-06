#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from urllib import parse
import requests
import time


def oceanengine_postback(
        callback_url,
        action_type,
        action_value=None
):
    """
    回传功能
    :param callback_url: 回传参数
    :param action_type: 回传类型
    :param action_value: 回传类型对于金额
    """
    callback_str_decode = parse.unquote(callback_url)
    if action_value is None:
        actions = [
                {
                    "action_type": action_type
                }
            ]
    else:
        actions = [
            {
                "action_type": action_type,
                "value": str(action_value)
            }
        ]
    response = requests.request(
        method='POST',
        url=callback_str_decode,
        json={
            "actions": actions
        }
    )
    response_json = response.json()
    if response_json.get('code') == 0:
        return True
    else:
        return False


def base_send_request(
        request_params: dict,  # 全部参数的值要转换为数值
        request_url: str = "https://ad.oceanengine.com/track/activate/"  # 上报数据的接口
):
    """
    回传文档：https://open.oceanengine.com/doc/index.html?key=ad&type=api&id=1696710647473167
    request_url="https://ad.oceanengine.com/track/activate/?link=__LINK__&source=__SOURCE__&conv_time=__CONV_TIME__&event_type=__EVENT_TYPE__"
    request_params={
        "callback": "EJiw267wvfQCGKf2g74ZIPD89-vIATAMOAFCIjIwMTkxMTI3MTQxMTEzMDEwMDI2MDc3MjE1MTUwNTczNTBIAQ==",
        "imei": "0c2bd03c39f19845bf54ea0abafae70e",
        "os": "1",
        "event_type": "2",
        "conv_time": str(int(time.time())),
        "link": 'https://www.chengzijianzhan.com/tetris/page/6979479559541784583/?adid=1701500355930731&clickid=EOvUs-KW8IIDGI6g7vOPloEDKIuQoZv_v4MD&creativeid=1701500355930731&creativetype=1'
    }
    其中的link必填
    回传参数说明：https://open.oceanengine.com/doc/index.html?key=ad&type=api&id=1696710647473167
        link （必填），拼接了参数的落地页链接
        event_type（必填回传参数）：2 付费
        conv_time：int（整型）建议填写（填写付费时间）
        source：string（字符串）建议填写（不填）

    但是说明文档说的用ip+ua匹配后直接用回调地址回传，文档见：https://bytedance.feishu.cn/docs/doccnOaxIYGeXokJUqHJGhm86Xf
    """
    try:
        response = requests.get(
            url=request_url,
            params=request_params,
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return


def send(
        callback_url: str,
        action_type: int = 0  # 0:激活，2：付费
):
    """
    快速回传接口，使用callback_url和event_type直接拼接回传
    回传激活和付费
    """
    if callback_url is None or len(callback_url) == 0:
        print('callback_url is wrong')
        return False
    elif action_type is None or len(str(action_type)) == 0:
        print('event_type is wrong')
        return False
    else:
        try:
            response = requests.request(
                method='GET',
                url=callback_url,
                params={'event_type': action_type}
            )
            response_json = response.json()
            print(response_json)
            return True
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
            return False


def send_request_quick_app_v2(
        callback: str = None
):
    """
    快应用API回传
    文档：https://event-manager.oceanengine.com/docs/8650/quickapp/
    文档2：https://event-manager.oceanengine.com/docs/8650/app_api_docs/
    """
    url = 'https://analytics.oceanengine.com/api/v2/conversion'
    data = {
        "event_type": "active_pay",
        "context": {
            "ad": {
                "callback": callback,
            }
        },
        "timestamp": int(time.time() * 1000)
    }
    response = requests.post(
        url=url,
        json=data
    )
    return response

