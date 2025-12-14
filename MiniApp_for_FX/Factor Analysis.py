import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import stats
import warnings

warnings.filterwarnings('ignore')


class USDCNYFactorAnalyzer:
    """美元人民币影响因子深度挖掘系统"""

    def __init__(self):
        self.factors_data = {}
        self.correlation_matrix = None
        self.importance_ranking = None

    def fetch_macro_economic_data(self):
        """获取宏观经济因子数据"""
        print("📊 获取宏观经济因子数据...")

        # 这里模拟数据，实际应用中需要连接API
        macro_factors = {
            'us_inflation': {'current': 3.2, 'prev': 3.4, 'trend': '下降'},  # 美国通胀
            'cn_inflation': {'current': 0.1, 'prev': 0.2, 'trend': '低通胀'},  # 中国通胀
            'us_gdp_growth': {'current': 2.1, 'prev': 2.0, 'trend': '稳定'},  # 美国GDP增长
            'cn_gdp_growth': {'current': 5.2, 'prev': 4.9, 'trend': '复苏'},  # 中国GDP增长
            'us_unemployment': {'current': 3.8, 'prev': 3.9, 'trend': '良好'},  # 美国失业率
            'cn_unemployment': {'current': 5.2, 'prev': 5.3, 'trend': '改善'},  # 中国失业率
            'trade_balance': {'current': -682, 'prev': -655, 'trend': '赤字扩大'},  # 中美贸易差额
        }

        self.factors_data['macro'] = macro_factors
        return macro_factors

    def fetch_monetary_policy_data(self):
        """获取货币政策因子"""
        print("🏦 获取货币政策因子数据...")

        monetary_factors = {
            'fed_funds_rate': {'current': 5.33, 'prev': 5.25, 'direction': 'hawkish'},  # 美联储利率
            'pboc_mlf_rate': {'current': 2.50, 'prev': 2.50, 'direction': 'accommodative'},  # 中国MLF利率
            'us_yield_10y': {'current': 4.28, 'prev': 4.15, 'trend': '上升'},  # 美债10年收益率
            'cn_yield_10y': {'current': 2.65, 'prev': 2.70, 'trend': '下降'},  # 中债10年收益率
            'interest_rate_diff': {'current': 2.68, 'prev': 2.55, 'impact': 'positive_usd'},  # 中美利差
            'us_balance_sheet': {'current': 7.42, 'prev': 7.45, 'trend': '收缩'},  # 美联储资产负债表
            'pboc_reserve_ratio': {'current': 7.4, 'prev': 7.4, 'trend': '稳定'},  # 中国存款准备金率
        }

        self.factors_data['monetary'] = monetary_factors
        return monetary_factors

    def fetch_market_sentiment_data(self):
        """获取市场情绪因子"""
        print("📈 获取市场情绪因子数据...")

        sentiment_factors = {
            'dxy_index': {'current': 104.5, 'prev': 103.8, 'trend': '强势'},  # 美元指数
            'cnh_cny_spread': {'current': 150, 'prev': 120, 'trend': '扩大'},  # 离岸在岸价差
            'risk_appetite': {'current': 0.65, 'prev': 0.60, 'trend': 'risk_on'},  # 风险偏好
            'volatility_index': {'current': 15.2, 'prev': 14.8, 'trend': '上升'},  # 波动率指数
            'speculative_positions': {'current': 'net_long_usd', 'prev': 'net_short', 'trend': '转多'},  # 投机头寸
            'capital_flows': {'current': 'outflow_cn', 'prev': 'inflow', 'trend': '流出'},  # 资本流动
        }

        self.factors_data['sentiment'] = sentiment_factors
        return sentiment_factors

    def fetch_political_geopolitical_data(self):
        """获取政治地缘因子"""
        print("🌍 获取政治地缘因子数据...")

        political_factors = {
            'us_china_tensions': {'level': 'high', 'trend': '加剧', 'impact': 'negative_cny'},  # 中美关系
            'trade_war_status': {'level': 'ongoing', 'tariffs': 'maintained', 'impact': 'mixed'},  # 贸易战状态
            'taiwan_issue': {'level': 'sensitive', 'recent_events': 'increased_activity', 'impact': 'risk_off'},  # 台湾问题
            'tech_decoupling': {'level': 'accelerating', 'impact': 'negative_cny'},  # 科技脱钩
            'global_alliances': {'us_strength': 'strong', 'cn_outreach': 'expanding', 'impact': 'complex'},  # 全球联盟
        }

        self.factors_data['political'] = political_factors
        return political_factors

    def fetch_technical_factors(self):
        """获取技术分析因子"""
        print("📉 获取技术分析因子数据...")

        technical_factors = {
            'usdcny_price': {'current': 7.1850, 'ma20': 7.1650, 'ma50': 7.1500, 'trend': 'uptrend'},
            'rsi_14': {'value': 62, 'signal': 'neutral_bullish', 'overbought': False},
            'macd': {'value': 0.0025, 'signal': 0.0018, 'histogram': 0.0007, 'trend': 'bullish'},
            'bollinger_bands': {'upper': 7.2100, 'middle': 7.1750, 'lower': 7.1400, 'width': 'expanding'},
            'support_levels': [7.1500, 7.1200, 7.0800],
            'resistance_levels': [7.2000, 7.2300, 7.2500],
            'volume_trend': {'current': 'increasing', 'avg_ratio': 1.2},
        }

        self.factors_data['technical'] = technical_factors
        return technical_factors

    def calculate_factor_correlations(self):
        """计算因子相关性矩阵"""
        print("\n🔗 计算因子相关性...")

        # 创建模拟历史数据（实际应用应从数据库获取）
        np.random.seed(42)
        n_periods = 100

        # 模拟各因子对USDCNY的影响
        factors = {
            'interest_rate_diff': np.random.normal(2.5, 0.3, n_periods),  # 中美利差
            'inflation_diff': np.random.normal(3.0, 0.5, n_periods),  # 通胀差
            'trade_balance': np.random.normal(-600, 100, n_periods),  # 贸易差额
            'dxy_index': np.random.normal(104, 2, n_periods),  # 美元指数
            'risk_appetite': np.random.uniform(0.3, 0.8, n_periods),  # 风险偏好
            'capital_flows': np.random.normal(-10, 5, n_periods),  # 资本流动
            'political_tension': np.random.uniform(0, 1, n_periods),  # 政治紧张度
        }

        # 模拟USDCNY汇率（基于因子线性组合加上噪声）
        usdcny = (
                7.0 +
                0.3 * factors['interest_rate_diff'] +
                0.15 * factors['inflation_diff'] +
                0.0005 * factors['trade_balance'] +
                0.02 * factors['dxy_index'] +
                -0.1 * factors['risk_appetite'] +
                -0.005 * factors['capital_flows'] +
                0.05 * factors['political_tension'] +
                np.random.normal(0, 0.01, n_periods)
        )

        # 创建DataFrame
        df = pd.DataFrame(factors)
        df['usdcny'] = usdcny

        # 计算相关系数
        correlation_matrix = df.corr()
        self.correlation_matrix = correlation_matrix

        return correlation_matrix

    def perform_granger_causality_test(self):
        """执行格兰杰因果关系检验（简化的模拟版本）"""
        print("\n🎯 格兰杰因果关系分析...")

        # 在实际应用中，这里应该使用statsmodels的grangercausalitytests
        # 这里我们用模拟结果展示

        causality_results = {
            'interest_rate_diff -> USDCNY': {'p_value': 0.0012, 'causal': True, 'lag': 2},
            'dxy_index -> USDCNY': {'p_value': 0.0034, 'causal': True, 'lag': 1},
            'trade_balance -> USDCNY': {'p_value': 0.0456, 'causal': True, 'lag': 3},
            'capital_flows -> USDCNY': {'p_value': 0.0123, 'causal': True, 'lag': 1},
            'political_tension -> USDCNY': {'p_value': 0.1234, 'causal': False, 'lag': 1},
            'risk_appetite -> USDCNY': {'p_value': 0.2345, 'causal': False, 'lag': 2},
        }

        return causality_results

    def calculate_factor_importance(self):
        """计算因子重要性排序"""
        print("\n📊 计算因子重要性...")

        # 使用随机森林特征重要性模拟（实际应用应训练模型）
        importance_scores = {
            '中美利差': 0.28,
            '美元指数走势': 0.22,
            '资本流动方向': 0.18,
            '贸易差额变化': 0.15,
            '中美通胀差': 0.08,
            '地缘政治风险': 0.05,
            '市场风险偏好': 0.04,
        }

        # 排序
        sorted_importance = dict(sorted(importance_scores.items(),
                                        key=lambda x: x[1], reverse=True))

        self.importance_ranking = sorted_importance
        return sorted_importance

    def perform_regime_analysis(self):
        """执行状态识别分析（不同市场环境下的因子表现）"""
        print("\n🔄 市场状态识别分析...")

        regimes = {
            'risk_on_env': {
                'description': '风险偏好环境',
                'dominant_factors': ['risk_appetite', 'capital_flows', 'growth_diff'],
                'usdcny_bias': 'depreciation_pressure',
                'volatility': 'moderate',
            },
            'risk_off_env': {
                'description': '避险环境',
                'dominant_factors': ['dxy_index', 'safe_haven', 'political_risk'],
                'usdcny_bias': 'appreciation_pressure',
                'volatility': 'high',
            },
            'hawkish_fed_env': {
                'description': '美联储鹰派环境',
                'dominant_factors': ['interest_rate_diff', 'us_yields', 'capital_flows'],
                'usdcny_bias': 'strong_appreciation',
                'volatility': 'moderate_high',
            },
            'pboc_intervention_env': {
                'description': '央行干预环境',
                'dominant_factors': ['policy_intervention', 'fixing_bias', 'state_banks'],
                'usdcny_bias': 'managed_range',
                'volatility': 'suppressed',
            },
        }

        # 判断当前市场状态
        current_regime = self._identify_current_regime()
        regimes['current_regime'] = current_regime

        return regimes

    def _identify_current_regime(self):
        """识别当前市场状态"""
        # 基于多个指标的综合判断
        indicators = {
            'volatility_index': 15.2,  # 低波动
            'risk_appetite': 0.65,  # 中等风险偏好
            'interest_rate_diff': 2.68,  # 利差扩大
            'dxy_trend': 'rising',  # 美元走强
        }

        if indicators['interest_rate_diff'] > 2.5 and indicators['dxy_trend'] == 'rising':
            return 'hawkish_fed_env'
        elif indicators['volatility_index'] < 20 and indicators['risk_appetite'] > 0.6:
            return 'risk_on_env'
        else:
            return 'normal_trading_env'

    def generate_interaction_effects(self):
        """分析因子交互效应"""
        print("\n⚡ 因子交互效应分析...")

        interactions = {
            '利差与资本流动': {
                'description': '利差扩大通常伴随资本流出中国，强化USDCNY上涨',
                'magnitude': '强',
                'direction': 'synergistic',
                'recent_evidence': 'observed_2023_h2',
            },
            '美元指数与风险偏好': {
                'description': '避险情绪推高美元，但极端避险可能引发流动性问题',
                'magnitude': '中等',
                'direction': 'complex',
                'recent_evidence': 'observed_during_covid',
            },
            '贸易战与供应链': {
                'description': '贸易紧张导致供应链重构，长期削弱人民币贸易支持',
                'magnitude': '长期显著',
                'direction': 'negative_cny',
                'recent_evidence': 'ongoing_since_2018',
            },
            '央行政策协调': {
                'description': '中美央行政策分化程度决定汇率波动区间',
                'magnitude': '决定性',
                'direction': 'regime_defining',
                'recent_evidence': 'major_driver_2022_2023',
            },
        }

        return interactions

    def create_comprehensive_report(self):
        """生成综合分析报告"""
        print("\n" + "=" * 80)
        print("美元人民币(USD/CNY)深度影响因子分析报告")
        print("=" * 80)

        # 收集所有数据
        self.fetch_macro_economic_data()
        self.fetch_monetary_policy_data()
        self.fetch_market_sentiment_data()
        self.fetch_political_geopolitical_data()
        self.fetch_technical_factors()

        # 执行分析
        correlations = self.calculate_factor_correlations()
        causality = self.perform_granger_causality_test()
        importance = self.calculate_factor_importance()
        regimes = self.perform_regime_analysis()
        interactions = self.generate_interaction_effects()

        # 生成报告
        report = {
            'executive_summary': self._generate_executive_summary(),
            'key_drivers': importance,
            'current_regime': regimes.get('current_regime'),
            'risk_assessment': self._assess_risks(),
            'forecast_scenarios': self._create_scenarios(),
            'monitoring_priority': self._set_monitoring_priority(importance),
        }

        return report

    def _generate_executive_summary(self):
        """生成执行摘要"""
        summary = """
        当前USD/CNY汇率主要受到以下因素驱动：

        1. **货币政策分化**：美联储维持鹰派 vs 中国央行宽松，利差扩大支撑美元
        2. **经济周期错位**：美国经济韧性 vs 中国复苏不均衡
        3. **资本流动压力**：套息交易和资产配置调整导致资金流出中国
        4. **技术面突破**：汇率突破关键阻力位，技术性买盘增加

        短期展望：在缺乏重大政策变化下，USD/CNY偏向测试7.20-7.25区间。
        """
        return summary

    def _assess_risks(self):
        """风险评估"""
        risks = {
            'upside_risks_usd': [
                '美联储意外加息',
                '中国房地产风险加剧',
                '地缘政治紧张升级',
                '全球避险情绪飙升'
            ],
            'downside_risks_usd': [
                '中国强刺激政策推出',
                '美联储提前降息',
                '中美关系大幅改善',
                '全球风险偏好强烈回升'
            ],
            'tail_risks': [
                '中国资本管制加强',
                '美国债务危机',
                '台海局势突变',
                '全球衰退深化'
            ]
        }
        return risks

    def _create_scenarios(self):
        """创建情景分析"""
        scenarios = {
            'bullish_usd_scenario': {
                'probability': 40,
                'triggers': ['fed_hikes_again', 'cn_economy_struggles'],
                'usdcny_target': '7.30-7.40',
                'timeframe': '3-6_months',
            },
            'range_bound_scenario': {
                'probability': 50,
                'triggers': ['policy_stability', 'managed_float'],
                'usdcny_target': '7.10-7.25',
                'timeframe': '3_months',
            },
            'bearish_usd_scenario': {
                'probability': 10,
                'triggers': ['fed_cuts_early', 'cn_stimulus_works'],
                'usdcny_target': '7.00-7.10',
                'timeframe': '6_months',
            },
        }
        return scenarios

    def _set_monitoring_priority(self, importance):
        """设置监控优先级"""
        priorities = {
            'high_priority': list(importance.keys())[:3],  # 前三个最重要因子
            'medium_priority': [
                '中国央行中间价信号',
                '离岸流动性变化',
                '企业结售汇行为'
            ],
            'event_risks': [
                '美联储议息会议',
                '中国政治局会议',
                '中美高层对话',
                '中国贸易数据'
            ]
        }
        return priorities

    def visualize_factor_analysis(self):
        """可视化分析结果"""
        if self.importance_ranking is None:
            self.calculate_factor_importance()

        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 1. 因子重要性条形图
        factors = list(self.importance_ranking.keys())
        scores = list(self.importance_ranking.values())

        axes[0, 0].barh(factors, scores, color='steelblue')
        axes[0, 0].set_xlabel('重要性得分')
        axes[0, 0].set_title('USD/CNY影响因子重要性排序')
        axes[0, 0].invert_yaxis()

        # 2. 相关性热力图（模拟）
        if self.correlation_matrix is not None:
            im = axes[0, 1].imshow(self.correlation_matrix.values, cmap='coolwarm',
                                   vmin=-1, vmax=1)
            axes[0, 1].set_title('因子相关性热力图')
            axes[0, 1].set_xticks(range(len(self.correlation_matrix.columns)))
            axes[0, 1].set_xticklabels(self.correlation_matrix.columns, rotation=45)
            axes[0, 1].set_yticks(range(len(self.correlation_matrix.index)))
            axes[0, 1].set_yticklabels(self.correlation_matrix.index)
            plt.colorbar(im, ax=axes[0, 1])

        # 3. 情景分析饼图
        scenarios = self._create_scenarios()
        labels = [k.replace('_scenario', '').replace('_', ' ').title()
                  for k in scenarios.keys()]
        sizes = [s['probability'] for s in scenarios.values()]
        colors = ['#ff9999', '#66b3ff', '#99ff99']

        axes[1, 0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                       startangle=90)
        axes[1, 0].set_title('USD/CNY情景分析概率分布')

        # 4. 风险矩阵
        risks = ['货币政策风险', '经济数据风险', '地缘政治风险', '市场情绪风险']
        impact = [8, 6, 9, 5]
        probability = [7, 8, 4, 6]

        scatter = axes[1, 1].scatter(probability, impact, s=200, alpha=0.6,
                                     c=range(len(risks)), cmap='viridis')
        axes[1, 1].set_xlabel('发生概率 (1-10)')
        axes[1, 1].set_ylabel('影响程度 (1-10)')
        axes[1, 1].set_title('风险矩阵分析')
        axes[1, 1].grid(True, alpha=0.3)

        # 添加风险标签
        for i, risk in enumerate(risks):
            axes[1, 1].annotate(risk, (probability[i], impact[i]),
                                xytext=(5, 5), textcoords='offset points')

        plt.tight_layout()
        plt.show()


def main():
    """主函数"""
    print("=" * 80)
    print("美元人民币(USD/CNY)深度影响因子挖掘系统")
    print("=" * 80)

    # 初始化分析器
    analyzer = USDCNYFactorAnalyzer()

    # 生成综合分析报告
    report = analyzer.create_comprehensive_report()

    # 打印报告
    print("\n📋 执行摘要:")
    print(report['executive_summary'])

    print("\n🎯 关键驱动因子排名:")
    for factor, score in report['key_drivers'].items():
        print(f"  {factor}: {score:.2f}")

    print(f"\n🔄 当前市场状态: {report['current_regime']}")

    print("\n⚠️ 主要风险:")
    print("上行风险（利空人民币）:")
    for risk in report['risk_assessment']['upside_risks_usd']:
        print(f"  • {risk}")

    print("\n下行风险（利多人民币）:")
    for risk in report['risk_assessment']['downside_risks_usd']:
        print(f"  • {risk}")

    print("\n📊 情景分析:")
    for name, scenario in report['forecast_scenarios'].items():
        name_display = name.replace('_scenario', '').replace('_', ' ').title()
        print(f"\n  {name_display} (概率: {scenario['probability']}%):")
        print(f"    目标区间: {scenario['usdcny_target']}")
        print(f"    时间框架: {scenario['timeframe']}")

    print("\n👁️ 监控优先级:")
    print("高优先级:")
    for item in report['monitoring_priority']['high_priority']:
        print(f"  • {item}")

    # 可视化
    print("\n📈 正在生成可视化图表...")
    analyzer.visualize_factor_analysis()

    print("\n" + "=" * 80)
    print("分析完成！建议结合实时数据更新分析。")
    print("=" * 80)


if __name__ == "__main__":
    main()