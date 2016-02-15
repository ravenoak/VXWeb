'''
Created on Jul 29, 2011

@author: ravenoak
'''

from vxweb.model import DeclarativeBase
from vxweb.model.auth import User
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Unicode, DateTime, String


class AuditLog(DeclarativeBase):
    __tablename__ = 'audit_log'
    id = Column(Integer(), primary_key = True)
    datetime = Column(DateTime(), nullable = False)
    user = relationship(User(), backref = 'audit', order_by = datetime)
    log = Column(Unicode(), nullable = False)
    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
