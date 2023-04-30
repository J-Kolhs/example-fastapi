from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

    owner = relationship("User")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key = True, nullable = False)
    meeting_name = Column(String, nullable = False)
    meeting_start = Column(TIMESTAMP(timezone = True), nullable = False)
    meeting_end = Column(TIMESTAMP(timezone = True), nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable = False)

    owner = relationship("User")
    room = relationship("Room")

    __table_args__ = (
        CheckConstraint("meeting_start < meeting_end", name="meetingStart_before_meetingEnd"),
    )

class User(Base):
    __tablename__ = "users"

    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    roles = Column(String, nullable = False, server_default='BASIC')
    first_name = Column(String, nullable = False, server_default='None')
    last_name = Column(String, nullable = False, server_default='None')
    company_id = Column(Integer, ForeignKey("companies.id", ondelete= "CASCADE"), nullable = False)
    is_verified = Column(Boolean, nullable = False, server_default = text('false'))

    access = relationship("Access", back_populates="user")
    companies = relationship("Companies")

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True, nullable = False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True, nullable = False)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key = True, nullable = False)
    room_name = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"),nullable = False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete = "CASCADE"),nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

    room = relationship("Room")
    user = relationship("User", back_populates="access")

class Companies(Base):
    __tablename__ = "companies"

    id = Column(Integer(),primary_key = True, nullable = False)
    companies_name = Column(String(), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), server_default=text('now()'), nullable = False)