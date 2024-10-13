from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory,abort,jsonify
import pymysql
import hashlib
import sqlalchemy
from sqlalchemy import insert
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Column, Enum,Integer,Table, String, ForeignKey, DateTime,Text,Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from flask import render_template #引入模板插件
from sqlalchemy.testing import db
from flask_mail import Mail, Message
import random
import os
from flask_cors import CORS



app = Flask(__name__,
static_folder='./public/static',  #设置静态文件夹目录
template_folder = "./public/templates")  #设置vue编译输出目录dist文件夹，为Flask模板文件目录
app.secret_key = '123456789'

CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    'password':'20040616',#这里改成自己的数据库密码
    'host':'localhost',
    'port':3306,
    'database': 'forest',#这里改成自己的数据库名字
    'charset':'utf8mb4'}
# 创建数据库连接
engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'.format(**db_config))

Base = declarative_base()


class user_participate_activity(Base):
    __tablename__ = 'user_participate_activity'
    upa_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 唯一标识
    participateNumber = Column(Integer, nullable=False)  # 此次报名活动人数
    note = Column(String(100), default="")  # 备注
    user_id = Column(Integer, ForeignKey('users.u_id'))
    activity_id = Column(Integer, ForeignKey('activities.a_id'))


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
    a_type = Column(Enum("伐木", "采摘", "旅游参观", "野营", "捕猎"), nullable=False)  # 活动类型
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
    a_approver_id = Column(Integer, ForeignKey('users.u_id'),nullable=True) #审批人id
    a_approveTime = Column(DateTime, nullable=True)  # 活动审批时间
    a_dismissreason = Column(String(100), nullable=True) #驳回理由





# 这是删除所有数据的操作，不到万不得已千万不要做
# 如果之前创建过同名数据库且不明白如何数据库迁移，可以把下面一句注释去掉，运行清除之前的表并创建新表，然后记得加上注释
#Base.metadata.drop_all(engine)

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
            return jsonify({'status': 'fail', 'message': error})
        existing_user = db_session.query(User).filter_by(u_name=username).first()
        if existing_user:
            error = "用户名已存在"
            return jsonify({'status': 'fail', 'message': error})
        existing_email = db_session.query(User).filter_by(u_email=email).first()
        if existing_email:
            error = "该邮箱已被注册"
            return jsonify({'status': 'fail', 'message': error})
        
        # 错误排除后创建新用户
        new_user = User(u_name=username, u_password=password, u_email=email)
        db_session.add(new_user)
        db_session.commit()

        success = "注册成功，请登录"
        return jsonify({'status': 'success', 'message': success})
    else:
        error = "请求错误"
        return jsonify({'status': 'fail', 'message': error})

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
            success='欢迎来到林上鹰眼！'
            return jsonify({'status': 'success', 'message': success})
        else:
            error='登录失败，邮箱或密码错误'
            return jsonify({'status': 'fail', 'message': error})
    else:
        error = "请求错误"
        return jsonify({'status': 'fail', 'message': error})

#注销
@app.route('/logoff')
def logoff():
    session.clear()
    flash('您已成功注销', 'success')
    return redirect(url_for('login'))

#退出登录
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

#林业活动界面
@app.route('/activity')
def activity():
    username = session.get('username')  # 从会话中获取用户名
    if not username:
        return redirect(url_for('login'))  # 如果没有用户名信息，重定向到登录页面

    # 根据用户名查询用户角色
    user = db_session.query(User).filter_by(u_name=username).first()
    if user:
        u_role = user.u_role
    else:
        flash('用户不存在或已被删除', 'error')
        return redirect(url_for('login'))
    #传递当前用户角色给前端，根据不同角色显示不同的按钮
    return render_template('activity.html', u_role=u_role)

#我的申请界面，显示当前用户已申请的活动
@app.route('/apply')
def apply():
    if 'username' in session:
        # 获取当前用户的申请中或已通过的活动
        username = session.get('username')  # 从会话中获取用户名
        user = db_session.query(User).filter_by(u_name=username).first()
        if user:
            u_id = user.u_id
        approving_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id,
                                                                 Activity.a_state == 'approving').all()
        approved_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id,
                                                                Activity.a_state == 'approved').all()
        dismissed_activities = db_session.query(Activity).filter(Activity.a_applicantId == u_id,
                                                                 Activity.a_state == 'dismissed').all()

        return render_template('apply.html',approving_activities=approving_activities, approved_activities=approved_activities, dismissed_activities=dismissed_activities)
    return redirect(url_for('index'))



#创建活动
@app.route('/create_activity', methods=['GET', 'POST'])
def create_activity():

    if request.method == 'POST':
        # 从表单中获取数据
        a_name = request.form['a_name']
        a_location = request.form['a_location']
        a_beginTime = request.form['a_beginTime']
        a_endTime = request.form['a_endTime']
        a_participantNumber = request.form['a_participantNumber']
        a_introduction = request.form['a_introduction']
        a_forest =request.form['a_forest']
        a_type = request.form['a_type']
        a_ableParticipate = request.form.get('a_ableParticipate') is not None

        # 处理文件上传
        a_picPath = request.files['a_picPath']
        if a_picPath:
            filename = secure_filename(a_picPath.filename)
            a_picPath.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 根据用户名查询用户
        username = session.get('username')  # 从会话中获取用户名
        user = db_session.query(User).filter_by(u_name=username).first()
        if user:
            u_id = user.u_id
        # 创建新的 Activity 实例
        new_activity = Activity(
            a_applicantId=u_id,
            a_name=a_name,
            a_location=a_location,
            a_beginTime=datetime.strptime(a_beginTime, '%Y-%m-%dT%H:%M'),
            a_endTime=datetime.strptime(a_endTime, '%Y-%m-%dT%H:%M'),
            a_participantNumber=int(a_participantNumber),
            a_introduction=a_introduction,
            a_picPath=filename,
            a_ableParticipate=a_ableParticipate,
            a_type = a_type,
            a_forest=a_forest,
            a_state="approving"  # 默认状态为待审批
        )

        # 将新活动添加到数据库会话并提交
        db_session.add(new_activity)
        db_session.commit()

        flash('活动创建成功，等待审批', 'success')
        return redirect(url_for('activity'))

    return render_template('create_activity.html')

#活动详情页，申请人和审批人公用界面，但是会传递一个is_approver参数决定前端是否显示“同意”“驳回”
@app.route('/activity_detail/<int:activity_id>')
def activity_detail(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if not activity:
        flash('活动不存在', 'error')
        return redirect(url_for('activity'))

    username = session.get('username')  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    current_user_role = user.u_role
    # 判断当前用户是否为审批人
    is_approver = current_user_role == '林业管理人员'
    return render_template('activity_detail.html', activity=activity,is_approver=is_approver)


#申请人删除所申请的活动
@app.route('/delete_activity/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):

    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if activity:
        db_session.delete(activity)
        db_session.commit()
        flash('活动删除成功', 'success')
    else:
        flash('活动不存在或已被删除', 'error')

    return redirect(url_for('apply'))

#我的审批界面
@app.route('/approve')
def approve():
    # 假设当前管理员的森林名称存储在session中
    username = session.get('username')  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    current_forest = user.u_forest

    if not current_forest:
        flash('您尚未登录或没有权限访问此页面', 'error')
        return redirect(url_for('login'))

    # 根据当前管理员的森林名称和状态查询活动
    approving_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest,
                                                             Activity.a_state == 'approving').all()
    approved_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest,
                                                            Activity.a_state == 'approved').all()
    dismissed_activities = db_session.query(Activity).filter(Activity.a_forest == current_forest,
                                                             Activity.a_state == 'dismissed').all()

    # 渲染模板并传递活动列表,传递用户的角色是因为在活动详情页时如果为审批人会添加审批通过或驳回按钮
    return render_template('approve.html', approving_activities=approving_activities,
                           approved_activities=approved_activities, dismissed_activities=dismissed_activities)


#审批通过
@app.route('/approve_activity/<int:activity_id>', methods=['POST'])
def approve_activity(activity_id):
    # 审批活动逻辑
    # 更新活动状态为 'approved'
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    #获取当前审批人的id
    username = session.get('username')  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    #修改状态
    activity.a_state= 'approved'
    #存储审批人的id
    activity.a_approver_id = user.u_id
    #存储审批时间
    activity.a_approveTime = datetime.now()

    return redirect(url_for('approve'))


#审批驳回
@app.route('/dismiss_activity/<int:activity_id>', methods=['POST'])
def dismiss_activity(activity_id):
    dismiss_reason = request.form.get('dismiss_reason', '')
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    #获取当前审批人的id
    username = session.get('username')  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    #修改状态
    activity.a_state = 'dismissed'
    #存储审批人的id
    activity.a_approver_id = user.u_id
    #存储审批时间
    activity.a_approveTime = datetime.now()
    #存储驳回理由
    activity.a_dismissreason = dismiss_reason
    return redirect(url_for('approve'))

# 活动风采界面
@app.route('/activities')
def activities():
    #筛选面向大众且截止时间晚于当前时间且审批通过的活动
    # 获取当前时间
    now = datetime.now()
    activities = db_session.query(Activity).filter(Activity.a_ableParticipate == True, Activity.a_endTime > now,Activity.a_state=='approved').all()
    return render_template('activities.html', activities=activities)

#报名活动界面
@app.route('/activity_enroll/<int:activity_id>',methods=['GET'])
def activity_enroll(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if activity:
        return render_template('activity_enroll.html', activity=activity)
    else:
        flash('活动不存在或已结束', 'error')
        return redirect(url_for('activities'))


#点击报名后
@app.route('/enroll/<int:activity_id>', methods=['POST'])
def enroll(activity_id):
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    if not activity or not activity.a_ableParticipate or activity.a_endTime <= datetime.now():
        flash('活动不可报名或已结束', 'error')
        return redirect(url_for('activities'))

    participant_number = request.form['participantNumber']
    remark = request.form.get('remark', '')  # 获取备注信息，默认为空字符串
    if int(participant_number) > (activity.a_participantNumber - activity.a_enrolledNumber):
        flash('报名人数超过剩余名额', 'error')
        return redirect(url_for('activity_enroll', activity_id=activity_id))

    # 获取用户id
    username = session.get('username')  # 从会话中获取用户名
    user_id = db_session.query(User).filter_by(u_name=username).first().u_id
    # 创建用户和活动的联系
    activity.a_enrolledNumber += int(participant_number)
    new_participant = user_participate_activity(
        participateNumber =  participant_number,
        note =  remark,
        user_id=user_id,
        activity_id=activity_id,
    )
    db_session.add(new_participant)
    db_session.commit()
    flash('报名成功', 'success')
    return redirect(url_for('activities'))


#我的报名界面
@app.route('/myenrolled')
def myenrolled():
    username = session.get('username')  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    if user:
        woos= db_session.query(user_participate_activity).filter_by(user_id=user.u_id).all()
        # 从每个记录中提取 activity_id，并将其存储在列表中
        activity_ids = [woo.activity_id for woo in woos]
    else:
        flash('找不到用户', 'error')
        return redirect(url_for('login'))
    participations= db_session.query(Activity).filter(Activity.a_id.in_(activity_ids)).all()

    return render_template('myenrolled.html', participations=participations)

#普通用户取消报名
@app.route('/cancel_enrollment/<int:activity_id>', methods=['POST'])
def cancel_enrollment(activity_id):
    username = session.get('username')  # 从会话中获取用户名
    user = db_session.query(User).filter_by(u_name=username).first()
    if not user:
        flash('您尚未登录或没有权限执行此操作', 'error')
        return redirect(url_for('login'))

    # 查询
    participation = db_session.query(user_participate_activity).filter_by(user_id=user.u_id, activity_id=activity_id).first()
    activity = db_session.query(Activity).filter_by(a_id=activity_id).first()
    activity.a_enrolledNumber -= participation.participateNumber
    if participation:
        db_session.delete(participation)
        db_session.commit()
        flash('取消报名成功', 'success')
    else:
        flash('取消报名失败，可能您已取消报名或不存在此活动', 'error')

    return redirect(url_for('myenrolled'))

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)