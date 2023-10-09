import json
import requests


# 微博热搜API URL
weibo_api_url = "https://weibo.com/ajax/statuses/hot_band"


# 自定义的Webhook URL，用于向用户接口推送数据
webhook_url = "http://xxx:3001/webhook/msg"  # 请替换为实际的Webhook URL

# 获取微博热搜数据的函数
def get_weibo_hot_search():
    try:
        # 发送HTTP GET请求获取微博热搜数据
        response = requests.get(weibo_api_url)
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            # 提取热搜列表
            hot_search_list = data.get('data', {}).get('band_list', [])[:10]
            return hot_search_list
    except Exception as e:
        print("获取微博热搜失败:", str(e))
        return []

# 构建带有链接的热搜消息
def build_hot_search_message(hot_search_list):
    message = ""
    for index, hot_search in enumerate(hot_search_list, start=1):
        title = hot_search.get("word", "N/A")
        link = hot_search.get("link", "")
        if link:
            message += f"{index}. [{title}]({link})\n"
        else:
            message += f"{index}. {title}\n"
    return message

# 获取各个热搜数据
weibo_hot_search_list = get_weibo_hot_search()

# 构建带有链接的热搜消息

weibo_message = "微博热搜榜：\n" + build_hot_search_message(weibo_hot_search_list)

message_data_weibo = {
    "to": "123", #替换真实的群名称或者个人
    "isRoom": True,
    "type": "text",
    "content": weibo_message
}

# 发送消息到自定义Webhook
try:
    headers = {"Content-Type": "application/json"}
   
    
    response_weibo = requests.post(webhook_url, data=json.dumps(message_data_weibo), headers=headers)
    
    if response_weibo.status_code == 200:
        print("微博热搜消息成功发送到Webhook。")
    else:
        print(f"发送微博热搜消息到Webhook失败，HTTP状态码: {response_weibo.status_code}")
except Exception as e:
    print("发送消息到Webhook失败:", str(e))
