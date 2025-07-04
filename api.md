上传本地文件获取临时公网URL
更新时间：2025-04-25 17:13:29
产品详情
我的收藏
在调用多模态、图像、视频或音频模型时，通常需要传入文件的公网 URL。为此，阿里云百炼提供了免费临时存储空间，您可将本地文件上传至该空间并获得公网 URL（有效期为 48 小时）。

使用限制
文件与模型绑定：文件上传时必须指定模型名称，且该模型须与后续调用的模型一致，不同模型无法共享文件。此外，不同模型对文件大小有不同限制，超出限制将导致上传失败。

文件与主账号绑定：文件上传与模型调用所使用的 API Key 必须属于同一个阿里云主账号，且上传的文件仅限该主账号及其对应模型使用，无法被其他主账号或其他模型共享。

文件有效期限制：文件上传后有效期48小时，超时后文件将被自动清理，请确保在有效期内完成模型调用。

文件使用限制：文件一旦上传，不可查询、修改或下载，仅能通过URL参数在模型调用时使用。

文件上传限流：文件上传凭证接口的调用限流为指定模型调用限流的10倍，超出限流将导致请求失败。

重要
临时公网URL仅适用于测试阶段，请勿在生产环境中使用。

在生产环境中，建议使用长期有效的 URL，例如将文件存储在阿里云OSS中，以确保文件的稳定性和持久性。

快速获取文件URL（推荐）
本文提供 Python 和 Java 示例代码，将上传本地文件至临时空间并获取 URL 的三步操作简化为一步。

前提条件
在调用前，您需要获取API Key，再配置API Key到环境变量。

示例代码
PythonJava
环境配置

推荐使用Python 3.8及以上版本。

请安装必要的依赖包。

 
pip install -U requests
输入参数

api_key：阿里云百炼API KEY。

model_name：上传文件时需指定调用的模型名称，如qwen-vl-plus。

file_path：待上传的本地文件路径（图片、视频等）。

 
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta

def get_upload_policy(api_key, model_name):
    """获取文件上传凭证"""
    url = "https://dashscope.aliyuncs.com/api/v1/uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "action": "getPolicy",
        "model": model_name
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to get upload policy: {response.text}")
    
    return response.json()['data']

def upload_file_to_oss(policy_data, file_path):
    """将文件上传到临时存储OSS"""
    file_name = Path(file_path).name
    key = f"{policy_data['upload_dir']}/{file_name}"
    
    with open(file_path, 'rb') as file:
        files = {
            'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
            'Signature': (None, policy_data['signature']),
            'policy': (None, policy_data['policy']),
            'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
            'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
            'key': (None, key),
            'success_action_status': (None, '200'),
            'file': (file_name, file)
        }
        
        response = requests.post(policy_data['upload_host'], files=files)
        if response.status_code != 200:
            raise Exception(f"Failed to upload file: {response.text}")
    
    return f"oss://{key}"

def upload_file_and_get_url(api_key, model_name, file_path):
    """上传文件并获取公网URL"""
    # 1. 获取上传凭证
    policy_data = get_upload_policy(api_key, model_name) 
    # 2. 上传文件到OSS
    oss_url = upload_file_to_oss(policy_data, file_path)
    
    return oss_url

# 使用示例
if __name__ == "__main__":
    # 从环境变量中获取API Key 或者 在代码中设置 api_key = "your_api_key"
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise Exception("请设置DASHSCOPE_API_KEY环境变量")
        
    # 设置model名称
    model_name="qwen-vl-plus"

    # 待上传的文件路径
    file_path = "/tmp/cat.png"  # 替换为实际文件路径
    
    try:
        public_url = upload_file_and_get_url(api_key, model_name, file_path)
        expire_time = datetime.now() + timedelta(hours=48)
        print(f"文件上传成功，有效期为48小时，过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"公网URL: {public_url}")

    except Exception as e:
        print(f"Error: {str(e)}")


HTTP调用接口
功能描述
用于生成人物试衣图片。

前提条件
已开通阿里云百炼服务并获得API-KEY：获取API Key。

作业提交接口
 
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis
说明
因该算法调用耗时较长，故采用异步调用的方式提交任务。

任务提交之后，系统会返回对应的作业ID，后续可通过“作业任务状态查询和结果获取接口”获取任务状态及对应结果。

入参描述






字段

类型

传参方式

必选

描述

示例值

Content-Type

String

Header

是

请求类型：application/json

application/json

Authorization

String

Header

是

API-Key，例如：Bearer d1**2a

Bearer d1**2a

X-DashScope-Async

String

Header

是

使用 enable，表明使用异步方式提交作业。

enable

model

String

Body

是

指明需要调用的模型。

aitryon-plus

input.person_image_url

String

Body

是

用户上传的模特人物图片URL。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此获取临时公网URL。

5KB≤图像文件≤5M

150≤图像边长≤4096

格式支持：jpg、png、jpeg、bmp、heic

需保持图片中有且仅有一个完整的人

上传图片仅支持HTTP链接，不支持本地路径

http://aaa/3.jpg

input.top_garment_url

String

Body

否

用户上传的上装服饰图片URL。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此获取临时公网URL。

5KB≤图像文件≤5M

150≤图像边长≤4096

格式支持：jpg、png、jpeg、bmp、heic

需上传服饰平铺图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多

上传图片仅支持HTTP链接，不支持本地路径

说明
上装或下装服饰图片需至少输入一个。

上装图片置空时，上装效果将随机生成。

连衣裙应作为上装输入，并将下装置空。

http://aaa/1.jpg

input.bottom_garment_url

String

Body

否

用户上传的下装服饰图片URL。

URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此获取临时公网URL。

5KB≤图像文件≤5M

150≤图像边长≤4096

格式支持：jpg、png、jpeg、bmp、heic

需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多

上传图片仅支持HTTP链接，不支持本地路径

说明
上装或下装服饰图片需至少输入一个。

下装图片置空时，下装效果将随机生成。

http://aaa/2.jpg

parameters.resolution

Int

Body

否

输出图片的分辨率控制。包含3个选项：

值为1024代表（576x1024）；

值为1280代表（720x1280）；

值为-1代表还原到原图大小，默认为-1。

说明
若后续还需调用AI试衣图片精修API，该值必须设为-1。

-1

parameters.restore_face

Bool

Body

否

输出图片模特脸部的还原控制。包含2个选项：

值为false时会生成新的人脸；

值为true时会还原原图人脸，默认为true。

说明
若后续还需调用AI试衣图片精修API，该值必须设为true。

true

出参描述




字段

类型

描述

示例值

output.task_id

String

提交异步任务的作业id，实际作业结果需要通过异步任务查询接口获取。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task_status

String

提交异步任务后的作业状态。

PENDING

request_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

请求示例
 
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-plus",
    "input": {
        "top_garment_url": "http://xxx/1.jpg",
        "bottom_garment_url": "http://xxx/2.jpg",
        "person_image_url": "http://xxx/3.jpg"
    },
    "parameters": {
        "resolution": -1,
        "restore_face": true
    }
  }'
响应示例
 
{
    "output": {
	"task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1", 
    	"task_status": "PENDING"
    }
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
作业任务状态查询和结果获取接口
 
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
说明
异步任务查询接口提供 20 QPS 的访问流量限制。若有更高频次的查询需求，可通过EventBridge配置事件转发，详见配置异步任务回调。

已提交的异步任务列表查询，及异步任务的取消管理，详见管理异步任务。

入参描述






字段

类型

传参方式

必选

描述

示例值

Authorization

String

Header

是

API-Key，例如：Bearer sk-xxx。

Bearer sk-xxx

task_id

String

Url Path

是

需要查询作业的 task_id。

a8532587-fa8c-4ef8-82be-0c46b17950d1

出参描述




字段

类型

描述

示例值

output.task_id

String

查询作业的 task_id

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task_status

String

被查询作业的作业状态

任务状态：

PENDING 排队中

PRE-PROCESSING 前置处理中

RUNNING 处理中

POST-PROCESSING 后置处理中

SUCCEEDED 成功

FAILED 失败

UNKNOWN 作业不存在或状态未知

CANCELED：任务取消成功

output.image_url

String

生成的结果物地址，

image_url有效期为作业完成后24小时

{"image_url":"https://xxx/1.jpg"}

usage.image_count

Int

本次请求生成图片张数

"image_count": 1

request_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

请求示例
 
curl -X GET \
 --header 'Authorization: Bearer <YOUR_API_KEY>' \
 'https://dashscope.aliyuncs.com/api/v1/tasks/<YOUR_TASK_ID>'
响应示例
 
{
  "request_id": "xxx",
  "output": {
    "task_id": "xxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2024-07-30 15:39:39.918",
    "scheduled_time": "2024-07-30 15:39:39.941",
    "end_time": "2024-07-30 15:39:55.080",
    "image_url": "YOUR_IMAGE_URL"
  },
  "usage": {
    "image_count": 1
  }
}
异常响应示例
 
{
    "request_id": "6bf4693b-c6d0-933a-b7b7-f625d098d742",
    "output": {
        "task_id": "e32bd911-5a3d-4687-bf53-9aaef32213e9",
        "task_status": "FAILED",
        "code": "xxx",
        "message": "xxxxxx"
  }
}