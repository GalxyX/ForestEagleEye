from flask import Flask
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    datetime,
    relationship,
    Table,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import declarative_base

engine = create_engine()
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

    u_submitTips = relationship()  # 提交的建议与举报
    u_approveTips = relationship()  # 审批的建议与举报
    u_post = relationship()  # 发布的帖子
    u_comments = relationship()  # 评论
    u_likes = relationship()  # 点赞的帖子
    u_question = relationship()  # 存小林问答问过的问题及回答


# 活动表
class Activity(Base):
    __tablename__ = "activities"
    a_id = Column(Integer, primary_key=True, nullable=False, unique=True)  # 活动编号
    a_applicantId = Column(Integer, ForeignKey("users.u_id"), nullable=False)  # 申请人id
    a_submitTime = Column(DateTime, nullable=False, default=datetime.now)  # 申请提交时间
    a_attachment = Column(String(100), default="")  # 申请附件
    a_name = Column(String(100), nullable=False)  # 活动名称
    a_type = Column(Enum("", "", "", "", ""), nullable=False)  # 活动类型
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