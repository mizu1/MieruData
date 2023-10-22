import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn import tree
from sklearn.model_selection import train_test_split
from pyecharts.charts import Bar,Line
from pyecharts import options as opts
from autogen.code_utils import (
    DEFAULT_MODEL,
    UNKNOWN,
    execute_code,
    extract_code,
    infer_lang,
)

# 决策树分类
def decision_tree_classifier(data,X_feature,Y_feature,n=0.3):
    X_train, X_test, y_train, y_test = train_test_split(data[X_feature], data[Y_feature], test_size=n, random_state=66)
    dtcf = DecisionTreeClassifier(criterion='entropy', 
                              splitter='best', 
                              random_state=66
                             )
    dtcf.fit(X_train, y_train)
    score = dtcf.score(X_test, y_test)

    return dtcf,score
# 决策树回归
def decision_tree_regressor(data,X_feature,Y_feature,n=0.3):
    X_train, X_test, y_train, y_test = train_test_split(data[X_feature], data[Y_feature], test_size=n, random_state=66)
    dtcf = DecisionTreeRegressor(criterion='friedman_mse', 
                              splitter='best', 
                              random_state=66
                             )
    dtcf.fit(X_train, y_train)
    score = dtcf.score(X_test, y_test)
    predicted_values = dtcf.predict(X_test)
    real_values = y_test
    return dtcf,score,real_values,predicted_values
# 绘制柱状图
def draw_bar(x_axis, title, y_label,y_value, subtitle):
    """
    Function draws a bar chart

    Input:
        x_axis (list): X-axis data
        y_label (str): Y-axis label
        y_value (list): Y-axis data
        title (str): Chart title
        subtitle (str): Chart subtitle

    Returns:
        The bar
    """
    c = (
            Bar()
                .add_xaxis(x_axis)
                .add_yaxis(y_label, y_value)
                .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle))
        )
    return c



# 绘制饼图

# 检查重复值
def check_duplicates(df, columns):
    """
    Function checks for duplicate rows in a dataframe

    Input:
        df: pandas DataFrame
        columns: list of columns to check for duplicates

    Returns:
        duplicate_rows: list of duplicate rows
    """

    duplicate_rows = df[df.duplicated(subset=columns)]
    return duplicate_rows

# 检查缺失值    
def check_missing(df, columns):
    """
    Function checks for missing values in a dataframe

    Input:
        df: pandas DataFrame
        columns: list of columns to check for missing values

    Returns:
        missing_values: list of missing values
    """

    missing_values = df[df.isnull().any(axis=1)]
    return missing_values

# 检查异常值
def check_outliers(df, columns):
    """
    Function checks for outliers in a dataframe

    Input:
        df: pandas DataFrame
        columns: list of columns to check for outliers

    Returns:
        outliers: list of outliers
    """

    outliers = []
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers.append(df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)].index)
    return outliers

# 绘制回归对比图
def draw_line_chart(real_values, predicted_values):
    line_chart = Line()
    #line_chart.add_xaxis(list(range(len(real_values))))
    line_chart.add_xaxis(real_values.index)
    real_values = real_values.to_numpy().astype(float).flatten()
    line_chart.add_yaxis("真实值", real_values)
    print(real_values)
    line_chart.add_yaxis("预测值", predicted_values)
    print(predicted_values)
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title="真实值与预测值对比图"))
    return line_chart

# 对话函数
def AIAgent(text,assistant,user_proxy,codeAnswer):
    if text == "自动代码执行":
        text = codeAnswer
    #assistant.reset_consecutive_auto_reply_counter(user_proxy)
    user_proxy.reset_consecutive_auto_reply_counter(assistant)
    #assistant.reply_at_receive[user_proxy] = True
    user_proxy.send(message=text,recipient=assistant,request_reply=True)
    lastmsg = user_proxy.last_message()
    # 提取代码块
    code = extract_code(lastmsg['content'])
    codeAnswer = ""
    # 它可能一次提供多个代码块，我们试出它的每个结果
    for Acode in code:
        if Acode[0] == "python":
            # 当代码类型是python时运行代码
            # logs_all是代码的执行结果
            logs_all = user_proxy.execute_code_blocks([Acode])
            # 把答案拼起来
            codeAnswer += logs_all[1] + "\n"
    return lastmsg['content'],codeAnswer