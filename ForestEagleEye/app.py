from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, abort, jsonify
import pymysql
import hashlib
import sqlalchemy
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy import insert
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Column, Enum, Integer, Table, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from flask import render_template  # 引入模板插件
from sqlalchemy.testing import db
from flask_mail import Mail, Message
import random
from datetime import timedelta
import os
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError,OperationalError
import re
import pandas as pd


app = Flask(__name__,
static_folder='./public/static',  #设置静态文件夹目录
template_folder = "./public/templates")  #设置vue编译输出目录dist文件夹，为Flask模板文件目录
app.secret_key = "123456789"

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAIL_SERVER"] = "smtp.qq.com"  # 邮件服务器
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "3327903803@qq.com"  # 邮箱
app.config["MAIL_PASSWORD"] = "xyjtyyhunuurdadj"  # 邮箱授权码
app.config["MAIL_DEFAULT_SENDER"] = "3327903803@qq.com"  # 邮箱
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

mail = Mail(app)
verification_codes = {}  # 存储邮箱和验证码的字典

# MySQL 数据库连接配置
db_config={
    'user':'root',
    'password':'20040616',#这里改成自己的数据库密码
    'host':'localhost',
    'port':3306,
    'database': 'forest',#这里改成自己的数据库名字
    'charset':'utf8mb4'}
# 创建数据库连接
engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(**db_config))

Base = declarative_base()


class user_participate_activity(Base):
    __tablename__ = "user_participate_activity"
    upa_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 唯一标识
    participateNumber = Column(Integer, nullable=False)  # 此次报名活动人数
    note = Column(String(100), default="")  # 备注
    user_id = Column(Integer, ForeignKey("users.u_id"))
    activity_id = Column(Integer, ForeignKey("activities.a_id"))


# 用户表
class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 唯一标识
    u_name = Column(String(10), nullable=False, unique=True)  # 用户昵称
    u_telphone = Column(String(15), unique=True)  # 联系电话
    u_password = Column(String(100), nullable=False)  # 用户密码
    u_email = Column(String(50), nullable=False, unique=True)  # 邮箱
    u_role = Column(Enum("普通用户", "林业从业人员", "林业管理人员", "林业监管人员"), nullable=False, default="普通用户")  # 用户所属角色（普通用户、林业从业人员、林业管理人员、环境管理人员、林业局监管人员）
    u_forest = Column(String(100))  # 所属森林（林业管理人员、环境管理人员、林业局监管人员需要选择）
    u_avatarPath = Column(String(100), nullable=False, default="src/assets/default-avatar.png")  # 头像图片路径
    u_signature = Column(String(100), default="这个人很懒，什么都没有留下...")  # 个性签名
    u_signupTime = Column(DateTime, nullable=False, default=datetime.now)  # 注册时间
    u_newestTime = Column(DateTime, nullable=False, onupdate=datetime.now, default=datetime.now)  # 最近登录时间
    u_institution = Column(Integer,ForeignKey("institutions.i_id"),nullable=True)    # 用户所属机构（除普通用户外需选择）

    # u_submitTips = relationship()  # 提交的建议与举报
    # u_approveTips = relationship()  # 审批的建议与举报
    # u_post = relationship()  # 发布的帖子
    # u_comments = relationship()  # 评论
    # u_likes = relationship()  # 点赞的帖子
    # u_question = relationship()  # 存小林问答问过的问题及回答


# 活动表
class Activity(Base):
    __tablename__ = "activities"
    a_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 活动编号
    a_applicantId = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 申请人id
    a_submitTime = Column(DateTime, nullable=False, default=datetime.now)  # 申请提交时间
    a_attachment = Column(String(100), default="")  # 申请附件
    a_name = Column(String(100), nullable=False)  # 活动名称
    a_type = Column(Enum("伐木", "采摘", "旅游参观", "野营", "捕猎","冥想","徒步"), nullable=False)  # 活动类型
    a_forest = Column(String(100), nullable=False)  # 审批单位（森林名称）
    a_location = Column(String(100), nullable=False)  # 活动地点（具体地点）
    a_beginTime = Column(DateTime, nullable=False)  # 活动开始时间
    a_endTime = Column(DateTime, nullable=False)  # 活动结束时间
    a_introduction = Column(String(1000), nullable=False)  # 活动简介
    a_picPath = Column(String(100), default="")  # 活动图片路径
    a_ableParticipate = Column(Boolean, nullable=False)  # 活动是否面向大众（大众可以报名参加）
    a_participantNumber = Column(Integer, nullable=False)  # 活动人数
    a_enrolledNumber = Column(Integer, nullable=False, default=0)  # 已报名人数
    a_state = Column(Enum("approving", "approved", "dismissed", "ongoing", "ended"), nullable=False, default="approving")  # 状态（待审批、通过、驳回、活动开始、活动完成）
    a_approver_id = Column(Integer, ForeignKey("users.u_id"), nullable=True)  # 审批人id
    a_approveTime = Column(DateTime, nullable=True)  # 活动审批时间
    a_dismissreason = Column(String(100), nullable=True)  # 驳回理由

### 机构相关表
# 管理机构
class Institution(Base):
    __tablename__ = "institutions"
    i_id = Column(Integer,primary_key=True,nullable=False,unique=True)  # 机构编号
    i_name = Column(String(20),nullable=False,unique=True)   # 机构名称
    i_type = Column(Enum('从业机构','管理机构'),nullable=False)   # 机构类别


### 森林相关表
# 所有森林常量表
class Forest(Base):
    __tablename__ = "forests"
    f_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 森林编号
    f_name = Column(String(100), nullable=False, unique=True)  # 森林名称
    f_location = Column(String(100), nullable=False,default='中国大陆')  # 森林地理位置
    f_area = Column(Integer, nullable=False,default=0)  # 森林占地面积
    f_soilType = Column(String(100), nullable=False,default='暂无')  # 土壤类型
    f_intro = Column(String(1000),default="森林管理员尚未添加简介...")  # 森林简介
    f_manager = Column(Integer,ForeignKey('institutions.i_id')) # 森林管理机构id


# 森林变量表
# 定义基础表模型
class ForestVariableBase(Base):
    __abstract__ = True  # 抽象基类
    f_id = Column(Integer, primary_key=True, autoincrement=True)  # 主键，自增
    f_date = Column(DateTime, nullable=False, default=datetime.now)  # 日期，默认当前时间
    f_temperature = Column(Float)  # 温度
    f_humidity = Column(Float)  # 湿度
    f_precipitation = Column(Float)  # 降水量
    f_resourceDistribution = Column(String(1000))  # 资源分布
    f_vegetationCoverage = Column(String(1000))  # 植被覆盖
    f_historicalCulture = Column(String(1000))  # 历史文化
    f_hydrologicalFeatures = Column(String(1000))  # 水文特征
    f_disasterSituation = Column(String(1000))  # 灾害情况
    f_wildlife = Column(String(1000))  # 野生动物
    f_economicValue = Column(String(1000))  # 经济价值


"""
    思想：以上创建了每个森林变量表的基类，每个森林所有时刻的变量存在一张表内，不同森林的变量存在不同表内，使用以下方法创建、访问、插入。
    # 动态创建表函数
    def create_forest_variable_table(forest_name):
        class ForestVariable(ForestVariableBase):
            __tablename__ = f'forest_variable_{forest_name}'
        
        ForestVariable.__table__.create(bind=engine)
        return ForestVariable

    # 获取动态创建的表函数
    def get_forest_variable_table(forest_name):
        class ForestVariable(ForestVariableBase):
            __tablename__ = f'forest_variable_{forest_name}'
        
        return ForestVariable

    # 创建一个新的森林变量表
    forest_name = 'example_forest'
    ForestVariable = create_forest_variable_table(forest_name)

    # 插入数据
    new_record = ForestVariable(temperature=25.5, humidity=60.0)
    db_session.add(new_record)
    db_session.commit()

    # 访问动态创建的表
    ForestVariable = get_forest_variable_table(forest_name)

    # 查询数据
    records = db_session.query(ForestVariable).all()
    for record in records:
        print(record.temperature, record.humidity)
"""

# 这是删除所有数据的操作，不到万不得已千万不要做
# 如果之前创建过同名数据库且不明白如何数据库迁移，可以把下面一句注释去掉，运行清除之前的表并创建新表，然后记得加上注释
#Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)

db_session_class = sessionmaker(bind=engine)
db_session = db_session_class()

# 以下是为了测试临时添加的森林、管理机构和从业机构
# 完整功能上线后，需删除！
'''
administrator=Institution(i_name="管理机构-测试",i_type='管理机构')
db_session.add(administrator)
db_session.commit()

practitioner=Institution(i_name='从业机构-测试',i_type='从业机构')
db_session.add(practitioner)
db_session.commit()

forest = Forest(f_name='测试森林',f_manager=administrator.i_id)
db_session.add(forest)
db_session.commit()
'''
# 完整功能上线后，以上需删除！

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def generate_verification_code():
    return str(random.randint(100000, 999999))


@app.route("/send_verification_code", methods=["POST"])
def send_verification_code():
    email = request.form["email"]
    code = generate_verification_code()
    verification_codes[email] = code
    msg = Message("欢迎来到林上鹰眼", recipients=[email])
    msg.body = f"您的验证码为 {code}"
    try:
        mail.send(msg)
        return jsonify({"status": "success", "message": "验证码已发送到您的邮箱"})
    except Exception as e:
        return jsonify({"status": "fail", "message": "发送邮件失败，请检查邮箱输入是否有误"})


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = hash_password(request.form["password"])
        code = request.form["code"]
        if email not in verification_codes or verification_codes[email] != code:
            error = "验证码错误"
            return jsonify({"status": "fail", "message": error})
        existing_user = db_session.query(User).filter_by(u_name=username).first()
        if existing_user:
            error = "用户名已存在"
            return jsonify({"status": "fail", "message": error})
        existing_email = db_session.query(User).filter_by(u_email=email).first()
        if existing_email:
            error = "该邮箱已被注册"
            return jsonify({"status": "fail", "message": error})

        # 错误排除后创建新用户
        user = User(u_name=username, u_password=password, u_email=email)
        user.u_role=request.form['role']
        if user.u_role!='普通用户':
            user.u_forest=request.form['forest']
            user.u_institution=request.form['inst']
        db_session.add(user)
        db_session.commit()

        success = "注册成功，请登录"
        return jsonify({
                'status': 'success', 
                'message': success,
            })
    else:
        error = "请求错误"
        return jsonify({"status": "fail", "message": error})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = hash_password(request.form["password"])
        user = db_session.query(User).filter_by(u_email=email, u_password=password).first()
        if user:
            user.u_newestTime = datetime.now()  # 最新登录时间设置为当前时间
            days = (user.u_newestTime - user.u_signupTime).days + 1
            db_session.commit()  # 提交更改到数据库
            
            # 在森林表和机构表中查询forest和inst的名称+编号
            forest=db_session.query(Forest).filter_by(f_id=user.u_forest).first()
            inst=db_session.query(Institution).filter_by(i_id=user.u_institution).first()
            
            success = "欢迎来到林上鹰眼！"
            data={                'status': 'success', 
                'message': success,

                'days': days,
                'avatar':user.u_avatarPath,
                'user_id':user.u_id,
                'newestTime':user.u_newestTime.strftime('%Y-%m-%d %H:%M:%S'),
                'signupTime':user.u_signupTime.strftime('%Y-%m-%d'),
                'role':user.u_role,
                'username':user.u_name,
                'email':user.u_email,
                'signature':user.u_signature
                }
            if user.u_role!='普通用户':
                data['forest']=f"{forest.f_name}(FO{forest.f_id})"
                data['inst']=f"{inst.i_name}(INST{inst.i_id})"
            return jsonify(data)
        else:
            error = "登录失败，邮箱或密码错误"
            return jsonify({"status": "fail", "message": error})
    else:
        error = "请求错误"
        return jsonify({"status": "fail", "message": error})


# 注销
@app.route("/logoff", methods=["GET", "POST"])
def logoff():
    session.clear()
    flash("您已成功注销", "success")
    return redirect(url_for("login"))


# 退出登录
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return jsonify({"status": "success"})


# 用户信息修改
@app.route("/setUserInfo", methods=["POST"])
def setUserInfo():
    target = request.form["target"]
    data = request.form["data"]
    user = db_session.query(User).filter_by(u_id=request.form["user_id"]).first()
    if target == "signature":
        user.u_signature = data
        db_session.commit()
        return jsonify({"status": "success", "message": "用户个性签名修改成功！"})
    elif target == "username":
        user.u_name = data
        db_session.commit()
        return jsonify({"status": "success", "message": "用户昵称修改成功！"})
    return jsonify({"status": "fail", "message": "修改失败！"}), 401

# 获取全部森林
@app.route("/get_all_forests",methods=["GET"])
def getAllForests():
    # 获取所有管理机构的名称和 ID
    institutions = {inst.i_id: inst.i_name for inst in db_session.query(Institution).filter_by(i_type='管理机构').all()}

    forests=[{
        'value': forest.f_id, 
        "label": forest.f_name, 
        "location": forest.f_location, 
        "area": forest.f_area, 
        "manager" : institutions.get(forest.f_manager)  # 使用森林的管理机构 ID 从字典中获取名称
    } for forest in db_session.query(Forest).all()]

    if forests:
        return jsonify({'forests':forests})
    return 401

# 获取对应森林的机构（用于非普通用户角色的注册）
@app.route("/get_relative_inst",methods=['POST'])
def getRelativeInstitutions():
    if request.form['role'] == '林业从业人员':
        inst_type='从业机构'
    else:
        inst_type='管理机构'
    try:
        insts = [{'value': inst.i_id, 'label': inst.i_name} for inst in db_session.query(Institution).filter_by(i_type=inst_type)]
        db_session.commit()
        if insts:
            return jsonify({'insts': insts})
        else:
            return jsonify({'error': 'No institutions found for the given criteria.'}), 404
    except Exception as e:
        return jsonify({'error': f'An error occurred while querying the database: {str(e)}'}), 500



# 林业活动界面
@app.route("/activity")
def activity():
    print(session)
    username = session.get("username")  # 从会话中获取用户名
    if not username:
        return redirect(url_for("login"))  # 如果没有用户名信息，重定向到登录页面

    # 根据用户名查询用户角色
    user = db_session.query(User).filter_by(u_name=username).first()
    if user:
        u_role = user.u_role
    else:
        flash("用户不存在或已被删除", "error")
        return redirect(url_for("login"))
    # 传递当前用户角色给前端，根据不同角色显示不同的按钮
    return render_template("activity.html", u_role=u_role)


# 我的申请界面，显示当前用户已申请的活动
@app.route("/apply")
def apply():
    if "username" in session:
        # 获取当前用户的申请中或已通过的活动
        username = session.get("username")  # 从会话中获取用户名
        user = db_session.query(User).filter_by(u_name=username).first()
        if user:
            u_id = user.u_id
        approving_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id, Activity.a_state == "approving").all()
        approved_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id, Activity.a_state == "approved").all()
        dismissed_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id, Activity.a_state == "dismissed").all()

        return render_template("apply.html", approving_activities=approving_activities, approved_activities=approved_activities, dismissed_activities=dismissed_activities)
    return redirect(url_for("index"))


# 创建活动
@app.route("/create_activity", methods=["GET", "POST"])
def create_activity():

    if request.method == "POST":
        # 从表单中获取数据
        a_name = request.form["a_name"]
        a_location = request.form["a_location"]
        a_beginTime = request.form["a_beginTime"]
        a_endTime = request.form["a_endTime"]
        a_participantNumber = request.form["a_participantNumber"]
        a_introduction = request.form["a_introduction"]
        a_forest = request.form["a_forest"]
        a_type = request.form["a_type"]
        a_ableParticipate = request.form.get("a_ableParticipate") is not None

        # 处理文件上传
        a_picPath = request.files["a_picPath"]
        if a_picPath:
            filename = secure_filename(a_picPath.filename)
            a_picPath.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # 根据用户名查询用户
        username = session.get("username")  # 从会话中获取用户名
        user = db_session.query(User).filter_by(u_name=username).first()
        if user:
            u_id = user.u_id
        # 创建新的 Activity 实例
        new_activity = Activity(
            a_applicantId=u_id,
            a_name=a_name,
            a_location=a_location,
            a_beginTime=datetime.strptime(a_beginTime, "%Y-%m-%dT%H:%M"),
            a_endTime=datetime.strptime(a_endTime, "%Y-%m-%dT%H:%M"),
            a_participantNumber=int(a_participantNumber),
            a_introduction=a_introduction,
            a_picPath=filename,
            a_ableParticipate=a_ableParticipate,
            a_type=a_type,
            a_forest=a_forest,
            a_state="approving",  # 默认状态为待审批
        )

        # 将新活动添加到数据库会话并提交
        db_session.add(new_activity)
        db_session.commit()

        flash("活动创建成功，等待审批", "success")
        return redirect(url_for("activity"))

    return render_template("create_activity.html")


# 活动详情页，申请人和审批人公用界面，但是会传递一个is_approver参数决定前端是否显示“同意”“驳回”
@app.route("/activity_detail/<int:activity_id>")
def activity_detail(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if not activity:
        flash("活动不存在", "error")
        return redirect(url_for("activity"))

    username = session.get("username")  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    current_user_role = user.u_role
    # 判断当前用户是否为审批人
    is_approver = current_user_role == "林业管理人员"
    return render_template("activity_detail.html", activity=activity, is_approver=is_approver)


# 申请人删除所申请的活动
@app.route("/delete_activity/<int:activity_id>", methods=["POST"])
def delete_activity(activity_id):

    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if activity:
        db_session.delete(activity)
        db_session.commit()
        flash("活动删除成功", "success")
    else:
        flash("活动不存在或已被删除", "error")

    return redirect(url_for("apply"))


# 我的审批界面
@app.route("/approve")
def approve():
    # 假设当前管理员的森林名称存储在session中
    username = session.get("username")  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    current_forest = user.u_forest

    if not current_forest:
        flash("您尚未登录或没有权限访问此页面", "error")
        return redirect(url_for("login"))

    # 根据当前管理员的森林名称和状态查询活动
    approving_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest, Activity.a_state == "approving").all()
    approved_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest, Activity.a_state == "approved").all()
    dismissed_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest, Activity.a_state == "dismissed").all()

    # 渲染模板并传递活动列表,传递用户的角色是因为在活动详情页时如果为审批人会添加审批通过或驳回按钮
    return render_template("approve.html", approving_activities=approving_activities, approved_activities=approved_activities, dismissed_activities=dismissed_activities)


# 审批通过
@app.route("/approve_activity/<int:activity_id>", methods=["POST"])
def approve_activity(activity_id):
    # 审批活动逻辑
    # 更新活动状态为 'approved'
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    # 获取当前审批人的id
    username = session.get("username")  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    # 修改状态
    activity.a_state = "approved"
    # 存储审批人的id
    activity.a_approver_id = user.u_id
    # 存储审批时间
    activity.a_approveTime = datetime.now()

    return redirect(url_for("approve"))


# 审批驳回
@app.route("/dismiss_activity/<int:activity_id>", methods=["POST"])
def dismiss_activity(activity_id):
    dismiss_reason = request.form.get("dismiss_reason", "")
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    # 获取当前审批人的id
    username = session.get("username")  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    # 修改状态
    activity.a_state = "dismissed"
    # 存储审批人的id
    activity.a_approver_id = user.u_id
    # 存储审批时间
    activity.a_approveTime = datetime.now()
    # 存储驳回理由
    activity.a_dismissreason = dismiss_reason
    return redirect(url_for("approve"))


# 活动风采界面
@app.route("/activities")
def activities():
    # 筛选面向大众且截止时间晚于当前时间且审批通过的活动
    # 获取当前时间
    now = datetime.now()
    activities = db_session.query(Activity).filter(Activity.a_ableParticipate == True, Activity.a_endTime > now, Activity.a_state == "approved").all()
    return render_template("activities.html", activities=activities)


# 报名活动界面
@app.route("/activity_enroll/<int:activity_id>", methods=["GET"])
def activity_enroll(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if activity:
        return render_template("activity_enroll.html", activity=activity)
    else:
        flash("活动不存在或已结束", "error")
        return redirect(url_for("activities"))


# 点击报名后
@app.route("/enroll/<int:activity_id>", methods=["POST"])
def enroll(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if not activity or not activity.a_ableParticipate or activity.a_endTime <= datetime.now():
        flash("活动不可报名或已结束", "error")
        return redirect(url_for("activities"))

    participant_number = request.form["participantNumber"]
    remark = request.form.get("remark", "")  # 获取备注信息，默认为空字符串
    if int(participant_number) > (activity.a_participantNumber - activity.a_enrolledNumber):
        flash("报名人数超过剩余名额", "error")
        return redirect(url_for("activity_enroll", activity_id=activity_id))

    # 获取用户id
    username = session.get("username")  # 从会话中获取用户名
    user_id = db_session.query(User).filter_by(u_name=username).first().u_id
    # 创建用户和活动的联系
    activity.a_enrolledNumber += int(participant_number)
    new_participant = user_participate_activity(
        participateNumber=participant_number,
        note=remark,
        user_id=user_id,
        activity_id=activity_id,
    )
    db_session.add(new_participant)
    db_session.commit()
    flash("报名成功", "success")
    return redirect(url_for("activities"))


# 我的报名界面
@app.route("/myenrolled")
def myenrolled():
    print(session)
    username = session.get("username")  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    if user:
        woos = db_session.query(user_participate_activity).filter_by(user_id=user.u_id).all()
        # 从每个记录中提取 activity_id，并将其存储在列表中
        activity_ids = [woo.activity_id for woo in woos]
    else:
        flash("找不到用户", "error")
        return redirect(url_for("login"))
    participations = db_session.query(Activity).filter(Activity.a_id.in_(activity_ids)).all()

    return render_template("myenrolled.html", participations=participations)


# 普通用户取消报名
@app.route("/cancel_enrollment/<int:activity_id>", methods=["POST"])
def cancel_enrollment(activity_id):
    username = session.get("username")  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    if not user:
        flash("您尚未登录或没有权限执行此操作", "error")
        return redirect(url_for("login"))

    # 查询
    participation = db_session.query(user_participate_activity).filter_by(user_id=user.u_id, activity_id=activity_id).first()
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    activity.a_enrolledNumber -= participation.participateNumber
    if participation:
        db_session.delete(participation)
        db_session.commit()
        flash("取消报名成功", "success")
    else:
        flash("取消报名失败，可能您已取消报名或不存在此活动", "error")

    return redirect(url_for("myenrolled"))


@app.route("/user", methods=["GET"])
def get_userinfo():
    if "username" in session:
        username = session.get("username")
        avatar = session.get("avatar")
        return jsonify({"username": username, "avatar": avatar})
    return "User not logged in", 401

def create_forest_variable_table(forest_name):
    class ForestVariable(ForestVariableBase):
        __tablename__ = f'forest_variable_{forest_name}'
        __table_args__ = {'extend_existing': True}
    inspector = inspect(engine)
    table_name = f'forest_variable_{forest_name}'
    if not inspector.has_table(table_name):
        ForestVariable.__table__.create(bind=engine)
        print(f"Table {table_name} created.")
    else:
        print(f"Table {table_name} already exists.")
    return ForestVariable


def get_forest_variable_table(forest_name):
    return create_forest_variable_table(forest_name)


def get_all_forests():
    return db_session.query(Forest).all()

@app.route("/add_forest", methods=["POST"])
def add_forest():
    if request.method == "POST":
        try:
            f_name = request.form["f_name"]
            f_location = request.form["f_location"]
            f_area = request.form["f_area"]
            f_soilType = request.form["f_soilType"]
            f_manager = request.form["f_manager"]
            f_intro = request.form.get("f_intro", "")

            new_forest = Forest(
                f_name=f_name,
                f_location=f_location,
                f_area=f_area,
                f_soilType=f_soilType,
                f_manager=f_manager,
                f_intro=f_intro
            )
            db_session.add(new_forest)
            db_session.commit()
            return jsonify({'status':'success to add forest'})
        
        except SQLAlchemyError as e:
            db_session.rollback()
            return jsonify({'status':'fail to add forest'})


@app.route("/forest_variable", methods=["GET", "POST"])
def view_forest_variable():
    if request.method == "POST":
        forest_name = request.form["forest_name"]
        ForestVariable = get_forest_variable_table(forest_name)
        try:

            forest_variables = db_session.query(ForestVariable).all()
        except SQLAlchemyError as e:
            forest_variables = []

        return render_template("forest_variable.html", forests=get_all_forests(),
                               forest_variables=forest_variables, selected_forest_name=forest_name)
    else:
        return render_template("forest_variable.html", forests=get_all_forests())

@app.route("/add_forest_variable", methods=["POST"])
def add_forest_variable():
    forest_name = request.form["forest_name"]
    print(forest_name)
    ForestVariable = get_forest_variable_table(forest_name)
    try:
        f_temperature = request.form["f_temperature"]
        f_humidity = request.form["f_humidity"]
        f_precipitation = request.form["f_precipitation"]
        f_resourceDistribution = request.form["f_resourceDistribution"]
        f_vegetationCoverage = request.form["f_vegetationCoverage"]
        f_historicalCulture = request.form["f_historicalCulture"]
        f_hydrologicalFeatures = request.form["f_hydrologicalFeatures"]
        f_disasterSituation = request.form["f_disasterSituation"]
        f_wildlife = request.form["f_wildlife"]
        f_economicValue = request.form["f_economicValue"]

        new_variable = ForestVariable(
            f_temperature=f_temperature,
            f_humidity=f_humidity,
            f_precipitation=f_precipitation,
            f_resourceDistribution=f_resourceDistribution,
            f_vegetationCoverage=f_vegetationCoverage,
            f_historicalCulture=f_historicalCulture,
            f_hydrologicalFeatures=f_hydrologicalFeatures,
            f_disasterSituation=f_disasterSituation,
            f_wildlife=f_wildlife,
            f_economicValue=f_economicValue,
            f_date=datetime.now()
        )

        db_session.add(new_variable)
        db_session.commit()

        flash("森林变量信息添加成功", "success")

    except SQLAlchemyError as e:
        db_session.rollback()

    try:
        forest_variables = db_session.query(ForestVariable).all()
    except SQLAlchemyError as e:
        forest_variables = []

    return render_template("forest_variable.html", forests=get_all_forests(),
                           forest_variables=forest_variables, selected_forest_name=forest_name)


@app.route("/forest_info", methods=["GET", "POST"])
def forest_info():
    forests = get_all_forests()

    if request.method == "POST":
        forest_name = request.form["forest_name"]

        forest_static_info = db_session.query(Forest).filter_by(f_name=forest_name).first()

        ForestVariable = get_forest_variable_table(forest_name)

        try:
            forest_variables = db_session.query(ForestVariable).all()
        except OperationalError as e:
            db_session.rollback()  # 回滚事务，防止表修改冲突

            forest_variables = []

        return render_template("forest_info.html",
                               forests=forests,
                               forest_static_info=forest_static_info,
                               forest_variables=forest_variables)

    return render_template("forest_info.html", forests=forests)

@app.route("/get_world_tree_cover_json",methods=["GET"])
def get_world_tree_cover_json():
    # 数据预处理
    iso_data=pd.read_csv("d://Desktop//forest1//ForestEagleEye//dataset//树木覆盖的全球位置//treecover_extent_2010_by_region__ha.csv").fillna(0)
    iso_meta=pd.read_csv("d://Desktop//forest1//ForestEagleEye//dataset//树木覆盖的全球位置//iso_metadata.csv").fillna(0)
    if(iso_data.empty or iso_meta.empty):
        return jsonify({
            'status':'fail',
            'datalist': None
        }),404
    else:
        mergedata=pd.merge(iso_data,iso_meta,on='iso')
        # 整理为列表字典格式
        datalist = [{'name': row['name'], 'value': row['umd_tree_cover_extent_2010__ha']} for index, row in mergedata.iterrows()]
        return jsonify({
            'status':'success',
            'datalist': datalist
        }),200

        








@app.route("/")
def index():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", username=username)
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)


 

