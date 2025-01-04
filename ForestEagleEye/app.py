from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, abort, \
    jsonify
import pymysql
import hashlib
import sqlalchemy
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy import insert
from werkzeug.utils import secure_filename
from sqlalchemy import text
from sqlalchemy import create_engine, Column, Enum, Integer, Table, String, ForeignKey, DateTime, Text, Boolean, Float, \
    inspect, MetaData, select
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from flask import render_template  # 引入模板插件
from sqlalchemy.testing import db
from flask_mail import Mail, Message
import random
from datetime import timedelta
import os
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import re
import pandas as pd
import requests
from http import HTTPStatus
import dashscope

app = Flask(
    __name__,
    static_folder="public/static",  # 指定静态文件目录
    template_folder="public/templates"  # 指定模板文件目录
)
app.secret_key = "123456789"

# 配置上传文件夹路径
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), 'public/uploads')

# 确保上传目录存在
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

metadata = MetaData()

app.config["MAIL_SERVER"] = "smtp.qq.com"  # 邮件服务器
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "3327903803@qq.com"  # 邮箱
app.config["MAIL_PASSWORD"] = "xyjtyyhunuurdadj"  # 邮箱授权码
app.config["MAIL_DEFAULT_SENDER"] = "3327903803@qq.com"  # 邮箱
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

mail = Mail(app)
verification_codes = {}  # 存储邮箱和验证码的字典
dashscope.api_key = 'sk-16d20b70778043379f8afa4b6a940a8b'

# MySQL 数据库连接配置
db_config={
    'user':'root',
    'password':'a!oe3q4r',#这里改成自己的数据库密码
    'host':'localhost',
    'port':3306,
    'database': 'forest',#这里改成自己的数据库名字
    'charset':'utf8mb4'}
# 创建数据库连接
engine = create_engine(
    "mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(**db_config))

Base = declarative_base()

# 森林百科-获取当前文件目录
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
# 森林百科-获取天气数据-城市编号字典
Amap = pd.read_excel(os.path.join(current_dir, 'src/assets/data/AMap_adcode_citycode.xlsx'))
CityCodeMap = pd.Series(Amap['adcode'].values, index=Amap['name']).to_dict()
API_KEY = "a4ff6e3b16fa5bc76d719f465c90e6da"  # 申请的高德地图API密钥，不要改


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
    u_role = Column(Enum("普通用户", "林业从业人员", "林业管理人员", "林业监管人员"), nullable=False,
                    default="普通用户")  # 用户所属角色（普通用户、林业从业人员、林业管理人员、环境管理人员、林业局监管人员）
    u_forest = Column(String(100))  # 所属森林（林业管理人员、环境管理人员、林业局监管人员需要选择）
    u_avatarPath = Column(String(100), nullable=False, default="src/assets/default-avatar.png")  # 头像图片路径
    u_signature = Column(String(100), default="这个人很懒，什么都没有留下...")  # 个性签名
    u_signupTime = Column(DateTime, nullable=False, default=datetime.now)  # 注册时间
    u_newestTime = Column(DateTime, nullable=False, onupdate=datetime.now, default=datetime.now)  # 最近登录时间
    u_institution = Column(Integer, ForeignKey("institutions.i_id"), nullable=True)  # 用户所属机构（除普通用户外需选择）

    # u_submitTips = relationship()  # 提交的建议与举报
    # u_approveTips = relationship()  # 审批的建议与举报
    # u_post = relationship()  # 发布的帖子
    # u_comments = relationship()  # 评论
    # u_likes = relationship()  # 点赞的帖子
    # u_question = relationship()  # 存小林问答问过的问题及回答


class Post(Base):
    __tablename__ = "posts"

    p_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 帖子唯一标识
    p_title = Column(String(200), nullable=False)  # 帖子标题
    p_content = Column(Text, nullable=False)  # 帖子内容
    p_timestamp = Column(DateTime, default=datetime.now, nullable=False)  # 发帖时间
    p_user_id = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 发帖用户ID

    original_post_id = Column(Integer, ForeignKey("posts.p_id"), nullable=True)  # 被转发的帖子ID

    # 定义关系
    images = relationship("Image", back_populates="post", cascade="all, delete-orphan")  # 帖子图片
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")  # 帖子评论
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")  # 帖子点赞
    author = relationship("User", backref="posts")  # 帖子作者

    # 建立 original_post 关系，引用被转发的帖子
    original_post = relationship("Post", remote_side=[p_id], backref="shared_posts")  # 引用原始帖子


class Comment(Base):
    __tablename__ = "comments"
    c_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    c_content = Column(Text, nullable=False)
    c_timestamp = Column(DateTime, default=datetime.now, nullable=False)
    c_user_id = Column(Integer, ForeignKey("users.u_id"), nullable=False)
    c_post_id = Column(Integer, ForeignKey("posts.p_id"), nullable=False)
    author = relationship("User", backref="comments")
    post = relationship("Post", back_populates="comments")
    images = relationship("Image", back_populates="comment", cascade="all, delete-orphan")  # 新增的关系


class Like(Base):
    __tablename__ = "likes"
    l_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 点赞唯一标识
    l_user_id = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 点赞用户ID
    l_post_id = Column(Integer, ForeignKey("posts.p_id"), nullable=False)  # 点赞的帖子ID
    user = relationship("User", backref="likes")  # 点赞用户
    post = relationship("Post", back_populates="likes")  # 被点赞的帖子


class Image(Base):
    __tablename__ = "images"
    img_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    file_path = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.p_id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.c_id"), nullable=True)  # 新增的外键
    post = relationship("Post", back_populates="images")
    comment = relationship("Comment", back_populates="images")  # 定义与 Comment 的关系


# 活动表
class Activity(Base):
    __tablename__ = "activities"
    a_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 活动编号
    a_applicantId = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 申请人id
    a_submitTime = Column(DateTime, nullable=False, default=datetime.now)  # 申请提交时间
    a_attachment = Column(String(100), default="")  # 申请附件
    a_name = Column(String(100), nullable=False)  # 活动名称
    a_type = Column(Enum("伐木", "采摘", "旅游参观", "野营", "捕猎", "冥想", "徒步"), nullable=False)  # 活动类型
    a_forest = Column(String(100), nullable=False)  # 审批单位（森林名称）
    a_location = Column(String(100), nullable=False)  # 活动地点（具体地点）
    a_beginTime = Column(DateTime, nullable=False)  # 活动开始时间
    a_endTime = Column(DateTime, nullable=False)  # 活动结束时间
    a_introduction = Column(String(1000), nullable=False)  # 活动简介
    a_picPath = Column(String(100), default="")  # 活动图片路径
    a_ableParticipate = Column(Boolean, nullable=False)  # 活动是否面向大众（大众可以报名参加）
    a_participantNumber = Column(Integer, nullable=False)  # 活动人数
    a_enrolledNumber = Column(Integer, nullable=False, default=0)  # 已报名人数
    a_state = Column(Enum("approving", "approved", "dismissed", "ongoing", "ended"), nullable=False,
                     default="approving")  # 状态（待审批、通过、驳回、活动开始、活动完成）
    a_approver_id = Column(Integer, ForeignKey("users.u_id"), nullable=True)  # 审批人id
    a_approveTime = Column(DateTime, nullable=True)  # 活动审批时间
    a_dismissreason = Column(String(100), nullable=True)  # 驳回理由


### 机构相关表
# 管理机构
class Institution(Base):
    __tablename__ = "institutions"
    i_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 机构编号
    i_name = Column(String(20), nullable=False, unique=True)  # 机构名称
    i_type = Column(Enum('从业机构', '管理机构'), nullable=False)  # 机构类别


### 森林相关表
# 所有森林常量表
class Forest(Base):
    __tablename__ = "forests"
    f_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 森林编号
    f_name = Column(String(100), nullable=False, unique=True)  # 森林名称
    f_location = Column(String(100), nullable=False, default='中国/中国大陆/中华人民共和国')  # 森林地理位置
    f_area = Column(Integer, nullable=False, default=100)  # 森林占地面积
    f_soilType = Column(String(100), nullable=False, default='暂无')  # 土壤类型
    f_intro = Column(String(1000), default="森林管理员尚未添加简介...")  # 森林简介
    f_manager = Column(Integer, ForeignKey('institutions.i_id'))  # 森林管理机构id

    f_resourceDistribution = Column(String(1000), nullable=True)  # 资源分布
    f_vegetationCoverage = Column(String(1000), nullable=True)  # 植被覆盖
    f_historicalCulture = Column(String(1000), nullable=True)  # 历史文化
    f_disasterSituation = Column(String(1000), nullable=True)  # 灾害情况
    f_wildlife = Column(String(1000), nullable=True)  # 野生动物
    f_economicValue = Column(String(1000), nullable=True)  # 经济价值


# 森林变量表
# 定义基础表模型

### 森林气象变量表
class ForestVariableBase(Base):
    __abstract__ = True  # 抽象基类
    f_date = Column(DateTime, nullable=False, default=datetime.now, primary_key=True)  # 日期，默认当前时间
    f_temperature = Column(Float)  # 温度
    f_humidity = Column(Float)  # 湿度
    f_winddirection = Column(String(20))  # 风向
    f_windpower = Column(String(20))  # 风力


### 森林灾害变量表
class ForestDisasterBase(Base):
    __abstract__ = True
    d_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 编号
    d_date = Column(DateTime, nullable=False, default=datetime.now)  # 日期，默认当前时间
    d_type = Column(Enum("火灾", "极端天气", "干旱", "土壤侵蚀", "酸雨", "地质灾害", "生物灾害", "人为灾害"),
                    nullable=False)  # 灾害类型
    d_loss = Column(Float)  # 受损面积
    d_desc = Column(String(1000))


### 森林动植物资源变量表
class ForestResourceBase(Base):
    __abstract__ = True
    r_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 编号
    r_name = Column(String(100))
    r_type = Column(Enum("动物", "植物", "微生物"), nullable=False)  # 资源类型
    r_latitude = Column(Float)  # 分布中心纬度
    r_longitude = Column(Float)  # 分布中心经度
    r_radius = Column(Float)  # 分布中心半径


### AI消息表
class AIMessage(Base):
    __tablename__ = 'AImessages'
    a_id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)  # 消息编号
    a_user_id = Column(Integer, ForeignKey('users.u_id'), nullable=False)  # 本消息发起用户的id
    a_qtime = Column(DateTime, nullable=False, default=datetime.now)  # 消息发送时间
    a_question = Column(String(1000), nullable=False)  # 消息内容
    a_atime = Column(DateTime, nullable=False, default=datetime.now)  # 消息回答时间
    a_answer = Column(String(1000), nullable=False)  # 消息回答

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
# with engine.connect() as connection:
#     connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
#     inspector = inspect(engine)
#     # foreign_keys = inspector.get_foreign_keys('institutions')
#     # foreign_key_names = [fk['name'] for fk in foreign_keys]

#     # if 'institutions_ibfk_1' in foreign_key_names:
#     #     # 删除外键约束
#     #     connection.execute(text("ALTER TABLE institutions DROP FOREIGN KEY institutions_ibfk_1;"))
#     Base.metadata.drop_all(engine)
#     connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

# Base.metadata.create_all(engine)

db_session_class = sessionmaker(bind=engine)
db_session = db_session_class()


# 以下是为了测试临时添加的森林、管理机构和从业机构
# 完整功能上线后，需删除！

# administrator=Institution(i_name="管理机构-测试",i_type='管理机构')
# db_session.add(administrator)
# db_session.commit()

# practitioner=Institution(i_name='从业机构-测试',i_type='从业机构')
# db_session.add(practitioner)
# db_session.commit()

# forest = Forest(f_name='测试森林',f_manager=administrator.i_id)
# db_session.add(forest)
# db_session.commit()

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
        return jsonify({"status": "success", "message": "验证码已发送到您的邮箱"}), 100
    except Exception as e:
        return jsonify({"status": "fail", "message": "发送邮件失败，请检查邮箱输入是否有误"}), 250


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
        user.u_role = request.form['role']
        if user.u_role != '普通用户':
            user.u_forest = request.form['forest']
            user.u_institution = request.form['inst']
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
        # user = db_session.query(User).filter_by(u_email=email, u_password=password).first() mkbk测试改动
        user = db_session.query(User).filter_by(u_email=email).first()
        if user:
            user.u_newestTime = datetime.now()  # 最新登录时间设置为当前时间
            days = (user.u_newestTime - user.u_signupTime).days + 1
            db_session.commit()  # 提交更改到数据库

            # 在森林表和机构表中查询forest和inst的名称+编号
            forest = db_session.query(Forest).filter_by(f_id=user.u_forest).first()
            inst = db_session.query(Institution).filter_by(i_id=user.u_institution).first()

            success = "欢迎来到林上鹰眼！"
            data = {'status': 'success',
                    'message': success,

                    'days': days,
                    'avatar': user.u_avatarPath,
                    'user_id': user.u_id,
                    'newestTime': user.u_newestTime.strftime('%Y-%m-%d %H:%M:%S'),
                    'signupTime': user.u_signupTime.strftime('%Y-%m-%d'),
                    'role': user.u_role,
                    'username': user.u_name,
                    'email': user.u_email,
                    'signature': user.u_signature
                    }
            if user.u_role != '普通用户':
                data['forest'] = f"{forest.f_name}(FO{forest.f_id})"
                data['inst'] = f"{inst.i_name}(INST{inst.i_id})"
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
@app.route("/get_all_forests", methods=["GET"])
def getAllForests():
    # 获取所有管理机构的名称和 ID
    institutions = {inst.i_id: inst.i_name for inst in db_session.query(Institution).filter_by(i_type='管理机构').all()}

    forests = [{
        'value': forest.f_id,
        "label": forest.f_name,
        "location": forest.f_location,
        "area": forest.f_area,
        "manager": institutions.get(forest.f_manager),  # 使用森林的管理机构 ID 从字典中获取名称
        "intro": forest.f_intro,
    } for forest in db_session.query(Forest).all()]

    if forests:
        return jsonify({'forests': forests})
    return 401


# 获取对应森林的机构（用于非普通用户角色的注册）
@app.route("/get_relative_inst", methods=['POST'])
def getRelativeInstitutions():
    if request.form['role'] == '林业从业人员':
        inst_type = '从业机构'
    else:
        inst_type = '管理机构'
    try:
        insts = [{'value': inst.i_id, 'label': inst.i_name} for inst in
                 db_session.query(Institution).filter_by(i_type=inst_type)]
        db_session.commit()
        if insts:
            return jsonify({'insts': insts})
        else:
            return jsonify({'error': 'No institutions found for the given criteria.'}), 404
    except Exception as e:
        return jsonify({'error': f'An error occurred while querying the database: {str(e)}'}), 500


# 森林百科-编辑详情-上传森林相册图片
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route("/uploadForestImage", methods=["POST"])
def uploadForestImage():
    if 'files' not in request.files:
        return jsonify({'message': '没有文件上传', 'status': 'error'}), 400
    files = request.files.getlist('files')
    f_name = request.form.get('f_name')

    for file in files:
        if file.filename == '':
            return jsonify({'message': '未选择文件', 'status': 'error'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 给文件名加上前缀 f_name
            new_filename = f"{f_name}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            # 这里可以添加代码将文件信息存储到数据库中
            return jsonify({'message': '文件上传成功', 'path': file_path})
    return jsonify({"message": "文件类型不支持", "status": "error"}), 400


### 动态创建并获取动植物资源详情的表格
def create_resource_variable_table(f_name):
    class ForestResource(ForestResourceBase):
        __tablename__ = f'forest_resource_{f_name}'
        __table_args__ = {'extend_existing': True}

    inspector = inspect(engine)
    table_name = f'forest_resource_{f_name}'
    if not inspector.has_table(table_name):
        ForestResource.__table__.create(bind=engine)
        print(f'Table {table_name} created.')
    else:
        print(f'Table {table_name} already exists.')
    return ForestResource


def get_forest_resource_table(f_name):
    return create_resource_variable_table(f_name)


# 森林百科-编辑相册-上传动植物资源文件
@app.route("/uploadResourceFile", methods=["POST"])
def uploadResourceFile():
    if 'file' not in request.files:
        return jsonify({'error': '未上传文件'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名无效'})
    # 文件上传成功，转为变量表添加记录
    df = pd.read_excel(file.stream)

    # 添加到数据库
    f_name = request.form['f_name']
    ForestResource = get_forest_resource_table(f_name)
    try:
        for index, row in df.iterrows():
            new_resource = ForestResource(
                r_name=row['资源名称'],
                r_type=row['资源类型'],
                r_latitude=row['分布中心纬度'],
                r_longitude=row['分布中心经度'],
                r_radius=row['分布范围半径(公里)']
            )
            db_session.add(new_resource)
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
    return jsonify({'message': '文件上传成功'}), 200


### 动态创建并获取灾害详情的表格
def create_disaster_variable_table(f_name):
    class ForestDisaster(ForestDisasterBase):
        __tablename__ = f'forest_disaster_{f_name}'
        __table_args__ = {'extend_existing': True}

    inspector = inspect(engine)
    table_name = f'forest_disaster_{f_name}'
    if not inspector.has_table(table_name):
        ForestDisaster.__table__.create(bind=engine)
        print(f'Table {table_name} created.')
    else:
        print(f'Table {table_name} already exists.')
    return ForestDisaster


def get_forest_disaster_table(f_name):
    return create_disaster_variable_table(f_name)


# 森林百科-编辑相册-上传灾害文件
@app.route("/uploadDisasterFile", methods=["POST"])
def uploadDisasterFile():
    if 'file' not in request.files:
        return jsonify({'error': '未上传文件'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名无效'})
    # 文件上传成功，转为变量表添加记录
    df = pd.read_excel(file.stream)
    df['日期'] = pd.to_datetime(df['日期'])

    # 添加到数据库
    f_name = request.form['f_name']
    ForestDisaster = get_forest_disaster_table(f_name)
    try:
        for index, row in df.iterrows():
            new_disaster = ForestDisaster(
                d_date=row['日期'],
                d_type=row['灾害类型'],
                d_loss=row['受损森林面积(公顷)'],
                d_desc=row['灾情概述']
            )
            db_session.add(new_disaster)
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
    return jsonify({'message': '文件上传成功'}), 200


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
@app.route("/apply", methods=["POST"])
def apply():
    u_id = request.form.get("user_id")
    # print(u_id)
    if not u_id:
        flash("未提供有效的user_id", "error")
        return jsonify({"error": "未提供有效的user_id"}), 400
    user = db_session.query(User).filter_by(u_id=u_id).first()
    if not user:
        flash("用户不存在", "error")
        return jsonify({"error": "用户不存在"}), 404
        # 根据当前管理员的森林名称和状态查询活动
    approving_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id,
                                                             Activity.a_state == "approving").all()
    approved_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id,
                                                            Activity.a_state == "approved").all()
    dismissed_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id,
                                                             Activity.a_state == "dismissed").all()

    # 将活动转换为字典格式返回
    approving_activities_data = [{"a_id": activity.a_id, "a_name": activity.a_name, "a_forest": activity.a_forest,
                                  "a_approver_id": activity.a_approver_id, "a_approveTime": activity.a_approveTime} for
                                 activity in approving_activities]
    approved_activities_data = [{"a_id": activity.a_id, "a_name": activity.a_name, "a_forest": activity.a_forest,
                                 "a_approver_id": activity.a_approver_id, "a_approveTime": activity.a_approveTime} for
                                activity in approved_activities]
    dismissed_activities_data = [{"a_id": activity.a_id, "a_name": activity.a_name, "a_forest": activity.a_forest,
                                  "a_approver_id": activity.a_approver_id, "a_approveTime": activity.a_approveTime} for
                                 activity in dismissed_activities]

    # 返回 JSON 数据
    return jsonify({
        "approving_activities": approving_activities_data,
        "approved_activities": approved_activities_data,
        "dismissed_activities": dismissed_activities_data
    })


# 创建活动(没有处理上传的图片！！)
@app.route("/create_activity", methods=["POST"])
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
        # 打印出所有接收到的字段
        print(
            f"接收到的表单字段: {a_name}, {a_location}, {a_beginTime}, {a_endTime}, {a_participantNumber}, {a_introduction}, {a_forest}, {a_type}, {a_ableParticipate}")
        a_picPath = request.form.get("a_picPath")  # 获取图片路径
        # 处理文件上传
        if not a_picPath:
            return jsonify({"message": "缺少活动封面图片", "status": "error"}), 400

        # 将前端传来的字符串转为 datetime 对象
        a_beginTime = datetime.strptime(a_beginTime, "%Y-%m-%dT%H:%M")
        a_endTime = datetime.strptime(a_endTime, "%Y-%m-%dT%H:%M")

        u_id = request.form.get("user_id")
        if not u_id:
            return jsonify({"message": "用户ID缺失", "status": "error"}), 400
        print(u_id)
        # 创建新的 Activity 实例
        new_activity = Activity(
            a_applicantId=u_id,
            a_name=a_name,
            a_location=a_location,
            a_beginTime=a_beginTime,
            a_endTime=a_endTime,
            a_participantNumber=int(a_participantNumber),
            a_introduction=a_introduction,
            a_picPath=a_picPath,
            a_ableParticipate=a_ableParticipate,
            a_type=a_type,
            a_forest=a_forest,
            a_state="approving",  # 默认状态为待审批
        )

        # 将新活动添加到数据库会话并提交
        try:
            db_session.add(new_activity)
            db_session.commit()
        except Exception as e:
            print(f"数据库操作失败: {e}")
            db_session.rollback()
            return jsonify({"message": "创建活动失败", "status": "error"}), 500

        # 返回成功的 JSON 响应
        return jsonify({"message": "活动创建成功，等待审批", "status": "success"}), 200

    # 对于 GET 请求，可以返回活动创建页面的 JSON 数据（如果需要的话）
    return jsonify({"message": "GET请求不支持", "status": "error"}), 405


@app.route("/upload_activity_image", methods=["POST"])
def upload_activity_image():
    if 'file' not in request.files:
        return jsonify({"message": "没有文件上传", "status": "error"}), 400

    file = request.files['file']

    # 检查文件是否符合要求
    if file and allowed_file(file.filename):  # `allowed_file` 验证文件类型
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 保存文件
        try:
            file.save(filepath)
        except Exception as e:
            print(f"文件保存失败: {e}")
            return jsonify({"message": "文件保存失败", "status": "error"}), 500

        # 返回成功消息
        file_url = f"/public/uploads/{filename}"
        return jsonify({"filePath": file_url, "status": "success"}), 200

    return jsonify({"message": "文件类型不支持", "status": "error"}), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# 活动详情页，申请人和审批人公用界面，但是会传递一个is_approver参数决定前端是否显示“同意”“驳回”
@app.route("/activity_detail/<int:activity_id>", methods=["POST"])
def activity_detail(activity_id):
    u_id = request.form.get("user_id")
    if not u_id:
        return jsonify({"message": "用户ID缺失", "status": "error"}), 400
    # print(u_id)
    user = db_session.query(User).filter_by(u_id=u_id).first()
    current_user_role = user.u_role
    # 判断当前用户是否为审批人
    is_approver = (current_user_role == "林业管理人员" or current_user_role == "林业监管人员")
    # print("执行到了")
    # print(is_approver)

    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if not activity:
        flash("活动不存在", "error")
        return redirect(url_for("activity"))

    # 返回 JSON 数据，供 Vue.js 前端使用
    return jsonify({
        'activity': {
            'a_id': activity.a_id,
            'a_name': activity.a_name,
            'a_location': activity.a_location,
            'a_type': activity.a_type,
            'a_beginTime': activity.a_beginTime,
            'a_endTime': activity.a_endTime,
            'a_participantNumber': activity.a_participantNumber,
            'a_enrolledNumber': activity.a_enrolledNumber,
            'a_forest': activity.a_forest,
            'a_introduction': activity.a_introduction,
            'a_state': activity.a_state,
            'a_applicantId': activity.a_applicantId,
            'a_submitTime': activity.a_submitTime,
            'a_picPath': activity.a_picPath,
            'a_ableParticipate': activity.a_ableParticipate
        },
        'isApprover': is_approver
    })


@app.route("/delete_activity/<int:activity_id>", methods=["POST"])
def delete_activity(activity_id):
    # 查找活动
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()

    if activity:
        # 删除活动
        db_session.delete(activity)
        db_session.commit()

        # 返回成功响应
        return jsonify({
            "status": "success",
            "message": "活动已成功删除~"
        })
    else:
        # 如果活动不存在或已被删除，返回失败响应
        return jsonify({
            "status": "error",
            "message": "活动不存在或已被删除"
        })


# 我的审批界面
@app.route("/approve", methods=["POST"])
def approve():
    u_id = request.form.get("user_id")
    # print(u_id)
    if not u_id:
        flash("未提供有效的user_id", "error")
        return jsonify({"error": "未提供有效的user_id"}), 400
    user = db_session.query(User).filter_by(u_id=u_id).first()
    if not user:
        flash("用户不存在", "error")
        return jsonify({"error": "用户不存在"}), 404

    forest = db_session.query(Forest).filter_by(f_id=user.u_forest).first()
    current_forest = forest.f_id

    if not current_forest:
        flash("您尚未登录或没有权限访问此页面", "error")
        return redirect(url_for("login"))

    # 根据当前管理员的森林名称和状态查询活动
    approving_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest,
                                                             Activity.a_state == "approving").all()
    approved_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest,
                                                            Activity.a_state == "approved").all()
    dismissed_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest,
                                                             Activity.a_state == "dismissed").all()

    # 将活动转换为字典格式返回
    approving_activities_data = [{"a_id": activity.a_id, "a_name": activity.a_name, "startTime": activity.a_beginTime,
                                  "applicant": activity.a_applicantId} for activity in approving_activities]
    approved_activities_data = [{"a_id": activity.a_id, "a_name": activity.a_name, "startTime": activity.a_beginTime,
                                 "applicant": activity.a_applicantId} for activity in approved_activities]
    dismissed_activities_data = [{"a_id": activity.a_id, "a_name": activity.a_name, "startTime": activity.a_beginTime,
                                  "applicant": activity.a_applicantId} for activity in dismissed_activities]

    # 返回 JSON 数据
    return jsonify({
        "approving_activities": approving_activities_data,
        "approved_activities": approved_activities_data,
        "dismissed_activities": dismissed_activities_data
    })


# 审批通过
@app.route("/approve_activity/<int:activity_id>", methods=["POST"])
def approve_activity(activity_id):
    # 审批活动逻辑
    # 更新活动状态为 'approved'
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    # 获取当前审批人的id
    user_id = request.form.get("user_id")
    user = db_session.query(User).filter_by(u_id=user_id).first()
    # 修改状态
    activity.a_state = "approved"
    print("执行到了同意")
    print(activity.a_id)
    print(activity.a_state)
    # 存储审批人的id
    activity.a_approver_id = user.u_id
    # 存储审批时间
    activity.a_approveTime = datetime.now()
    db_session.commit()  # 确保提交更改
    return jsonify({"message": "Activity approved successfully"}), 200


# 审批驳回
@app.route("/dismiss_activity/<int:activity_id>", methods=["POST"])
def dismiss_activity(activity_id):
    dismiss_reason = request.form.get("dismiss_reason", "")
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    # 获取当前审批人的id
    user_id = request.form.get("user_id")
    user = db_session.query(User).filter_by(u_id=user_id).first()
    # 修改状态
    activity.a_state = "dismissed"
    # print("执行到了驳回")
    # 存储审批人的id
    activity.a_approver_id = user.u_id
    # 存储审批时间
    activity.a_approveTime = datetime.now()
    # 存储驳回理由
    activity.a_dismissreason = dismiss_reason
    db_session.commit()  # 确保提交更改
    return jsonify({"message": "Activity dismissed successfully"}), 200


# 活动风采界面
@app.route("/activities", methods=["GET"])
def activities():
    # 获取当前时间
    now = datetime.now()

    # 获取所有活动，包括：未截止且通过的活动，以及已截止且通过的活动
    activities = db_session.query(Activity).filter(
        Activity.a_ableParticipate == True,
        Activity.a_state == "approved"
    ).all()

    # 分类活动：按活动的状态分组
    due_activities = [activity for activity in activities if activity.a_endTime > now]
    overdue_activities = [activity for activity in activities if activity.a_endTime <= now]

    # 返回活动数据
    activities_data = {
        'due_activities': [],
        'overdue_activities': []
    }

    for activity in due_activities:
        activities_data['due_activities'].append({
            'id': activity.a_id,
            'name': activity.a_name,
            'picPath': activity.a_picPath,
            'location': activity.a_location,
            'type': activity.a_type,
            'introduction': activity.a_introduction,
            'participantNumber': activity.a_participantNumber,
            'enrolledNumber': activity.a_enrolledNumber
        })



    for activity in overdue_activities:
        activities_data['overdue_activities'].append({
            'id': activity.a_id,
            'name': activity.a_name,
            'picPath': activity.a_picPath,
            'location': activity.a_location,
            'type': activity.a_type,
            'introduction': activity.a_introduction,
            'participantNumber': activity.a_participantNumber,
            'enrolledNumber': activity.a_enrolledNumber
        })

    return jsonify(activities_data)


# 报名活动界面
@app.route("/activity_enroll/<int:activity_id>", methods=["GET"])
def activity_enroll(activity_id):
    # print(activity_id)
    # 查询数据库，获取指定活动的详情
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    # print("执行到了1")
    if not activity:
        return jsonify({"success": False, "message": "活动未找到"}), 404

    # 检查活动是否可以报名（如活动时间未过等）
    now = datetime.now()
    if activity.a_endTime <= now or not activity.a_ableParticipate:
        return jsonify({"success": False, "message": "活动不可报名或已结束"}), 400

    # 返回活动详情
    activity_data = {
        "id": activity.a_id,
        "name": activity.a_name,
        "picPath": activity.a_picPath,
        "location": activity.a_location,
        "type": activity.a_type,
        "introduction": activity.a_introduction,
        "participantNumber": activity.a_participantNumber,
        "enrolledNumber": activity.a_enrolledNumber,
    }

    return jsonify({"success": True, "activity": activity_data})


# 点击报名后
@app.route("/enroll/<int:activity_id>", methods=["POST"])
def enroll(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if not activity or not activity.a_ableParticipate or activity.a_endTime <= datetime.now():
        return jsonify({"success": False, "message": "活动不可报名或已结束"})

    participant_number = request.form.get("participantNumber")
    remark = request.form.get("remark", "")  # 获取备注信息，默认为空字符串

    if int(participant_number) > (activity.a_participantNumber - activity.a_enrolledNumber):
        return jsonify({"success": False, "message": "报名人数超过剩余名额"})

    # 获取用户id
    user_id = request.form.get("user_id")

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
    return jsonify({"success": True})


# 我的报名界面
@app.route("/myenrolled", methods=["POST"])
def myenrolled():
    user_id = request.form.get("user_id")
    user = db_session.query(User).filter_by(u_id=user_id).first()

    if user:
        woos = db_session.query(user_participate_activity).filter_by(user_id=user.u_id).all()
        # 从每个记录中提取 activity_id，并将其存储在列表中
        activity_ids = [woo.activity_id for woo in woos]
    else:
        return jsonify({"success": False, "message": "找不到用户"}), 400

    participations = db_session.query(Activity).filter(Activity.a_id.in_(activity_ids)).all()

    # 返回活动数据
    activities = [
        {
            "a_id": participation.a_id,
            "a_name": participation.a_name,
            "a_location": participation.a_location,
            "a_type": participation.a_type,
            "a_beginTime": participation.a_beginTime
        }
        for participation in participations
    ]

    return jsonify({"success": True, "participations": activities})


# 普通用户取消报名
@app.route("/cancel_enrollment/<int:activity_id>", methods=["POST"])
def cancel_enrollment(activity_id):
    user_id = request.form.get("user_id")
    user = db_session.query(User).filter_by(u_id=user_id).first()

    if not user:
        return jsonify({"success": False, "message": "您尚未登录或没有权限执行此操作"}), 403

    # 查询
    participation = db_session.query(user_participate_activity).filter_by(user_id=user.u_id,
                                                                          activity_id=activity_id).first()
    if participation:
        activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
        activity.a_enrolledNumber -= participation.participateNumber
        db_session.delete(participation)
        db_session.commit()
        return jsonify({"success": True, "message": "取消报名成功"})
    else:
        return jsonify({"success": False, "message": "取消报名失败，可能您已取消报名或不存在此活动"}), 400


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
            return jsonify({'message': 'success to add forest', 'status': 'success'})

        except SQLAlchemyError as e:
            db_session.rollback()
            return jsonify({'message': 'fail to add forest', 'status': 'error'})


@app.route("/delete_forest", methods=["POST"])
def delete_forest():
    if request.method == 'POST':
        print(request)
        try:
            f_id = request.form['f_id']
            forest_to_delete = db_session.query(Forest).filter_by(f_id=f_id).first()
            if forest_to_delete:
                db_session.delete(forest_to_delete)
                db_session.commit()
                return jsonify({'message': '该记录已成功在林上鹰眼数据库删除~'})
            else:
                raise Exception("Forest not found")
        except SQLAlchemyError as e:
            db_session.rollback()
            return jsonify({'message': '操作失败，请重新尝试'})


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


@app.route("/get_world_tree_cover_json", methods=["GET"])
def get_world_tree_cover_json():
    # 获取当前文件的绝对路径
    iso_data_fp = os.path.join(current_dir, 'src/assets/data/treecover_extent_2010_by_region__ha.csv')
    iso_meta_fp = os.path.join(current_dir, 'src/assets/data/iso_metadata.csv')
    print(iso_meta_fp)
    # 数据预处理
    iso_data = pd.read_csv(iso_data_fp).fillna(0)
    iso_meta = pd.read_csv(iso_meta_fp).fillna(0)
    if (iso_data.empty or iso_meta.empty):
        return jsonify({
            'status': 'fail',
            'datalist': None
        }), 404
    else:
        mergedata = pd.merge(iso_data, iso_meta, on='iso')
        # 整理为列表字典格式
        datalist = [{'name': row['name'], 'value': row['umd_tree_cover_extent_2010__ha']} for index, row in
                    mergedata.iterrows()]
        return jsonify({
            'status': 'success',
            'datalist': datalist
        }), 200


# 此处获取到weather记录后，会同步添加到数据库
@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    altcity = request.form['altcity']
    forest_name = request.form["f_name"]
    adcode = CityCodeMap.get(city, 'no data')
    if adcode == 'no data':
        adcode = CityCodeMap.get(altcity, 'no data')
    if adcode != 'no data':
        # 向高德API发送请求
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={API_KEY}&city={adcode}&extensions=base&output=JSON"
        response = requests.get(url)
        data = response.json()

        if data['status']:
            w_temperature = data['lives'][0]['temperature']
            w_winddirection = data['lives'][0]['winddirection']
            w_windpower = data['lives'][0]['windpower']
            w_humidity = data['lives'][0]['humidity']
            w_time = datetime.strptime(data['lives'][0]['reporttime'], '%Y-%m-%d %H:%M:%S')

            # 添加到数据库
            ForestVariable = get_forest_variable_table(forest_name)
            try:
                new_variable = ForestVariable(
                    f_temperature=float(w_temperature),
                    f_humidity=float(w_humidity),
                    f_winddirection=w_winddirection,
                    f_windpower=w_windpower,
                    f_date=w_time
                )
                db_session.add(new_variable)
                db_session.commit()

            except SQLAlchemyError as e:
                db_session.rollback()

            # 返回前端展示数据
            weather = [{
                'temperature': w_temperature,
                'winddirection': w_winddirection,
                'windpower': w_windpower,
                'humidity': w_humidity,
                'time': w_time.strftime('%Y-%m-%d %H:%M:%S')  # 将 datetime 对象转换为 ISO 格式的字符串
            }]
            return jsonify({'status': 'success', 'weather': weather}), 200
    return jsonify({'status': 'fail'}), 404


@app.route('/setForestInfo', methods=['POST'])
def setForestInfo():
    if request.method == 'POST':
        intro = request.form['intro']
        print(intro)
        forest = db_session.query(Forest).filter_by(f_id=request.form["id"]).first()
        # 更新记录
        forest.f_intro = intro
        db_session.commit()
        return jsonify({'status': 'success', 'message': 'edited f_intro successfully'}), 200
    return jsonify({'status': 'fail', 'message': 'failed to edit f_intro'}), 404


## 单林区查询
@app.route('/searchOneForest', methods=['POST'])
def searchOneForest():
    f_id = request.form['f_id']
    forest = db_session.query(Forest).filter_by(f_id=f_id).first()
    institutions = {inst.i_id: inst.i_name for inst in db_session.query(Institution).filter_by(i_type='管理机构').all()}

    # 待返回的动态表
    weather_formatted_data = {}
    resource_formatted_data = {}
    disaster_formatted_data = {}

    # 加载数据库中的所有表结构
    metadata.reflect(bind=engine)

    # 天气数据
    weatherTableName = 'forest_variable_' + forest.f_name
    if weatherTableName in metadata.tables:
        weatherTable = metadata.tables[weatherTableName]
        query = select(weatherTable)
        result = db_session.execute(query)
        rows = result.fetchall()
        weather = [row._asdict() for row in rows]

        # 格式化数据
        weather_formatted_data = {
            'dates': [item['f_date'].strftime('%Y-%m-%d %H:%M:%S') for item in weather],
            'temperatures': [item['f_temperature'] for item in weather],
            'humidities': [item['f_humidity'] for item in weather],
            'winddirections': [item['f_winddirection'] for item in weather],
            'windpowers': [item['f_windpower'] for item in weather]
        }

    # 资源数据
    resourceTableName = 'forest_resource_' + forest.f_name
    if resourceTableName in metadata.tables:
        resourceTable = metadata.tables[resourceTableName]
        query = select(resourceTable)
        result = db_session.execute(query)
        rows = result.fetchall()
        resource = [row._asdict() for row in rows]

        # 格式化数据
        resource_formatted_data = {
            'id': [item['r_id'] for item in resource],
            'name': [item['r_name'] for item in resource],
            'type': [item['r_type'] for item in resource],
            'latitude': [item['r_latitude'] for item in resource],
            'longitude': [item['r_longitude'] for item in resource],
            'radius': [item['r_radius'] for item in resource],
        }

    # 灾害数据
    disasterTableName = 'forest_disaster_' + forest.f_name
    if disasterTableName in metadata.tables:
        disasterTable = metadata.tables[disasterTableName]
        query = select(disasterTable)
        result = db_session.execute(query)
        rows = result.fetchall()
        disaster = [row._asdict() for row in rows]

        # 格式化数据
        disaster_formatted_data = {
            'dates': [item['d_date'].strftime('%Y-%m-%d %H:%M:%S') for item in disaster],
            'type': [item['d_type'] for item in disaster],
            'loss': [item['d_loss'] for item in disaster],
            'desc': [item['d_desc'] for item in disaster],
        }

    # 基本静态表
    baseInfo = [{
        'sf_name': forest.f_name,
        'sf_area': forest.f_area,
        'sf_location': forest.f_location,
        'sf_manager': institutions.get(forest.f_manager),
        'sf_intro': forest.f_intro,
        'sf_id': forest.f_id
    }]

    # 森林相册图片
    image_paths = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith(forest.f_name) and filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path = '/public/uploads/' + filename
            image_paths.append(file_path)

    # 返回全部表信息
    return jsonify({
        'baseInfo': baseInfo,
        'sf_images': image_paths,
        'weather': weather_formatted_data,
        'resource': resource_formatted_data,
        'disaster': disaster_formatted_data
    })


# 这里是论坛首页，现在的session我写死了等于一个字符串，到时候只需登录的时候把session动态填写一下就好
# 返回字典 post代表帖子信息，user代表用户信息
@app.route('/forum', methods=['GET'])
def forum_home():
    username = request.args.get('username')
    user = db_session.query(User).filter_by(u_name=username).first()
    if not user:
        return jsonify({"error": "User not logged in"}), 403

    posts = db_session.query(Post).order_by(Post.p_timestamp.desc()).all()

    post_data = []
    for post in posts:
        post_images = [image.file_path for image in post.images[:3]]
        like_count = len(post.likes)
        is_liked = any(like.l_user_id == user.u_id for like in post.likes)

        total_likes = db_session.query(Like).filter_by(l_user_id=user.u_id).count()
        total_posts = db_session.query(Post).filter_by(p_user_id=user.u_id).count()

        post_data.append({
            "id": post.p_id,
            "title": post.p_title,
            "content_preview": post.p_content[:280] + "..." if len(post.p_content) > 280 else post.p_content,
            "images": post_images,
            "like_count": like_count,
            "is_liked": is_liked,
            "time": post.p_timestamp,
            "author": {
                "username": post.author.u_name,
                "avatar": f"/{post.author.u_avatarPath}"
            },
            "original_post": {
                "id": post.original_post.p_id,
                "title": post.original_post.p_title
            } if post.original_post else None,
        })

    return jsonify({"posts": post_data, "total_likes": total_likes, "total_writes": total_posts})


# 发表帖子
@app.route('/forum/post', methods=['GET', 'POST'])
def forum_post():
    if request.method == 'POST':
        username = request.form['username']
        user = db_session.query(User).filter_by(u_name=username).first()
        if not user:
            return jsonify({"error": "User not logged in"}), 403

        title = request.form['title']
        content = request.form['content']
        images = request.files.getlist('images')

        new_post = Post(p_title=title, p_content=content, author=user)
        db_session.add(new_post)
        db_session.commit()

        for index, image in enumerate(images[:9]):
            if image.filename != '':
                filename = secure_filename(f"{new_post.p_id}_{index + 1}_{image.filename}")
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(filepath)

                relative_path = f"uploads/{filename}"
                new_image = Image(file_path=relative_path, post=new_post)
                db_session.add(new_image)
        db_session.commit()

        return jsonify({"message": "Post created successfully", "post_id": new_post.p_id}), 200
    

@app.route('/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    username = request.form['username']
    user = db_session.query(User).filter_by(u_name=username).first()
    if not user:
        return jsonify({"error": "User not logged in"}), 403

    existing_like = db_session.query(Like).filter_by(l_user_id=user.u_id, l_post_id=post_id).first()

    if existing_like:
        db_session.delete(existing_like)
        action = "unliked"
    else:
        new_like = Like(l_user_id=user.u_id, l_post_id=post_id)
        db_session.add(new_like)
        action = "liked"

    db_session.commit()

    like_count = db_session.query(Like).filter_by(l_post_id=post_id).count()
    return jsonify({
        "action": action,
        "like_count": like_count,
        "post_id": post_id,
        "is_liked": action == "liked"
    })


@app.route('/post/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    username = request.args.get('username')

    post = db_session.query(Post).get(post_id)
    comments = db_session.query(Comment).filter_by(c_post_id=post_id).all()

    post_data = {
        "id": post.p_id,
        "title": post.p_title,
        "content": post.p_content,
        "images": [image.file_path for image in post.images],
        "time": post.p_timestamp,
        "author": {
            "username": post.author.u_name,
            "avatar": f"/{post.author.u_avatarPath}"
        },
        "original_post": {
            "id": post.original_post.p_id,
            "title": post.original_post.p_title,
            "author": post.original_post.author.u_name,
            "avatar": f"/{post.original_post.author.u_avatarPath}"
        } if post.original_post else None
    }

    comments_data = []
    for comment in comments:
        comment_images = [image.file_path for image in comment.images[:3]]
        comments_data.append({
            "content": comment.c_content,
            "author": {
                "username": comment.author.u_name,
                "avatar": f"/{comment.author.u_avatarPath}"
            },
            "images": comment_images
        })

    like_count = db_session.query(Like).filter_by(l_post_id=post_id).count()
    user = db_session.query(User).filter_by(u_name=username).first()
    existing_like = db_session.query(Like).filter_by(l_user_id=user.u_id, l_post_id=post_id).first()

    if existing_like:
        action = "liked"
    else:
        action = "unliked"

    return jsonify({"posts": post_data, "comments": comments_data, "like_count": like_count, "is_liked": action == "liked"})


@app.route('/post/<int:post_id>/comment', methods=['POST'])
def post_comment(post_id):
    username = request.form['username']
    print()
    print(username)
    print()

    content = request.form['content']
    images = request.files.getlist('images')

    user = db_session.query(User).filter_by(u_name=username).first()
    print()
    print(user)
    print()
    print(user.u_id)
    new_comment = Comment(c_content=content, c_post_id=post_id, author=user)
    db_session.add(new_comment)
    db_session.commit()

    for index, image in enumerate(images[:3]):
        if image.filename != '':
            filename = secure_filename(f"{new_comment.c_id}_{index + 1}_{image.filename}")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filepath)

            relative_path = f"uploads/{filename}"
            new_image = Image(file_path=relative_path, comment=new_comment)
            db_session.add(new_image)
    db_session.commit()

    return jsonify({"message": "Comment created successfully", "comment_id": new_comment.c_id}), 200

@app.route('/post/<int:post_id>/share', methods=['POST'])
def share_post(post_id):
    username = request.form['username']
    user = db_session.query(User).filter_by(u_name=username).first()
    if not user:
        return jsonify({"error": "User not logged in"}), 403

    if user is None:
        return jsonify({"error": "User not found"}), 404

    title = request.form['title']
    content = request.form['content']
    images = request.files.getlist('images')

    original_post = db_session.query(Post).filter_by(p_id=post_id).first()
    if original_post is None:
        return jsonify({"error": "Original post not found"}), 404

    new_post = Post(
        p_title=title+"(转发)",
        p_content=content,
        author=user,
        original_post_id=original_post.p_id
    )
    db_session.add(new_post)
    db_session.commit()

    for index, image in enumerate(images[:9]):
        if image.filename != '':
            filename = secure_filename(f"{new_post.p_id}_{index + 1}_{image.filename}")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filepath)

            relative_path = f"uploads/{filename}"
            new_image = Image(file_path=relative_path, post=new_post)
            db_session.add(new_image)
    db_session.commit()

    return jsonify({
        "message": "Post shared successfully",
        "shared_post_id": new_post.p_id
    }), 200


@app.route('/user/<string:username>', methods=['GET'])
def user_profile(username):
    user = db_session.query(User).filter_by(u_name=username).first()
    if user is None:
        return redirect(url_for('forum_home'))

    # 获取要显示的栏目，默认为“我的发布”
    tab = request.args.get('tab', 'my_posts')

    if tab == 'my_posts':
        # 仅查询原创发布的帖子，排除转发的帖子
        posts = db_session.query(Post).filter(Post.p_user_id == user.u_id, Post.original_post_id == None).order_by(
            Post.p_timestamp.desc()).all()
    elif tab == 'my_likes':
        # 查询用户点赞的帖子
        posts = db_session.query(Post).join(Like).filter(Like.l_user_id == user.u_id).order_by(
            Post.p_timestamp.desc()).all()
    elif tab == 'my_favorites':  # “我的转发”
        # 查询用户转发的帖子（即 original_post_id 不为空的帖子）
        posts = db_session.query(Post).filter(Post.p_user_id == user.u_id, Post.original_post_id != None).order_by(
            Post.p_timestamp.desc()).all()
    else:
        posts = []

    # 格式化帖子数据
    post_data = []
    for post in posts:
        post_images = [image.file_path for image in post.images[:3]]
        like_count = db_session.query(Like).filter_by(l_post_id=post.p_id).count()
        is_liked = db_session.query(Like).filter_by(l_user_id=user.u_id, l_post_id=post.p_id).first() is not None

        # 如果是转发的帖子，包含原帖信息
        original_post_data = None
        if post.original_post:
            original_post_data = {
                "id": post.original_post.p_id,
                "title": post.original_post.p_title,
                "author": {
                    "username": post.original_post.author.u_name,
                    "avatar": f"/{post.original_post.author.u_avatarPath}"
                }
            }

        post_data.append({
            "id": post.p_id,
            "title": post.p_title,
            "content_preview": post.p_content[:100],
            "images": post_images,
            "like_count": like_count,
            "is_liked": is_liked,
            "author": {
                "username": post.author.u_name,
                "avatar": f"/{post.author.u_avatarPath}"
            },
            "original_post": original_post_data  # 添加原帖信息
        })

    return render_template('user_profile.html', user=user, posts=post_data, current_tab=tab)


@app.route('/ask_model', methods=['POST'])
def ask_model():
    qtime=datetime.now()
    question = request.form.get('question', '')
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=question
        )

        if response.status_code == HTTPStatus.OK:

            if isinstance(response.output, dict) and 'text' in response.output:
                answer = response.output['text']
            else:

                answer = response.output
            print(answer)

            atime=datetime.now()
            username=request.form['username']
            if username:
                user = db_session.query(User).filter_by(u_name=username).first()
                db_session.add(AIMessage(
                    a_user_id=user.u_id,
                    a_qtime=qtime,
                    a_atime=atime,
                    a_question=question,
                    a_answer=answer))
                db_session.commit()

        else:
            answer = f"Error: {response.code}, {response.message}"
    except Exception as e:
        answer = f'调用API时出错: {str(e)}'

    return jsonify({"text": answer})


@app.route('/fetchChatHistory', methods=['GET'])
def fetch_chat_history():
    username = request.args.get('username')
    user = db_session.query(User).filter_by(u_name=username).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    messages = db_session.query(AIMessage).filter_by(a_user_id=user.u_id).order_by(AIMessage.a_qtime.desc()).all()

    message_data = []
    for message in messages:
        message_data.append({
            "question": message.a_question,
            "answer": message.a_answer,
            "q_time": message.a_qtime,
            "a_time": message.a_atime
        })

    return jsonify(message_data)


@app.route('/deleteChatHistory', methods=['POST'])
def delete_chat_history():
    username = request.form.get('username')
    user = db_session.query(User).filter_by(u_name=username).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    db_session.query(AIMessage).filter_by(a_user_id=user.u_id).delete()
    db_session.commit()

    return jsonify({"message": "Chat history deleted successfully"})





if __name__ == "__main__":
    app.run(debug=True)



