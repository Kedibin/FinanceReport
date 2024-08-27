#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 20:07
# @Author  : 
# @Software: PyCharm
import tushare as ts
import streamlit as st
from stock_page import main as stock
import json

token = "d3d69e716b6b30f97a4e42b6863a69501ee049f807b6bfa89097636f"
pro = ts.pro_api(token)


def get_users():
    with open('users.json', 'r') as file:
        users = json.load(file)
    return users


@st.cache_data
def get_basic_data():
    base_df = pro.stock_basic(fields=["symbol", "name", "ts_code"])
    return base_df


def page_home():
    select = st.sidebar.radio('导航', ['首页', '股票', '行业', '宏观', '期货', '期权', '量化'])
    if select == '首页':
        st.markdown("<h1 style='text-align: center; color: red;'>财报</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: black;'>各大公司中报陆续发布，熊市末端，让我们一起挖呀挖呀挖！</p>",
            unsafe_allow_html=True)
        l, m, r = st.columns([1, 8, 1])
        with m:
            ts_name = st.selectbox('', ts_names, placeholder='🔍 选择或输入股票名称，一键生成公司财务分析报告',
                                   index=None,
                                   label_visibility='hidden')
        if st.session_state.stock == ts_name:
            pass
        elif ts_name in ts_names:
            st.session_state.page = 'page_stock' + ts_name
            st.session_state.stock = ts_name
            st.rerun()
        elif not ts_name:
            pass
        else:
            st.error('输入有误！')

    elif select == '股票':
        l, r = st.columns(2)
        with l:
            ts_name1 = st.selectbox('', ts_names, placeholder='🔍 选择或输入股票名称，一键生成公司财务分析报告',
                                    index=None,
                                    label_visibility='hidden')
        if ts_name1:
            st.session_state.stock = ts_name1
            stock(df, ts_name1, pro)
    else:
        st.subheader('敬请期待！')


def page_stock(a):
    select = st.sidebar.radio('导航', ['首页', '股票', '行业', '宏观', '期货', '期权', '量化'], index=1)
    if select == '首页':
        st.session_state.page = 'home'
        st.rerun()
    elif select == '股票':
        l, r = st.columns(2)
        with l:
            ts_name2 = st.selectbox('', ts_names, placeholder='🔍 选择或输入股票名称，一键生成公司财务分析报告',
                                    index=None,
                                    label_visibility='hidden')
        if not a or not ts_name2:
            pass
        elif ts_name2:
            st.session_state.stock = ts_name2
            stock(df, ts_name2, pro)
        else:
            stock(df, a, pro)
    else:
        st.subheader('敬请期待！')


def page_xx():
    st.title('当前是 xx 页面')


def page_login():
    c1, c2, c3 = st.columns(3)
    with c2:
        with st.form("login_form"):
            st.header("登录/注册")
            username = st.text_input("用户名", value="")
            password = st.text_input("密码", value="", type="password")
            submit = st.form_submit_button("登录/注册")
            if submit:
                if username not in user_info.keys():
                    st.success('新用户注册成功！')
                    # 更新会话状态为已登录
                    st.session_state.logged_in = True
                    st.session_state.user = '新用户 ' + username
                    # 保存用户
                    user_info[username] = password
                    file = open('users.json', "w", encoding='utf8')
                    json.dump(user_info, file, ensure_ascii=False)
                    file.close()
                    # 重新运行脚本以显示主页面
                    st.rerun()
                else:
                    if username in user_info.keys() and password == user_info.get(username):
                        st.success("登录成功！")
                        # 更新会话状态为已登录
                        st.session_state.logged_in = True
                        st.session_state.user = username
                        # 重新运行脚本以显示主页面
                        st.rerun()
                    else:
                        st.error("密码错误，请重新输入。")


# 设置页面配置
st.set_page_config(page_title='FR', layout='wide', page_icon=':coffee:')

df = get_basic_data()
ts_names = list(df['name'])

# 初始化 session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ''
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'stock' not in st.session_state:
    st.session_state.stock = ''

user_info = get_users()

if st.session_state.logged_in:
    st.sidebar.write('欢迎 ' + st.session_state.user)
    if st.session_state.page == 'home':
        page_home()
    elif 'page_stock' in st.session_state.page:
        page_stock(st.session_state.page.replace('page_stock', ''))
    elif st.session_state.page == 'page_xx':
        page_xx()
else:
    page_login()
