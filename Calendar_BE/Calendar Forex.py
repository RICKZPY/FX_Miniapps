import requests

# 简洁版本
url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

try:
    # 获取数据
    response = requests.get(url)
    data = response.json()

    # 筛选并打印高影响事件
    high_impact = [event for event in data if event.get('impact') == 'High']

    print(f"找到 {len(high_impact)} 个高影响事件:")
    for event in high_impact:
        print(f"\n标题: {event.get('title')}")
        print(f"时间: {event.get('date')}")
        print(f"国家: {event.get('country')}")
        print(f"前值: {event.get('previous')}")
        print(f"预测: {event.get('forecast')}")

except Exception as e:
    print(f"发生错误: {e}")