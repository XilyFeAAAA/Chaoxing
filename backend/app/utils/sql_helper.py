#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import select, Select, func
from sqlalchemy.orm import InstrumentedAttribute

# local
from app.core.db import Base
from app.schemas.request import PaginationIn
from app.models import model_dict, CourseOrder

"""
keyword = {
    'role.name': 'sa'
}
要join的是user对应的User, 要filter的是Role.name == 'sa' 
keyword = {
    'name__contains': 's'
}
要filter的是User.name.like('%s%')
"""


def add_filter(query: Select, _model: Base, keyword: dict) -> Select:

    def add_join():
        nonlocal query
        for model_chain in join_models:
            cnt_model = _model
            for chain in model_chain:
                if hasattr(cnt_model, chain) and isinstance(next_model := getattr(cnt_model, chain), InstrumentedAttribute):
                    cnt_model = next_model
            query = query.join(cnt_model)
        return query

    join_models = set()  # Use a set to avoid duplicates
    for _attr, value in keyword.items():
        if isinstance(value, str) and not value.strip():
            continue
        # Check for fuzzy query
        attr = _attr.removesuffix("__contains")
        model = _model
        # Check for join operation
        if len(parts := attr.split('.')) > 1:  # Check for join operation
            join_models.add(tuple(parts[:-1]))
            model, attr = model_dict[parts[-2]], parts[-1]
        if hasattr(model, attr) and isinstance(getattr(model, attr), InstrumentedAttribute):
            query = query.filter(getattr(model, attr).like(f"%{value}%")) if _attr.endswith("__contains") else query.filter(getattr(model, attr) == value)

    return add_join()


def patch_query(model: Base, pagination: PaginationIn) -> Select:
    query = select(model).offset(pagination.cursor * pagination.limit).limit(pagination.limit)
    return add_filter(query, model, pagination.keyword)


def patch_count(model: Base, pagination: PaginationIn) -> Select:
    query = select(func.count(model.id))
    return add_filter(query, model, pagination.keyword)


"""
class Order:
    user: User
    
class User:
    info: UserInfo
    
class UserInfo:
    name: str

select(Order).join(User).join(UserInfo).filter(UserInfo.name == 'sa')
"""