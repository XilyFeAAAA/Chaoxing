#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from app.models.chaoxing import Account, Course, CourseOrder, ChaoxingSetting, Log
from app.models.mail import Notification
from app.models.permission import Permission
from app.models.relation import RolePermission
from app.models.role import Role
from app.models.user import User, UserInfo

models = [User,
          UserInfo,
          RolePermission,
          Role,
          Permission,
          Account,
          Course,
          CourseOrder,
          ChaoxingSetting,
          Notification,
          Log]

model_dict = {}

for model in models:
    model_dict[model.__name__.lower()] = model
