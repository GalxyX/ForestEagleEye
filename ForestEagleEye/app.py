from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory,abort,jsonify
import pymysql
import hashlib
import sqlalchemy
from sqlalchemy import create_engine, Column, Enum,Integer,Table, String, ForeignKey, DateTime,Text,Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from flask import render_template #引入模板插件
from sqlalchemy.testing import db
from flask_mail import Mail, Message
import random

app = Flask(__name__,
static_folder='./public/static',  #设置静态文件夹目录
template_folder = "./public/templates")  #设置vue编译输出目录dist文件夹，为Flask模板文件目录
app.secret_key = '123456789'

app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮件服务器
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '3327903803@qq.com'  # 邮箱
app.config['MAIL_PASSWORD'] = 'xyjtyyhunuurdadj'  # 邮箱授权码
app.config['MAIL_DEFAULT_SENDER'] = '3327903803@qq.com'  # 邮箱

mail = Mail(app)
verification_codes = {}  # 存储邮箱和验证码的字典

# MySQL 数据库连接配置
db_config={
    'user':'root',
    'password':'hxyym123',#这里改成自己的数据库密码
    'host':'localhost',
    'port':3306,
    'database': 'forest',#这里改成自己的数据库名字
    'charset':'utf8mb4'}
# 创建数据库连接
engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'.format(**db_config))

Base = declarative_base()

user_participate_activity = Table(
    "user_participate_activity",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.u_id")),
    Column("activity_id", Integer, ForeignKey("activities.a_id")),
)


# 用户表
class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 唯一标识
    u_name = Column(String(100), nullable=False, unique=True)  # 用户昵称
    u_telphone = Column(String(15), unique=True)  # 联系电话
    u_password = Column(String(100), nullable=False)  # 用户密码
    u_email = Column(String(50), nullable=False, unique=True)  # 邮箱
    u_role = Column(Enum("普通用户", "林业从业人员", "林业管理人员", "环境管理人员", "林业监管人员"), nullable=False, default="普通用户")  # 用户所属角色（普通用户、林业从业人员、林业管理人员、环境管理人员、林业局监管人员）
    u_forest = Column(String(100))  # 所属森林（林业管理人员、环境管理人员、林业局监管人员需要选择）
    u_avatarPath = Column(String(100), nullable=False, default="")  # 头像图片路径    ###############需修改default处准备一默认头像
    u_signature = Column(String(100), default="")  # 个性签名
    u_signupTime = Column(DateTime, nullable=False, default=datetime.now)  # 注册时间
    u_newestTime = Column(DateTime, nullable=False, onupdate=datetime.now, default=datetime.now)  # 最近登录时间

    # 联系集
    u_participateActivity = relationship("Activity", secondary=user_participate_activity, back_populates="a_participants")  # 报名参加的活动
    u_applyActivities = relationship("Activity", backref="applicant")  # 申请的活动
    u_approveActivity = relationship("ApprovalProcess", backref="approver")  # 审批的活动

    #u_submitTips = relationship()  # 提交的建议与举报
    #u_approveTips = relationship()  # 审批的建议与举报
    #u_post = relationship()  # 发布的帖子
    #u_comments = relationship()  # 评论
    #u_likes = relationship()  # 点赞的帖子
    #u_question = relationship()  # 存小林问答问过的问题及回答


# 活动表
class Activity(Base):
    __tablename__ = "activities"
    a_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 活动编号
    a_applicantId = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 申请人id
    a_submitTime = Column(DateTime, nullable=False, default=datetime.now)  # 申请提交时间
    a_attachment = Column(String(100), default="")  # 申请附件
    a_name = Column(String(100), nullable=False)  # 活动名称
    # a_type = Column(Enum("", "", "", "", ""), nullable=False)  # 活动类型
    a_forest = Column(String(100), nullable=False)  # 审批单位（森林名称）
    a_location = Column(String(100), nullable=False)  # 活动地点（具体地点）
    a_beginTime = Column(DateTime, nullable=False)  # 活动开始时间
    a_endTime = Column(DateTime, nullable=False)  # 活动结束时间
    a_introduction = Column(String(1000), nullable=False)  # 活动简介
    a_picPath = Column(String(100), default="")  # 活动图片路径
    a_ableParticipate = Column(Boolean, nullable=False)  # 活动是否面向大众（大众可以报名参加）
    a_participantNumber = Column(Integer, nullable=False)  # 活动人数
    a_state = Column(Enum("approving", "approved", "dismissed", "ongoing", "ended"), nullable=False, default="approving")  # 状态（待审批、通过、驳回、活动开始、活动完成）

    # 联系集
    a_participants = relationship("User", secondary=user_participate_activity, back_populates="u_participateActivity")  # 报名参加的人
    a_approvalProcessId = relationship("ApprovalProcess", backref="activities")  # 审批的所有结点编号


# 审批流结点
class ApprovalProcess(Base):
    __tablename__ = "approvalprocesses"
    p_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    p_lastId = Column(Integer, nullable=False)  # 上一个审批结点  ## null表示为第一个审批结点
    p_activityId = Column(Integer, ForeignKey("activities.a_id"), nullable=False)  # 本结点对应的活动
    p_approverId = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 本结点上的审批者
    a_submitTime = Column(DateTime, nullable=False, default=datetime.now)  # 本次审批提交时间
    a_approveTime = Column(DateTime)  # 本次审批审批时间
    p_result = Column(Enum("approved", "dismissed"), nullable=False)  # 审批意见（通过、驳回）
    p_notes = Column(String(1000))  # 审批理由

Base.metadata.create_all(engine)

db_session_class = sessionmaker(bind=engine)
db_session = db_session_class()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_verification_code():
    return str(random.randint(100000, 999999))

@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.form['email']
    code = generate_verification_code()
    verification_codes[email] = code
    msg = Message('欢迎来到林上鹰眼', recipients=[email])
    msg.body = f'您的验证码为 {code}'
    try:
        mail.send(msg)
        return jsonify({'status': 'success', 'message': '验证码已发送到您的邮箱'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': '发送邮件失败，请检查邮箱输入是否有误'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        code = request.form['code']
        if email not in verification_codes or verification_codes[email] != code:
            error = "验证码错误"
            flash("验证码错误", 'error')
            return render_template('register.html', error=error)
        existing_user = db_session.query(User).filter_by(u_name=username).first()
        if existing_user:
            error = "用户名已存在"
            flash("用户名已存在", 'error')
            return render_template('register.html', error=error)
        existing_email = db_session.query(User).filter_by(u_email=email).first()
        if existing_email:
            error = "该邮箱已被注册"
            flash("该邮箱已被注册", 'error')
            return render_template('register.html', error=error)
        new_user = User(u_name=username, u_password=password, u_email=email)
        db_session.add(new_user)
        db_session.commit()
        success = "注册成功，请登录"
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        user = db_session.query(User).filter_by(u_email=email, u_password=password).first()
        if user:
            session['username'] = user.u_name
            session['user_id'] = user.u_id
            session['role'] = user.u_role
            flash('登录成功', 'success')
            return redirect(url_for("index"))
        else:
            error = "邮箱或密码错误"
            flash('登录失败，请检查邮箱和密码', 'error')
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('您已成功注销', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()