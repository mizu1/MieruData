import os
# 在这里填入你的代理，可以连接openai服务器的话请把下面两行删掉
os.environ["OPENAI_API_BASE"] = "http://example.com/v1"
os.environ["OPENAI_API_PREFIX"] = "http://example.com"
from flask import Flask,render_template,request,jsonify,session
from flask_session import Session 
from werkzeug.utils import secure_filename
from jinja2.utils import markupsafe
from algorithm import draw_bar,decision_tree_regressor,draw_line_chart,AIAgent
from pyecharts.charts import Bar,Line
import pandas as pd
from AutogenAngent import assistant,user_proxy
# 全局对象，避免实例化出不同的对象导致记忆丢失
Globalassistant = assistant
Globaluser_proxy = user_proxy
#
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'inputData')
app.config['SECRET_KEY'] = 'abc123'
app.config['SESSION_PERMANENT'] = False  # 设置会话的过期时间为浏览器关闭时  
app.config['SESSION_TYPE'] = 'filesystem'  # 会话存储类型，这里使用文件系统存储 

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def analyzer():
    session['codeAnswer'] = None
    return render_template('analyzer.html')
# 获取文件
@app.route('/get-filenames', methods=['GET'])
def get_filenames():
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'inputData')
    filenames = os.listdir(folder_path)
    return jsonify(filenames)
# 把选择的文件存在session中
@app.route('/read', methods=['POST'])  
def set_session():  
    path = request.form.get('path')

    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    full_path = os.path.normpath(full_path)
    response = full_path
    session['full_path'] = full_path
    return jsonify(response)


@app.route('/get-columns', methods=['GET'])
def get_columns():
    full_path = session['full_path']
    df = pd.read_csv(full_path)
    columns = df.columns.tolist()
    return jsonify(columns)


@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件在请求中
    if 'csvfile' not in request.files:
        return 'No file part'

    file = request.files['csvfile']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以要检查文件是否有名字
    if file.filename == '':
        return 'No selected file'

    # 保存文件
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return 'File uploaded successfully'

@app.route('/tree-regression', methods=['POST'])
def tree_regression():
    full_path = session['full_path']
    df = pd.read_csv(full_path)
    x_label = request.form.getlist('x_label[]')
    y_label = request.form.getlist('y_label[]')
    dtcf,score,real_values,predicted_values = decision_tree_regressor(df, x_label, y_label)
    print(f"real_values:{real_values}")
    line_chart = draw_line_chart(real_values, predicted_values)
    return render_template('analyzer.html',myechart=line_chart.dump_options())

### 这个是关键，关注这个就可以了
@app.route('/chat', methods=['POST'])
def chat():
    # 从请求中获取消息
    message = request.form.get('message')
    full_path = session['full_path']
    if "数据地址" not in message:
        message = f"{message} \n【数据地址:{full_path}】"

    if "自动代码执行" in message:
        message = "自动代码执行"

    if "图" in message or "可视化" in message:
        hack = "如果要绘制图像的话,请把图像保存在/static/img/createdImg/created.png。并且打印'图像已绘制'到控制台"
        message = f"{message} \n 【{hack}】"
    if session['codeAnswer'] != None:
        codeAnswer = str(session['codeAnswer'])
        response,codeAnswer =  AIAgent(text=message,assistant=assistant,user_proxy=Globaluser_proxy,codeAnswer=codeAnswer)
    else:
        response,codeAnswer =  AIAgent(text=message,assistant=assistant,user_proxy=Globaluser_proxy,codeAnswer="")
    session['codeAnswer'] = codeAnswer

    show_image = '图像已绘制' in response
    # 返回一个 JSON 响应
    return jsonify({'response': response, 'show_image': show_image})

if __name__ == '__main__':
    app.run()