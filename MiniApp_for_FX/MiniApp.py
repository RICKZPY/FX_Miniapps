# market_economic_calendar_app.py
# 兼容Python 3.7的版本

import streamlit as st
import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime, date, timedelta
import warnings
import sys

# 检查Python版本
python_version = sys.version_info
#st.write(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

# 根据Python版本处理TypedDict导入
if python_version.major == 3 and python_version.minor >= 8:
    from typing import TypedDict
else:
    # Python 3.7的兼容处理
    try:
        from typing_extensions import TypedDict
    except ImportError:
        # 如果typing_extensions不可用，使用替代方案
        class TypedDict:
            def __init_subclass__(cls, **kwargs):
                pass

warnings.filterwarnings('ignore')

# 设置页面配置
st.set_page_config(
    page_title="全球市场与经济事件日历",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #37474F;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
        border-left: 4px solid #1E88E5;
        padding-left: 0.8rem;
    }
    .market-card {
        background: #667eea;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        color: white;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .event-card {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.6rem;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .fed-event { border-left-color: #FF5252; }
    .nfp-event { border-left-color: #FF9800; }
    .cpi-event { border-left-color: #4CAF50; }
    .earnings-event { border-left-color: #2196F3; }
    .trading-day { 
        background-color: #E3F2FD; 
        border-radius: 4px;
        padding: 0.2rem 0.4rem;
        margin: 0.1rem;
        display: inline-block;
        font-size: 0.85rem;
    }
    .holiday-day { 
        background-color: #FFEBEE; 
        border-radius: 4px;
        padding: 0.2rem 0.4rem;
        margin: 0.1rem;
        display: inline-block;
        font-size: 0.85rem;
    }
    .importance-high { color: #FF5252; font-weight: bold; }
    .importance-medium { color: #FF9800; font-weight: bold; }
    .importance-low { color: #4CAF50; font-weight: bold; }
    .highlight-box {
        background: #f5f7fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 市场配置 - 简化为几个主要市场
MARKETS = {
    "纽约证券交易所 (NYSE)": "NYSE",
    "纳斯达克 (NASDAQ)": "NASDAQ",
    "伦敦证券交易所 (LSE)": "LSE",
    "东京证券交易所 (JPX)": "JPX",
    "香港交易所 (XHKG)": "XHKG",
    "上海证券交易所 (SSE)": "SSE",
}


class EconomicCalendar:
    """经济事件日历类 - 简化版本"""

    def __init__(self):
        self.events_cache = {}

    def get_fed_meetings_2024(self):
        """获取2024年美联储议息会议日程"""
        return [
            {"date": "2024-01-30", "event": "FOMC会议", "importance": "high", "category": "fed",
             "description": "美联储议息会议，决定利率政策"},
            {"date": "2024-03-19", "event": "FOMC会议 + 经济预测", "importance": "very_high", "category": "fed",
             "description": "季度会议，包含经济预测和点阵图"},
            {"date": "2024-04-30", "event": "FOMC会议", "importance": "high", "category": "fed"},
            {"date": "2024-06-11", "event": "FOMC会议 + 经济预测", "importance": "very_high", "category": "fed"},
            {"date": "2024-07-30", "event": "FOMC会议", "importance": "high", "category": "fed"},
            {"date": "2024-09-17", "event": "FOMC会议 + 经济预测", "importance": "very_high", "category": "fed"},
            {"date": "2024-11-06", "event": "FOMC会议", "importance": "high", "category": "fed"},
            {"date": "2024-12-17", "event": "FOMC会议 + 经济预测", "importance": "very_high", "category": "fed"},
        ]

    def get_nfp_schedule_2024(self):
        """获取2024年非农就业数据发布时间"""
        nfp_dates = []
        months = [
            ("2024-01-05", "1月非农"),
            ("2024-02-02", "2月非农"),
            ("2024-03-08", "3月非农"),
            ("2024-04-05", "4月非农"),
            ("2024-05-03", "5月非农"),
            ("2024-06-07", "6月非农"),
            ("2024-07-05", "7月非农"),
            ("2024-08-02", "8月非农"),
            ("2024-09-06", "9月非农"),
            ("2024-10-04", "10月非农"),
            ("2024-11-01", "11月非农"),
            ("2024-12-06", "12月非农"),
        ]

        for date_str, event_name in months:
            nfp_dates.append({
                "date": date_str,
                "event": event_name + "就业数据",
                "importance": "very_high",
                "category": "nfp",
                "description": "美国非农就业人数变化、失业率"
            })

        return nfp_dates

    def get_cpi_schedule_2024(self):
        """获取2024年CPI数据发布时间"""
        cpi_dates = [
            {"date": "2024-01-11", "event": "12月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-02-13", "event": "1月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-03-12", "event": "2月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-04-10", "event": "3月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-05-15", "event": "4月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-06-12", "event": "5月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-07-11", "event": "6月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-08-14", "event": "7月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-09-11", "event": "8月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-10-10", "event": "9月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-11-14", "event": "10月CPI", "importance": "high", "category": "cpi"},
            {"date": "2024-12-11", "event": "11月CPI", "importance": "high", "category": "cpi"},
        ]

        return cpi_dates

    def get_earnings_season_2024(self):
        """获取2024年财报季重要日期"""
        return [
            {"date": "2024-01-15", "event": "Q4财报季开始", "importance": "medium", "category": "earnings"},
            {"date": "2024-01-25", "event": "苹果(AAPL)财报", "importance": "high", "category": "earnings"},
            {"date": "2024-01-30", "event": "微软(MSFT)财报", "importance": "high", "category": "earnings"},
            {"date": "2024-04-15", "event": "Q1财报季开始", "importance": "medium", "category": "earnings"},
            {"date": "2024-04-23", "event": "特斯拉(TSLA)财报", "importance": "high", "category": "earnings"},
            {"date": "2024-07-15", "event": "Q2财报季开始", "importance": "medium", "category": "earnings"},
            {"date": "2024-10-15", "event": "Q3财报季开始", "importance": "medium", "category": "earnings"},
            {"date": "2024-10-24", "event": "亚马逊(AMZN)财报", "importance": "high", "category": "earnings"},
        ]

    def get_all_economic_events(self, start_date=None, end_date=None):
        """获取所有经济事件"""
        if start_date is None:
            start_date = date.today().strftime('%Y-%m-%d')
        if end_date is None:
            end_date = (date.today() + timedelta(days=180)).strftime('%Y-%m-%d')

        # 获取所有事件
        all_events = []
        all_events.extend(self.get_fed_meetings_2024())
        all_events.extend(self.get_nfp_schedule_2024())
        all_events.extend(self.get_cpi_schedule_2024())
        all_events.extend(self.get_earnings_season_2024())

        # 转换为DataFrame
        df = pd.DataFrame(all_events)
        df['date'] = pd.to_datetime(df['date'])

        # 过滤日期范围
        start_dt = pd.Timestamp(start_date)
        end_dt = pd.Timestamp(end_date)

        mask = (df['date'] >= start_dt) & (df['date'] <= end_dt)
        filtered_df = df[mask].sort_values('date').reset_index(drop=True)

        return filtered_df


def get_market_info(market_code):
    """获取市场基本信息"""
    market_info = {
        "NYSE": {"name": "纽约证券交易所", "country": "美国", "currency": "USD", "open": "09:30", "close": "16:00"},
        "NASDAQ": {"name": "纳斯达克", "country": "美国", "currency": "USD", "open": "09:30", "close": "16:00"},
        "LSE": {"name": "伦敦证券交易所", "country": "英国", "currency": "GBP", "open": "08:00", "close": "16:30"},
        "JPX": {"name": "东京证券交易所", "country": "日本", "currency": "JPY", "open": "09:00", "close": "15:00"},
        "XHKG": {"name": "香港交易所", "country": "中国香港", "currency": "HKD", "open": "09:30", "close": "16:00"},
        "SSE": {"name": "上海证券交易所", "country": "中国", "currency": "CNY", "open": "09:30", "close": "15:00"},
    }
    return market_info.get(market_code,
                           {"name": market_code, "country": "未知", "currency": "未知", "open": "09:30", "close": "16:00"})


def get_market_calendar(market_code, start_date, end_date):
    """获取市场日历数据 - 安全版本"""
    try:
        calendar = mcal.get_calendar(market_code)
        schedule = calendar.schedule(start_date=start_date, end_date=end_date)

        # 计算总天数
        start_dt = pd.Timestamp(start_date)
        end_dt = pd.Timestamp(end_date)
        total_days = (end_dt - start_dt).days + 1

        return {
            'success': True,
            'schedule': schedule,
            'trading_days': len(schedule),
            'total_days': total_days,
            'market_code': market_code
        }
    except Exception as e:
        st.error(f"获取{market_code}日历错误: {str(e)[:100]}")
        return {
            'success': False,
            'error': str(e),
            'schedule': pd.DataFrame(),
            'trading_days': 0,
            'total_days': 0,
            'market_code': market_code
        }


def display_market_summary(market_info, market_data, events_count):
    """显示市场概要信息"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌍 市场", market_info['name'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if market_data['success']:
            st.metric("📅 交易日", market_data['trading_days'])
        else:
            st.metric("📅 交易日", "N/A")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 经济事件", events_count)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if market_data['success'] and market_data['total_days'] > 0:
            trading_ratio = (market_data['trading_days'] / market_data['total_days']) * 100
            st.metric("📈 交易比例", f"{trading_ratio:.1f}%")
        else:
            st.metric("📈 交易比例", "N/A")
        st.markdown('</div>', unsafe_allow_html=True)


def display_economic_events(events_df, market_schedule):
    """显示经济事件"""
    if events_df.empty:
        st.info("📭 该时间段内无经济事件")
        return

    st.markdown('<div class="sub-header">📅 经济事件日历</div>', unsafe_allow_html=True)

    # 创建显示数据
    display_data = []

    for idx, event in events_df.iterrows():
        date_str = event['date'].strftime('%Y-%m-%d')
        weekday = event['date'].strftime('%A')

        # 检查是否是交易日
        is_trading = False
        if hasattr(market_schedule, 'index'):
            is_trading = event['date'] in market_schedule.index

        # 重要性图标
        importance_icons = {
            'very_high': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }

        importance_icon = importance_icons.get(event.get('importance', 'medium'), '⚪')

        # 事件类型图标
        category_icons = {
            'fed': '🏛️',
            'nfp': '📊',
            'cpi': '📈',
            'earnings': '💰'
        }

        category_icon = category_icons.get(event.get('category', ''), '📅')

        display_data.append({
            '日期': date_str,
            '星期': weekday,
            '事件': f"{category_icon} {event['event']}",
            '重要性': f"{importance_icon} {event.get('importance', 'medium')}",
            '交易日': '✅' if is_trading else '❌',
            '描述': event.get('description', '')
        })

    # 创建DataFrame并显示
    display_df = pd.DataFrame(display_data)

    # 使用Streamlit的数据框显示
    st.dataframe(
        display_df,
        column_config={
            "日期": st.column_config.TextColumn("日期", width="small"),
            "星期": st.column_config.TextColumn("星期", width="small"),
            "事件": st.column_config.TextColumn("事件"),
            "重要性": st.column_config.TextColumn("重要性", width="small"),
            "交易日": st.column_config.TextColumn("交易日", width="small"),
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

    return display_df


def display_event_statistics(events_df):
    """显示事件统计"""
    if events_df.empty:
        return

    st.markdown('<div class="sub-header">📊 事件统计</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # 按类别统计
        if 'category' in events_df.columns:
            category_counts = events_df['category'].value_counts()

            # 简单文本显示
            st.write("**事件类别分布:**")
            for category, count in category_counts.items():
                category_names = {
                    'fed': '美联储会议',
                    'nfp': '非农数据',
                    'cpi': 'CPI数据',
                    'earnings': '财报季'
                }
                category_name = category_names.get(category, category)
                st.write(f"• {category_name}: {count}个")

    with col2:
        # 按重要性统计
        if 'importance' in events_df.columns:
            importance_counts = events_df['importance'].value_counts()

            st.write("**重要性分布:**")
            for importance, count in importance_counts.items():
                importance_names = {
                    'very_high': '极高',
                    'high': '高',
                    'medium': '中',
                    'low': '低'
                }
                importance_name = importance_names.get(importance, importance)
                st.write(f"• {importance_name}: {count}个")


def display_upcoming_events(events_df, days=7):
    """显示即将到来的事件"""
    today = pd.Timestamp(date.today())
    future_date = today + pd.Timedelta(days=days)

    upcoming = events_df[(events_df['date'] >= today) & (events_df['date'] <= future_date)]

    if not upcoming.empty:
        st.markdown(f'<div class="sub-header">🔔 未来{days}天重要事件</div>', unsafe_allow_html=True)

        for idx, event in upcoming.iterrows():
            days_to_event = (event['date'].date() - date.today()).days

            # 创建卡片
            with st.container():
                col1, col2 = st.columns([1, 4])

                with col1:
                    # 事件图标
                    category_icons = {
                        'fed': '🏛️',
                        'nfp': '📊',
                        'cpi': '📈',
                        'earnings': '💰'
                    }
                    icon = category_icons.get(event.get('category', ''), '📅')
                    st.markdown(f"<h2>{icon}</h2>", unsafe_allow_html=True)

                with col2:
                    # 事件详情
                    st.markdown(f"**{event['event']}**")
                    st.markdown(f"📅 {event['date'].strftime('%Y-%m-%d %A')} ({days_to_event}天后)")

                    if 'description' in event and pd.notna(event['description']):
                        st.caption(f"📝 {event['description']}")

                st.markdown("---")


def display_trading_tips():
    """显示交易提示"""
    st.markdown('<div class="sub-header">💡 交易提示</div>', unsafe_allow_html=True)

    tips = [
        ("🏛️ 美联储会议日", "市场波动通常加大，建议减少仓位或使用期权对冲"),
        ("📊 非农数据日", "就业数据对货币政策影响重大，关注美元和黄金反应"),
        ("📈 CPI数据日", "通胀数据直接影响利率预期，关注债券和成长股"),
        ("💰 财报季", "个股波动加大，建议分散投资，避免单一股票风险"),
        ("📅 节假日前后", "市场流动性可能降低，注意调整交易策略")
    ]

    for icon, tip in tips:
        with st.expander(f"{icon} {tip.split('，')[0]}"):
            st.write(tip)


def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">📈 市场与经济事件日历</h1>', unsafe_allow_html=True)

    # 侧边栏
    with st.sidebar:
        st.markdown("### ⚙️ 设置")

        # 市场选择
        selected_market = st.selectbox(
            "选择市场",
            list(MARKETS.keys()),
            index=0
        )
        market_code = MARKETS[selected_market]
        market_info = get_market_info(market_code)

        st.markdown("---")
        st.markdown("### 📅 日期范围")

        # 日期选择
        today = date.today()

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "开始日期",
                value=today - timedelta(days=30),
                max_value=today + timedelta(days=365)
            )
        with col2:
            end_date = st.date_input(
                "结束日期",
                value=today + timedelta(days=90),
                min_value=start_date,
                max_value=today + timedelta(days=730)
            )

        st.markdown("---")
        st.markdown("### 🚀 快速选择")

        # 快速选择按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("最近30天"):
                start_date = today - timedelta(days=30)
                end_date = today
        with col2:
            if st.button("未来90天"):
                start_date = today
                end_date = today + timedelta(days=90)

        st.markdown("---")
        st.markdown("### 👁️ 显示选项")

        show_upcoming = st.checkbox("显示即将发生的事件", value=True)
        show_tips = st.checkbox("显示交易提示", value=True)
        days_ahead = st.slider("显示未来几天", 1, 30, 7)

        st.markdown("---")
        st.markdown("### 📖 关于")
        st.info("""
        功能说明：
        - 查看全球主要市场交易日历
        - 跟踪重要经济事件（美联储会议、非农数据等）
        - 获取交易提示和建议
        - 支持Python 3.7+
        """)

    # 主内容区域
    st.markdown(f"""
    <div class="market-card">
        <h3>🏛️ {market_info['name']}</h3>
        <p>📍 {market_info['country']} | 💰 {market_info['currency']} | 🕐 {market_info['open']}-{market_info['close']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 获取数据
    econ_calendar = EconomicCalendar()
    events_df = econ_calendar.get_all_economic_events(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    market_data = get_market_calendar(
        market_code,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    # 显示市场概要
    display_market_summary(market_info, market_data, len(events_df))

    # 显示即将发生的事件
    if show_upcoming:
        display_upcoming_events(events_df, days_ahead)

    # 显示经济事件
    display_economic_events(events_df, market_data.get('schedule', pd.DataFrame()))

    # 显示事件统计
    display_event_statistics(events_df)

    # 显示交易提示
    if show_tips:
        display_trading_tips()

    # 数据下载
    if not events_df.empty:
        st.markdown('<div class="sub-header">💾 数据导出</div>', unsafe_allow_html=True)

        # 准备CSV数据
        csv_data = events_df.to_csv(index=False).encode('utf-8-sig')

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📥 下载CSV",
                data=csv_data,
                file_name=f"economic_events_{market_code}_{today}.csv",
                mime="text/csv"
            )

        with col2:
            # JSON数据
            json_data = events_df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="📥 下载JSON",
                data=json_data,
                file_name=f"economic_events_{market_code}_{today}.json",
                mime="application/json"
            )

    # 底部信息
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>📅 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Python {python_version.major}.{python_version.minor}.{python_version.micro}</p>
        <p>⚠️ 提示: 事件日期可能变更，请以官方发布为准</p>
    </div>
    """, unsafe_allow_html=True)


# 简化版本，不需要plotly和yfinance
if __name__ == "__main__":
    try:
        # 检查依赖
        import pandas_market_calendars

        st.success("✅ 系统准备就绪")
        main()
    except ImportError as e:
        st.error(f"❌ 缺少依赖库: {e}")
        st.info("请安装必要依赖: pip install streamlit pandas pandas_market_calendars")