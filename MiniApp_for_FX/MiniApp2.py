import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz

# 设置页面
st.set_page_config(
    page_title="美国高影响经济事件日历",
    page_icon="📅",
    layout="wide"
)

# 应用标题
st.title("📅 美国高影响经济事件日历")
st.markdown("本应用实时显示本周对美国市场有**高影响**的经济事件与数据发布时间。")

# 侧边栏说明
with st.sidebar:
    st.header("信息")
    st.markdown("""
    **数据源**:
    - 来自: `https://nfs.faireconomy.media/ff_calendar_thisweek.json`

    **筛选条件**:
    1. 事件国家: **美国 (USD)**
    2. 影响程度: **High**

    **时间说明**:
    - 原始数据时间为**纽约时间(UTC-5)**
    - 下方表格时间已转换为**北京时间(UTC+8)**
    """)

    # 手动刷新按钮
    if st.button("🔄 手动刷新数据"):
        st.rerun()

    st.caption(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# 获取并处理数据
@st.cache_data(ttl=600)  # 缓存10分钟
def fetch_and_filter_events():
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 转换为DataFrame
        df = pd.DataFrame(data)

        # 筛选美国高影响事件
        us_high_impact = df[(df['country'] == 'USD') & (df['impact'] == 'High')].copy()

        if us_high_impact.empty:
            return pd.DataFrame(), "找到 0 个美国高影响事件。"

        # 转换时间格式
        ny_tz = pytz.timezone('America/New_York')
        beijing_tz = pytz.timezone('Asia/Shanghai')

        def convert_time(ts):
            try:
                dt_ny = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                if dt_ny.tzinfo is None:
                    dt_ny = ny_tz.localize(dt_ny)
                dt_beijing = dt_ny.astimezone(beijing_tz)
                return dt_beijing
            except:
                return None

        # 应用时间转换
        us_high_impact['date_beijing'] = us_high_impact['date'].apply(convert_time)
        us_high_impact['date_original'] = pd.to_datetime(us_high_impact['date'])

        # 提取日期和时间
        us_high_impact['date_only'] = us_high_impact['date_beijing'].apply(
            lambda x: x.strftime('%Y-%m-%d') if x else ''
        )
        us_high_impact['time_only'] = us_high_impact['date_beijing'].apply(
            lambda x: x.strftime('%H:%M') if x else ''
        )
        us_high_impact['weekday'] = us_high_impact['date_beijing'].apply(
            lambda x: x.strftime('%A') if x else ''
        )

        # 按时间排序
        us_high_impact = us_high_impact.sort_values('date_original')

        # 选择显示的列
        display_cols = ['date_only', 'weekday', 'time_only', 'title', 'forecast', 'previous']
        result_df = us_high_impact[display_cols].copy()

        # 重命名列
        result_df.columns = ['日期', '星期', '时间(北京)', '事件', '预测值', '前值']

        return result_df, f"找到 {len(result_df)} 个美国高影响事件。"

    except requests.exceptions.RequestException as e:
        return pd.DataFrame(), f"网络错误: {e}"
    except Exception as e:
        return pd.DataFrame(), f"数据处理错误: {e}"


# 主界面
st.subheader("📊 本周美国高影响经济事件")

# 获取数据
events_df, message = fetch_and_filter_events()

st.info(message)

if not events_df.empty:
    # 今天和明天
    today = datetime.now(pytz.timezone('Asia/Shanghai')).date()
    tomorrow = today + timedelta(days=1)

    today_str = today.strftime('%Y-%m-%d')
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    # 按日期分组
    st.markdown("### 🗓️ 按日期查看")

    # 创建标签页
    tab_titles = ["所有事件", f"今天 ({today_str})", f"明天 ({tomorrow_str})", "即将发生"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:  # 所有事件
        st.dataframe(
            events_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "日期": st.column_config.TextColumn(width="medium"),
                "时间(北京)": st.column_config.TextColumn(width="small"),
                "事件": st.column_config.TextColumn(width="large"),
                "预测值": st.column_config.TextColumn(width="small"),
                "前值": st.column_config.TextColumn(width="small"),
            }
        )

    with tabs[1]:  # 今天
        today_events = events_df[events_df['日期'] == today_str]
        if not today_events.empty:
            st.dataframe(today_events, use_container_width=True, hide_index=True)
            st.metric("今日高影响事件数", len(today_events))
        else:
            st.success("🎉 今天没有高影响经济事件！")

    with tabs[2]:  # 明天
        tomorrow_events = events_df[events_df['日期'] == tomorrow_str]
        if not tomorrow_events.empty:
            st.dataframe(tomorrow_events, use_container_width=True, hide_index=True)
            st.metric("明日高影响事件数", len(tomorrow_events))
        else:
            st.info("明天没有高影响经济事件。")

    with tabs[3]:  # 即将发生
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        upcoming = []

        for _, row in events_df.iterrows():
            try:
                event_time = datetime.strptime(
                    f"{row['日期']} {row['时间(北京)']}",
                    '%Y-%m-%d %H:%M'
                ).replace(tzinfo=pytz.timezone('Asia/Shanghai'))

                if event_time > now:
                    time_diff = event_time - now
                    hours = time_diff.total_seconds() / 3600

                    if hours <= 24:  # 未来24小时内
                        upcoming.append({
                            **row.to_dict(),
                            '倒计时': f"{int(hours)}小时{int((hours % 1) * 60)}分钟"
                        })
            except:
                continue

        if upcoming:
            upcoming_df = pd.DataFrame(upcoming)
            st.dataframe(upcoming_df, use_container_width=True, hide_index=True)

            # 显示最近的事件
            next_event = upcoming[0]
            st.success(f"⏰ 下一个事件: **{next_event['事件']}** 于 {next_event['时间(北京)']} ({next_event['倒计时']}后)")
        else:
            st.info("未来24小时内没有即将发生的高影响事件。")

    # 统计信息
    st.markdown("### 📈 事件统计")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("总事件数", len(events_df))

    with col2:
        today_count = len(events_df[events_df['日期'] == today_str])
        st.metric("今日事件", today_count)

    with col3:
        # 计算包含预测值的事件数
        forecast_count = events_df['预测值'].notna().sum()
        st.metric("含预测事件", forecast_count)

    # 按星期分布
    st.markdown("#### 📅 按星期分布")
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_map = {
        'Monday': '周一',
        'Tuesday': '周二',
        'Wednesday': '周三',
        'Thursday': '周四',
        'Friday': '周五',
        'Saturday': '周六',
        'Sunday': '周日'
    }

    if '星期' in events_df.columns:
        # 转换为中文星期
        events_df['星期中文'] = events_df['星期'].map(weekday_map)

        # 按原始英文排序，但显示中文
        events_df['星期_排序'] = pd.Categorical(
            events_df['星期'],
            categories=weekday_order,
            ordered=True
        )

        weekday_counts = events_df.groupby(['星期_排序', '星期中文']).size().reset_index(name='数量')
        weekday_counts = weekday_counts.sort_values('星期_排序')

        # 显示条形图
        st.bar_chart(weekday_counts.set_index('星期中文')['数量'])

    # 数据下载
    st.markdown("### 💾 数据下载")
    csv_data = events_df.to_csv(index=False).encode('utf-8-sig')

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="下载CSV文件",
            data=csv_data,
            file_name=f"us_high_impact_events_{today_str}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # JSON格式
        json_data = events_df.to_json(orient='records', force_ascii=False, indent=2)
        st.download_button(
            label="下载JSON文件",
            data=json_data,
            file_name=f"us_high_impact_events_{today_str}.json",
            mime="application/json",
            use_container_width=True
        )

    # 原始数据预览
    with st.expander("查看原始数据样本"):
        st.dataframe(events_df.head(10), use_container_width=True, hide_index=True)

else:
    st.warning("当前没有找到符合条件的美国高影响经济事件。")
    st.markdown("""
    可能的原因：
    1. 本周确实没有美国高影响事件
    2. 数据源暂时没有更新
    3. 网络连接问题

    建议：
    - 稍后刷新页面重试
    - 检查网络连接
    - 确认数据源URL是否有效
    """)

# 页脚
st.markdown("---")
st.caption("数据来源: https://nfs.faireconomy.media/ff_calendar_thisweek.json")
st.caption("提示: 经济事件时间可能变动，请以官方发布为准。")