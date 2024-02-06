import re  # 引入正则表达式对用户输入进行限制
import flask
import pymysql  # 连接数据库


# 初始化
app = flask.Flask(__name__)

# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='123qwe', database='pro_pro', charset='utf8')

# 操作数据库，获取db下的cursor对象
cursor = db.cursor()

# 存储登陆用户的名字用户其它网页的显示
users = []


# 网页初始页面 -> 登陆页面
@app.route("/", methods=["GET", "POST"])
def login():
    # 增加会话保护机制(未登陆前login的session值为空)
    flask.session['login'] = ''

    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        result_user = re.search(r"^[a-zA-Z]+$", user)  # 限制用户名为全字母
        result_pwd = re.search(r"^[a-zA-Z\d]+$", pwd)  # 限制密码为 字母和数字的组合
        
        # 检测账户和密码是否输入，如果输入 -> 登陆按钮被按下，执行登陆操作
        if result_user != None and result_pwd != None:  # 验证通过
            msg = '用户名或密码错误'
            # 判断账户和密码是否为管理员
            sql1 = "select * from admin where admin_id='" + \
                   user + "' and password='" + pwd + "';"
            cursor.execute(sql1)
            result_admin = cursor.fetchone()

            # 判断账户和密码是否为用户
            sql2 = "select * from user where user_id='" + \
                   user + "' and password='" + pwd + "';"
            cursor.execute(sql2)
            reseult_user = cursor.fetchone()

            # 验证得到密码后，进入界面跳转页面
            if result_admin or reseult_user:
                # 登陆成功
                flask.session['login'] = 'OK'
                users.append(user)  # 存储登陆成功的用户名用于显示
                if result_admin:
                    return flask.redirect(flask.url_for('admin')) # admin
                elif result_user:
                    return flask.redirect(flask.url_for('user'))    # user
                # return flask.redirect('/file')
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
        user = ''
    return flask.render_template('login.html', msg=msg, user=users)


# 用户注册页面
@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        pwd_confirm = flask.request.values.get("pwd_confirm", "")
        if pwd == pwd_confirm:
            result_user = re.search(r"^[a-zA-Z]+$", user)  # 限制用户名为全字母
            result_pwd = re.search(r"^[a-zA-Z\d]+$", pwd)  # 限制密码为 字母和数字的组合
            
            # 检测账户和密码是否输入，如果输入 -> 确认按钮被按下，执行注册操作
            if result_user != None and result_pwd != None:  # 验证通过
                msg = ''
                
                # 判断输入的账户名是否为已经为用户
                sql1 = "select * from user where user_id='" + \
                    user + "' ;"
                cursor.execute(sql1)
                reseult_duplicated = cursor.fetchone()
                print(reseult_duplicated)

                # 确认用户名已存在
                if  reseult_duplicated:
                    msg = "用户名已存在"
                # 确认用户名不存在
                else:   # 执行注册
                    sql2 = "INSERT INTO `user` VALUES('" + \
                    user + "', '" + pwd + "');"
                    print(sql2)
                    cursor.execute(sql2)
                    db.commit() # 执行语句
                    msg = '注册成功'
            else:  # 输入验证不通过
                msg = '用户名或密码格式错误'
        else:
            msg = '两次输入的密码不相同'
    else:
        msg = ''

    return flask.render_template('register.html', msg=msg)


# 用户登陆后页面
@app.route('/user', methods=["GET", "POST"])
def user():
    if flask.session.get("login", "") == '':
        return flask.redirect('/')
    
    insert_result = ''
    if users:
        for user in users:
            user_info = user
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        student_name = flask.request.values.get("student_name", "")
        student_sex = flask.request.values.get("student_sex", "")
        student_age = flask.request.values.get("student_age", "")
        student_class = flask.request.values.get("student_class", "")
        student_go = flask.request.values.get("student_go", "")

        # 检查输入是否为空
        if not all([student_name, student_sex, student_age, student_class, student_go]):
            insert_result = "输入的学生信息不能为空"
        else:
            try:
                # 信息存入数据库
                sql_1 = f"insert into `user_info` values('{user_info}', '{student_name}', '{student_sex}', {student_age}, '{student_class}', '{student_go}')"
                print(sql_1)
                cursor.execute(sql_1)
                insert_result = "学生信息上传成功"
                db.commit()
            except Exception as err:
                # 信息存入数据库
                insert_result = "学生信息已上传"

    return flask.render_template('user.html', insert_result=insert_result, user_info=user_info)


# 管理员登陆后页面 -> 主页面 -> 档案信息录入
@app.route('/admin', methods=["GET", "POST"])
def admin():
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        return flask.redirect('/')
    
    insert_result = ''
    results = ''
    if users:
        for user in users:
            user_info = user
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        student_id = flask.request.values.get("student_id", "")
        student_name = flask.request.values.get("student_name", "")
        student_sex = flask.request.values.get("student_sex", "")
        student_age = flask.request.values.get("student_year", "")
        student_class = flask.request.values.get("student_class", "")
        student_go = flask.request.values.get("student_go", "")

        # 检查输入是否为空
        if not all([student_id, student_name, student_sex, student_age, student_class, student_go]):
            insert_result = "输入的学生信息不能为空"
        else:
            try:
                # 信息存入数据库
                sql_1 = f"insert into `user_info` values('{student_id}', '{student_name}', '{student_sex}', {student_age}, '{student_class}', '{student_go}')"
                print(sql_1)
                cursor.execute(sql_1)
                insert_result = "学生信息上传成功"
                db.commit()
            except Exception as err:
                # 信息存入数据库
                insert_result = "学生信息已上传"

    # 显示所有数据
    sql_list = "select * from user_info"
    cursor.execute(sql_list)
    results = cursor.fetchall()
    print(results)

    return flask.render_template('admin.html', insert_result=insert_result, user_info=user_info, results=results)


# 管理员登陆后页面 -> 更改学生信息
@app.route('/update_info', methods=["GET", "POST"])
def update_info():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        return flask.redirect('/')
    
    user_info = ''
    if users:
        for user in users:
            user_info = user
    insert_result = ''

    if flask.request.method == 'POST':
        # 获取输入的学生信息
        student_id = flask.request.values.get("student_id", "")
        student_name = flask.request.values.get("student_name", "")
        student_sex = flask.request.values.get("student_sex", "")
        student_age = flask.request.values.get("student_age", "")
        student_class = flask.request.values.get("student_class", "")
        student_go = flask.request.values.get("student_go", "")

        if student_id != None:  # 验证通过
            # 获取下拉框的数据
            select = flask.request.form.get('selected_one')
            print("select")
            
            if select == '修改姓名':
                try:
                    sql = "update user_info set `姓名`=%s where user_id=%s;"
                    cursor.execute(sql, (student_name, student_id))
                    insert_result = student_id + "的姓名修改成功!"
                    db.commit()
                except Exception as err:
                    print(err)
                    insert_result = "修改姓名失败!"
                    pass

            if select == '修改性别':
                try:
                    sql = "update user_info set `性别`=%s where user_id=%s;"
                    cursor.execute(sql, (student_sex, student_id))
                    insert_result = student_id + "的性别修改成功!"
                    db.commit()
                except Exception as err:
                    print(err)
                    insert_result = "修改性别失败!"
                    pass
                
            if select == '修改年龄':
                try:
                    sql = "update user_info set `年龄`=%s where user_id=%s;"
                    cursor.execute(sql, (student_age, student_id))
                    insert_result = student_id + "的年龄修改成功!"
                    db.commit()
                except Exception as err:
                    print(err)
                    insert_result = "修改年龄失败!"
                    pass
                
            if select == '修改所属班级':
                try:
                    sql = "update user_info set `所属班级`=%s where user_id=%s;"
                    cursor.execute(sql, (student_class, student_id))
                    insert_result = student_id + "的所属班级修改成功!"
                    db.commit()
                except Exception as err:
                    print(err)
                    insert_result = "修改所属班级失败!"
                    pass
                
            if select == '修改毕业去向':
                try:
                    sql = "update user_info set `毕业去向`=%s where user_id=%s;"
                    cursor.execute(sql, (student_go, student_id))
                    insert_result = student_id + "的毕业去向修改成功!"
                    db.commit()
                except Exception as err:
                    print(err)
                    insert_result = "修改毕业去向失败!"
                    pass

            if select == '修改全部信息':
                try:
                    sql = "update user_info set `姓名`=%s where user_id=%s;"
                    cursor.execute(sql, (student_name, student_id))
                    sql = "update user_info set `性别`=%s where user_id=%s;"
                    cursor.execute(sql, (student_sex, student_id))
                    sql = "update user_info set `年龄`=%s where user_id=%s;"
                    cursor.execute(sql, (student_age, student_id))
                    sql = "update user_info set `所属班级`=%s where user_id=%s;"
                    cursor.execute(sql, (student_class, student_id))
                    sql = "update user_info set `毕业去向`=%s where user_id=%s;"
                    cursor.execute(sql, (student_go, student_id))
                    insert_result = student_id + "的全部信息修改成功!"
                    db.commit()
                except Exception as err:
                    print(err)
                    insert_result = "修改全部信息失败!"
                    pass
                
        else:  # 输入验证不通过
            insert_result = "用户名输入格式不符合要求!"

    # 显示所有数据
    sql_list = "select * from user_info"
    cursor.execute(sql_list)
    results = cursor.fetchall()
    print(results)

    return flask.render_template('update_info.html', insert_result=insert_result, results=results, user_info=user_info)
                              


# 管理员登陆后页面 -> 查询用户信息
@app.route("/search", methods=["GET", "POST"])
def search():
    if flask.session.get("login", "") == '':
    # 用户没有登陆
        return flask.redirect('/')
    
    user_info = ''
    if users:
        for user in users:
            user_info = user
    result = ''
    if flask.request.method == 'POST':
        selected = flask.request.values.get("selected", "")
        info = flask.request.values.get("info", "")
        print(selected)
        print(info)
        if (selected == "姓名查询"):
            sql = f"SELECT * FROM `user_info` WHERE `姓名` = '{info}';"
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
        if (selected == "用户名查询"):
            sql = f"SELECT * FROM `user_info` WHERE `user_id` = '{info}';"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    return flask.render_template('search.html',results = result)


# 管理员登陆后页面 -> 更改用户信息
@app.route('/user_change', methods=["GET", "POST"])
def user_change():
    if flask.session.get("login", "") == '':
    # 用户没有登陆
        return flask.redirect('/')

    user_info = ''
    if users:
        for user in users:
            user_info = user
    insert_result = ''
    if flask.request.method == 'POST':
        admin_name = flask.request.values.get("admin_name", "")
        admin_password = flask.request.values.get("admin_password", "")
        selected_one = flask.request.values.get("selected_one", "")
        print(selected_one)
        result_user = re.search(r"^[a-zA-Z]+$", admin_name)  # 限制用户名为全字母
        result_pwd = re.search(r"^[a-zA-Z\d]+$", admin_password)  # 限制密码为 字母和数字的组合
        if result_user != None and result_pwd != None:  # 验证通过
            if(selected_one == "修改用户密码"):
                sql = f"SELECT * FROM `user` WHERE `user_id` = '{admin_name}';"
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    sql =f"UPDATE `user` SET `password` = '{admin_password}' WHERE `user_id` = '{admin_name}';"
                    cursor.execute(sql)
                    print(sql)
                    db.commit()
                    insert_result = "密码修改完成"
                else:
                    insert_result = "没有该用户，密码修改失败"
                
            if(selected_one == "删除用户"):
                sql = f"SELECT * FROM `user` WHERE `user_id` = '{admin_name}' AND `password` = '{admin_password}';"
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)

                if result:
                    sql = f"DELETE FROM `user` WHERE `user_id` = '{admin_name}' AND `password` = '{admin_password}';"
                    cursor.execute(sql)
                    print(sql)
                    db.commit()
                    insert_result = "用户删除成功"
                else:
                    insert_result = "用户名或密码错误，删除失败"

            if(selected_one == "增加用户"):
                sql = f"SELECT * FROM `user` WHERE `user_id` = '{admin_name}';"
                cursor.execute(sql)
                result = cursor.fetchone()
                if not result:
                    sql = f"INSERT INTO `user` VALUES('{admin_name}','{admin_password}');"
                    cursor.execute(sql)
                    print(sql)
                    db.commit()
                    insert_result = "用户添加成功"
                else:
                    insert_result = "用户已存在，添加失败"

    # POST方法时显示数据
    sql_list = "select * from user"
    cursor.execute(sql_list)
    results = cursor.fetchall()
    print(results)
    return flask.render_template('user_change.html', insert_result=insert_result,results=results,user_info=user_info)


# 管理员登陆后页面 -> 更改管理员信息
@app.route('/admin_change', methods=["GET", "POST"])
def admin_change():
    if flask.session.get("login", "") == '':
    # 用户没有登陆
        return flask.redirect('/')
    
    user_info = ''
    if users:
        for user in users:
            user_info = user
    insert_result = ''
    if flask.request.method == 'POST':
        admin_name = flask.request.values.get("admin_name", "")
        admin_password = flask.request.values.get("admin_password", "")
        selected_one = flask.request.values.get("selected_one", "")
        print(selected_one)
        result_user = re.search(r"^[a-zA-Z]+$", admin_name)  # 限制用户名为全字母
        result_pwd = re.search(r"^[a-zA-Z\d]+$", admin_password)  # 限制密码为 字母和数字的组合
        if result_user != None and result_pwd != None:  # 验证通过
            if(selected_one == "修改管理员密码"):
                sql = f"SELECT * FROM `admin` WHERE `admin_id` = '{admin_name}';"
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                if result:
                    sql =f"UPDATE `admin` SET `password` = '{admin_password}' WHERE `admin_id` = '{admin_name}';"
                    cursor.execute(sql)
                    print(sql)
                    db.commit()
                    insert_result = "密码修改完成"
                else:
                    insert_result = "没有该管理员，密码修改失败"
                
            if(selected_one == "删除管理员"):
                sql = f"SELECT * FROM `admin` WHERE `admin_id` = '{admin_name}' AND `password` = '{admin_password}';"
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)

                if result:
                    sql = f"DELETE FROM `admin` WHERE `admin_id` = '{admin_name}' AND `password` = '{admin_password}';"
                    cursor.execute(sql)
                    print(sql)
                    db.commit()
                    insert_result = "管理员删除成功"
                else:
                    insert_result = "管理员名或密码错误，删除失败"

            if(selected_one == "增加管理员"):
                sql = f"SELECT * FROM `admin` WHERE `admin_id` = '{admin_name}';"
                cursor.execute(sql)
                result = cursor.fetchone()
                if not result:
                    sql = f"INSERT INTO `admin` VALUES('{admin_name}','{admin_password}');"
                    cursor.execute(sql)
                    print(sql)
                    db.commit()
                    insert_result = "管理员添加成功"
                else:
                    insert_result = "管理员已存在，添加失败"

    sql_list = "select * from admin"
    cursor.execute(sql_list)
    results = cursor.fetchall()

    return flask.render_template('admin_change.html', insert_result=insert_result,results=results, user_info=user_info)               


# 启动服务器
app.debug = True

# 增加session会话保护(任意字符串,用来对session进行加密)
app.secret_key = 'carson'
try:
    app.run()
except Exception as err:
    print(err)
    db.close()  # 关闭数据库连接
