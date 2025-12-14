import pandas_market_calendars as mcal
import pandas as pd
from datetime import datetime, date, timedelta
import warnings

warnings.filterwarnings('ignore')


def get_market_events(calendar_name='NYSE', start_date=None, end_date=None):
    """
    获取指定市场的重要事件日历 - 修正版
    """

    # 设置默认日期范围
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    try:
        # 获取指定市场的日历
        calendar = mcal.get_calendar(calendar_name)

        print(f"=== {calendar_name} 市场事件日历 ({start_date} 到 {end_date}) ===")

        # 1. 获取交易日程
        schedule = calendar.schedule(start_date=start_date, end_date=end_date)
        print(f"\n1. 交易日历:")
        print(f"   交易日总数: {len(schedule)}天")
        if len(schedule) > 0:
            print(f"   第一个交易日: {schedule.index[0].date()}")
            print(f"   最后一个交易日: {schedule.index[-1].date()}")

        # 2. 获取市场交易时间
        print(f"\n2. 市场交易时间:")
        try:
            # 尝试获取交易时间
            test_schedule = calendar.schedule(start_date=start_date,
                                              end_date=start_date)
            if len(test_schedule) > 0:
                market_open = test_schedule.iloc[0]['market_open']
                market_close = test_schedule.iloc[0]['market_close']
                open_time = market_open.strftime('%H:%M')
                close_time = market_close.strftime('%H:%M')
                print(f"   常规交易时间: {open_time} - {close_time}")
            else:
                # 使用常见市场的默认值
                default_hours = {
                    'NYSE': ('09:30', '16:00'),
                    'NASDAQ': ('09:30', '16:00'),
                    'XHKG': ('09:30', '16:00'),
                    'SSE': ('09:30', '15:00'),
                    'SZSE': ('09:30', '15:00'),
                    'JPX': ('09:00', '15:00'),
                    'LSE': ('08:00', '16:30'),
                    'TSX': ('09:30', '16:00'),
                    'ASX': ('10:00', '16:00'),
                }
                if calendar_name in default_hours:
                    open_time, close_time = default_hours[calendar_name]
                    print(f"   常规交易时间: {open_time} - {close_time}")
                else:
                    print(f"   常规交易时间: 09:30 - 16:00 (默认)")
        except Exception as e:
            print(f"   无法获取交易时间: {e}")
            print(f"   常规交易时间: 09:30 - 16:00 (默认)")

        # 3. 获取节假日 - 修正版本
        print(f"\n3. 节假日/休市日:")
        try:
            # 方法1：使用 holidays().holidays 属性
            if hasattr(calendar, 'holidays'):
                holidays_obj = calendar.holidays()
                # 检查是否有 holidays 属性
                if hasattr(holidays_obj, 'holidays'):
                    holidays_list = holidays_obj.holidays
                    if isinstance(holidays_list, pd.DatetimeIndex):
                        # 转换为日期字符串列表
                        all_holidays = [pd.Timestamp(h).strftime('%Y-%m-%d')
                                        for h in holidays_list]
                    elif isinstance(holidays_list, list):
                        all_holidays = [h.strftime('%Y-%m-%d') for h in holidays_list]
                    else:
                        all_holidays = []
                else:
                    all_holidays = []
            else:
                all_holidays = []

            # 过滤指定日期范围内的节假日
            recent_holidays = []
            for holiday in all_holidays:
                if start_date <= holiday <= end_date:
                    recent_holidays.append(holiday)

            if recent_holidays:
                print(f"   近期节假日:")
                for holiday in sorted(recent_holidays)[:10]:  # 只显示前10个
                    holiday_date = datetime.strptime(holiday, '%Y-%m-%d')
                    print(f"   {holiday} ({holiday_date.strftime('%A')})")
                if len(recent_holidays) > 10:
                    print(f"   ... 共{len(recent_holidays)}个节假日")
            else:
                print(f"   近期无节假日")

        except Exception as e:
            print(f"   获取节假日失败: {e}")

        # 4. 显示具体的交易日
        print(f"\n4. 交易日列表:")
        if len(schedule) > 0:
            trading_days = []
            for date_idx in schedule.index:
                date_str = date_idx.strftime('%Y-%m-%d')
                weekday = date_idx.strftime('%A')
                trading_days.append(f"{date_str} ({weekday})")

            for i, day in enumerate(trading_days[:10]):  # 只显示前10个
                print(f"   {day}")
            if len(trading_days) > 10:
                print(f"   ... 共{len(trading_days)}个交易日")
        else:
            print(f"   该时间段内无交易日")

        # 5. 统计信息
        print(f"\n5. 统计信息:")
        total_days = (datetime.strptime(end_date, '%Y-%m-%d') -
                      datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        print(f"   总天数: {total_days}")
        print(f"   交易日: {len(schedule)}")
        print(f"   非交易日: {total_days - len(schedule)}")
        if total_days > 0:
            trading_ratio = (len(schedule) / total_days) * 100
            print(f"   交易日比例: {trading_ratio:.1f}%")

        return {
            'calendar_name': calendar_name,
            'schedule': schedule,
            'trading_days_count': len(schedule),
            'date_range': {'start': start_date, 'end': end_date},
            'total_days': total_days
        }

    except Exception as e:
        print(f"获取{calendar_name}日历失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_holidays_fixed(calendar, start_date, end_date):
    """
    修正版获取节假日函数
    """
    try:
        # 方法1：使用 holidays() 方法
        holidays_obj = calendar.holidays()

        # 不同的库版本返回不同的对象类型
        if isinstance(holidays_obj, pd.DatetimeIndex):
            # 直接是 DatetimeIndex
            holidays_list = list(holidays_obj)
        elif hasattr(holidays_obj, 'holidays'):
            # 有 holidays 属性
            holidays_list = list(holidays_obj.holidays)
        elif hasattr(holidays_obj, '__iter__'):
            # 可迭代对象
            holidays_list = list(holidays_obj)
        else:
            # 尝试其他方法
            holidays_list = []

        # 转换为字符串格式
        holidays_str = []
        for h in holidays_list:
            if isinstance(h, (pd.Timestamp, datetime)):
                holidays_str.append(h.strftime('%Y-%m-%d'))
            elif isinstance(h, str):
                holidays_str.append(h)

        # 过滤日期范围
        filtered_holidays = [h for h in holidays_str
                             if start_date <= h <= end_date]

        return filtered_holidays

    except Exception as e:
        print(f"获取节假日失败: {e}")
        return []


def check_trading_day_simple(market='NYSE', check_date=None):
    """
    简化版检查交易日
    """
    if check_date is None:
        check_date = datetime.now().strftime('%Y-%m-%d')

    try:
        calendar = mcal.get_calendar(market)
        schedule = calendar.schedule(start_date=check_date, end_date=check_date)

        check_date_obj = datetime.strptime(check_date, '%Y-%m-%d')
        weekday = check_date_obj.strftime('%A')

        if not schedule.empty:
            print(f"\n✓ {check_date} ({weekday}) 是 {market} 的交易日")
            return True
        else:
            print(f"\n✗ {check_date} ({weekday}) 不是 {market} 的交易日")

            # 检查是否是周末
            if check_date_obj.weekday() >= 5:
                print(f"  原因: 周末")
            else:
                # 尝试获取节假日信息
                holidays = get_holidays_fixed(calendar, check_date, check_date)
                if holidays:
                    print(f"  原因: 节假日")
                else:
                    print(f"  原因: 特殊休市日")

            return False

    except Exception as e:
        print(f"检查失败: {e}")
        return None


def get_market_calendar_simple(market='NYSE', months=1):
    """
    简化版获取市场日历
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    try:
        calendar = mcal.get_calendar(market)
        schedule = calendar.schedule(start_date=start_str, end_date=end_str)

        print(f"\n{market} 日历 ({start_str} 到 {end_str})")
        print("-" * 50)

        # 按周分组显示
        week_data = {}
        for date_idx in schedule.index:
            week_num = date_idx.isocalendar()[1]  # 周数
            if week_num not in week_data:
                week_data[week_num] = []
            week_data[week_num].append(date_idx.strftime('%Y-%m-%d %A'))

        for week_num in sorted(week_data.keys()):
            print(f"\n第 {week_num} 周:")
            for day in week_data[week_num]:
                print(f"  {day}")

        # 节假日
        holidays = get_holidays_fixed(calendar, start_str, end_str)
        if holidays:
            print(f"\n节假日:")
            for holiday in sorted(holidays):
                holiday_date = datetime.strptime(holiday, '%Y-%m-%d')
                print(f"  {holiday} ({holiday_date.strftime('%A')})")

        return {
            'market': market,
            'schedule': schedule,
            'holidays': holidays,
            'trading_days': len(schedule)
        }

    except Exception as e:
        print(f"获取{market}日历失败: {e}")
        return None


def get_next_n_trading_days(market='NYSE', n=10, start_date=None):
    """
    获取未来N个交易日
    """
    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')

    try:
        calendar = mcal.get_calendar(market)

        # 搜索未来足够多的天数以确保找到N个交易日
        search_days = n * 3  # 假设大约1/3的日子是交易日

        # 计算结束日期
        start_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_obj = start_obj + timedelta(days=search_days)
        end_date = end_obj.strftime('%Y-%m-%d')

        # 获取日程
        schedule = calendar.schedule(start_date=start_date, end_date=end_date)

        # 获取交易日列表
        trading_days = []
        for date_idx in schedule.index:
            if date_idx >= pd.Timestamp(start_date):
                trading_days.append(date_idx)
                if len(trading_days) >= n:
                    break

        print(f"\n{market} 未来{n}个交易日:")
        print("-" * 30)

        for i, day in enumerate(trading_days, 1):
            day_str = day.strftime('%Y-%m-%d %A')
            print(f"{i:2d}. {day_str}")

            # 获取交易时间
            day_schedule = calendar.schedule(start_date=day.strftime('%Y-%m-%d'),
                                             end_date=day.strftime('%Y-%m-%d'))
            if not day_schedule.empty:
                market_open = day_schedule.iloc[0]['market_open']
                market_close = day_schedule.iloc[0]['market_close']
                print(f"    交易时间: {market_open.strftime('%H:%M')} - {market_close.strftime('%H:%M')}")

        return trading_days

    except Exception as e:
        print(f"获取交易日失败: {e}")
        return []


# =========== 使用示例 ===========

if __name__ == "__main__":

    print("市场日历工具 - 完全修正版")
    print("=" * 60)

    # 显示库版本信息
    try:
        print(f"pandas_market_calendars 版本: {mcal.__version__}")
    except:
        print("无法获取库版本信息")

    print("\n" + "=" * 60)

    # 示例1: 获取NYSE日历
    print("\n示例1: 获取NYSE市场日历")
    nyse_result = get_market_events('NYSE',
                                    start_date='2024-01-01',
                                    end_date='2024-01-31')

    print("\n" + "=" * 60)

    # 示例2: 检查交易日
    print("\n示例2: 检查交易日状态")

    # 检查今天
    today = datetime.now().strftime('%Y-%m-%d')
    check_trading_day_simple('NYSE', today)

    # 检查几个特定日期
    test_dates = ['2024-01-01', '2024-07-04', '2024-12-25']  # 节假日
    for test_date in test_dates:
        check_trading_day_simple('NYSE', test_date)

    print("\n" + "=" * 60)

    # 示例3: 获取简化版日历
    print("\n示例3: 简化版日历查看")
    simple_cal = get_market_calendar_simple('NYSE', months=1)

    print("\n" + "=" * 60)

    # 示例4: 获取未来交易日
    print("\n示例4: 获取未来交易日")
    future_days = get_next_n_trading_days('NYSE', n=5)

    print("\n" + "=" * 60)

    # 示例5: 测试多个市场
    print("\n示例5: 测试多个市场")

    markets = ['XHKG', 'LSE', 'JPX', 'SSE']
    for market in markets:
        print(f"\n--- {market} ---")
        try:
            # 获取最近一个月的日历
            result = get_market_events(
                market,
                start_date=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                end_date=datetime.now().strftime('%Y-%m-%d')
            )
            if result:
                print(f"✓ 成功获取{market}日历数据")
        except Exception as e:
            print(f"✗ 获取{market}失败: {e}")