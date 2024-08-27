#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 10:15
# @Author  : Ken
# @Software: PyCharm
import streamlit as st
import json
from get_data import basic_info, daily_chips_and_winrate, fin_income, fin_balancesheet, fin_cashflow, \
    valuation_percentile, main_business, industry_rank, top10_holders, fina_audit


def main(df, ts_name, pro):
    if ts_name:
        left, right = st.columns([2, 8])
        with left:
            ts_code = df[df['name'] == ts_name]['ts_code'].values[0]
            tabs = ['基础信息', '筹码分布', '利润表', '资产负债表', '现金流量表', '估值分位', '主营业务', '行业排名',
                    '前十大股东', '审计意见']
            select_tab = st.radio('目录', tabs)
            df_basic = basic_info(pro, ts_code)
            json_basic = df_basic.to_json(orient="columns", force_ascii=False)
            json_basic = json.loads(json_basic)
            public_date = json_basic.get('ann_date').get('0')
        with right:
            if select_tab == '基础信息':
                # 一、个股基础信息
                co1, co2, co3, co4 = st.columns([1, 2, 1, 6])
                with co2:
                    st.write('**股票代码**')
                    st.write('**公司全称**')
                    st.write('**统一社会信用代码**')
                    st.write('**法人代表**')
                    st.write('**总经理**')
                    st.write('**董秘**')
                    st.write('**注册资本(万元)**')
                    st.write('**注册日期**')
                    st.write('**所在省份**')
                    st.write('**所在城市**')
                    st.write('**公司介绍**')
                    st.write('**公司主页**')
                    st.write('**电子邮件**')
                    st.write('**办公室**')
                    st.write('**公告日期**')
                    st.write('**经营范围**')
                    st.write('**员工人数**')
                    st.write('**主要业务及产品**')
                    st.write('**交易所代码**')
                with co4:
                    st.write(json_basic.get('股票代码').get('0'))
                    st.write(json_basic.get('公司全称').get('0'))
                    st.write(json_basic.get('统一社会信用代码').get('0'))
                    st.write(json_basic.get('法人代表').get('0'))
                    st.write(json_basic.get('总经理').get('0'))
                    st.write(json_basic.get('董秘').get('0'))
                    st.write(str(json_basic.get('注册资本(万元)').get('0')))
                    st.write(json_basic.get('注册日期').get('0'))
                    st.write(json_basic.get('所在省份').get('0'))
                    st.write(json_basic.get('所在城市').get('0'))
                    st.text(json_basic.get('公司介绍').get('0'))
                    st.write(json_basic.get('公司主页').get('0'))
                    st.text(json_basic.get('电子邮件').get('0'))
                    st.text(json_basic.get('办公室').get('0'))
                    st.write(json_basic.get('ann_date').get('0'))
                    st.text(json_basic.get('经营范围').get('0'))
                    st.write(str(json_basic.get('员工人数').get('0')))
                    st.text(json_basic.get('主要业务及产品').get('0'))
                    st.write(json_basic.get('交易所代码').get('0'))
            elif select_tab == '筹码分布':
                # 二、筹码分布
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 366
                    df_daily = daily_chips_and_winrate(pro, ts_code, data_len=data_len)
                    df_bar = df_daily[['交易日期', '胜率']]
                    df_bar = df_bar.set_index('交易日期')
                    df_line = df_daily.drop(['股票代码', '胜率'], axis=1)
                    df_line = df_line.set_index('交易日期')
                    st.line_chart(df_line)
                    st.bar_chart(df_bar)
                with r:
                    st.write('**智能分析：**')
            elif select_tab == '利润表':
                # 三、财务-利润表
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 8
                    df_income = fin_income(pro, ts_code, data_len)
                    cols = df_income.columns.tolist()
                    select_col = st.selectbox('科目：', cols[7:39])
                    plt_df = df_income[['报告期', select_col]]
                    plt_df = plt_df.set_index('报告期')
                    st.bar_chart(plt_df, use_container_width=True)
                with r:
                    st.write('**智能分析：**')
            elif select_tab == '资产负债表':
                # 四、财务-资产负债表
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 8
                    df_balance = fin_balancesheet(pro, ts_code, data_len)
                    cols = df_balance.columns.tolist()
                    select_col = st.selectbox('科目：', cols[7:48])
                    plt_df = df_balance[['报告期', select_col]]
                    plt_df = plt_df.set_index('报告期')
                    st.bar_chart(plt_df, use_container_width=True)
                with r:
                    st.write('**智能分析：**')

            elif select_tab == '现金流量表':
                # 五、财务-现金流量表
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 8
                    df_cash = fin_cashflow(pro, ts_code, data_len)
                    cols = df_cash.columns.tolist()
                    select_col = st.selectbox('科目：', cols[7:59])
                    plt_df = df_cash[['报告期', select_col]]
                    plt_df = plt_df.set_index('报告期')
                    st.bar_chart(plt_df, use_container_width=True)
                with r:
                    st.write('**智能分析：**')

            elif select_tab == '估值分位':
                # 六、估值分位
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 1024
                    df_pe, df_pb, df_ps, df_dv = valuation_percentile(pro, ts_code, data_len)
                    select_col = st.selectbox('科目：', ['市盈率', '市净率', '市销率', '股息率'])
                    if select_col == '市盈率':
                        df_pe = df_pe.drop(['ts_code'], axis=1)
                        df_pe = df_pe.set_index('trade_date')
                        st.line_chart(df_pe)
                    elif select_col == '市净率':
                        df_pb = df_pb.drop(['ts_code'], axis=1)
                        df_pb = df_pb.set_index('trade_date')
                        st.line_chart(df_pb)
                    elif select_col == '市销率':
                        df_ps = df_ps.drop(['ts_code'], axis=1)
                        df_ps = df_ps.set_index('trade_date')
                        st.line_chart(df_ps)
                    elif select_col == '股息率':
                        df_dv = df_dv.drop(['ts_code'], axis=1)
                        df_dv = df_dv.set_index('trade_date')
                        st.line_chart(df_dv)
                with r:
                    st.write('**智能分析：**')
            elif select_tab == '主营业务':
                # 七、主营业务
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 5
                    df_P, df_D = main_business(pro, ts_code, data_len)
                    select_col = st.selectbox('科目：', ['业务类型', '业务地区'])
                    if select_col == '业务类型':
                        pt_df = df_P.pivot_table(values='主营业务收入(元)', index='报告期', columns='主营业务来源',
                                                 aggfunc='sum')
                        st.bar_chart(pt_df)
                    else:
                        pt_df = df_D.pivot_table(values='主营业务收入(元)', index='报告期', columns='主营业务来源',
                                                 aggfunc='sum')
                        st.bar_chart(pt_df)
                with r:
                    st.write('**智能分析：**')
            elif select_tab == '行业排名':
                # 八、行业排名
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    df_rank = industry_rank(pro, ts_code)
                    cols = df_rank.columns.tolist()
                    select_col = st.selectbox('科目：', cols[3:])
                    plt_df = df_rank[['股票名称', select_col]]
                    plt_df = plt_df.set_index('股票名称')
                    st.bar_chart(plt_df, use_container_width=True)
                with r:
                    st.write('**智能分析：**')

            elif select_tab == '前十大股东':
                # 九、前十大股东+流动股东
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')

                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    df_top10_holders, df_top10_floatholders = top10_holders(pro, ts_code)
                    report_date = set(df_top10_holders['报告期'])
                    report_date.update(set(df_top10_floatholders['报告期']))
                    report_date = list(report_date)
                    select_col = st.selectbox('科目：', ['前十大股东', '前十大流动股东'])
                    st.write('报告期：' + report_date[0])

                    if select_col == '前十大股东':
                        df_top10_holders = df_top10_holders.drop(['TS股票代码', '公告日期', '报告期'], axis=1)
                        st.dataframe(df_top10_holders, hide_index=True)
                    else:
                        df_top10_floatholders = df_top10_floatholders.drop(['TS股票代码', '公告日期', '报告期'], axis=1)
                        st.dataframe(df_top10_floatholders, hide_index=True)
                with r:
                    st.write('**智能分析：**')
            elif select_tab == '审计意见':
                # 十、财务审计意见
                c1, c2, c3 = st.columns([3, 3, 4])
                with c1:
                    st.write('**股票代码: ' + ts_code + '**')
                with c2:
                    st.write('**公告日期: ' + public_date + '**')
                st.markdown("<p style='text-align: center; color: black;'> </p>", unsafe_allow_html=True)
                l, r = st.columns([7, 3])
                with l:
                    data_len = 6
                    st.dataframe(fina_audit(pro, ts_code, data_len), hide_index=True)
                with r:
                    st.write('**智能分析：**')
