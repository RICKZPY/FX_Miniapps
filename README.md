主要功能说明
数据获取与筛选

自动从 https://nfs.faireconomy.media/ff_calendar_thisweek.json 获取本周经济日历

筛选条件：country为"USD"（美国）且impact为"High"

数据缓存10分钟以减少频繁请求

时间处理

原始时间（纽约时间，UTC-5）自动转换为北京时间（UTC+8）

显示日期、星期和具体时间

多维度查看

所有事件：完整列表

今日事件：当天的高影响事件

明日事件：明天的事件预览

即将发生：未来24小时内的事件倒计时

统计信息

事件总数、今日事件数统计

按星期分布的可视化图表

含预测值的事件统计

数据导出

支持CSV和JSON格式下载

包含所有筛选后的事件数据

如何使用
安装依赖：

bash
pip install streamlit pandas requests pytz
运行应用：

bash
streamlit run us_economic_calendar.py
使用提示：

侧边栏有手动刷新按钮

数据每10分钟自动更新

支持多种格式数据下载

时间已转换为北京时间

这个应用专注于美国高影响经济事件，界面简洁，功能实用，适合交易员和投资者快速了解重要经济数据发布时间。
