#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime

from sigmago.corelib.ext import db
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin(db.Model):
    """A mixin class to record the model's created, updated timestamp."""

    created = db.Column("created", db.DateTime, nullable=False,
                        default=datetime.datetime.utcnow)
    updated = db.Column("updated", db.DateTime, nullable=False,
                        default=datetime.datetime.utcnow)

    __abstract__ = True
    __mapper_args__ = {'order_by': created.desc()}

    @db.validates("updated")
    def validate_to_update_timestamp(self, key, value):
        return datetime.datetime.utcnow()


class BaseComment(TimestampMixin, db.Model):
    """The base class of the comment model."""

    __abstract__ = True
    __commentable__ = {'owner_id': None, 'subject_id': None,
                       'subject_class': None, 'owner_class': None}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    content = db.Column(db.Text, nullable=False)

    @declared_attr
    def owner_id(cls):
        owner_pk = cls.__commentable__['owner_id']
        return db.Column(db.ForeignKey(owner_pk), nullable=False)

    @declared_attr
    def subject_id(cls):
        subject_pk = cls.__commentable__['subject_id']
        return db.Column(db.ForeignKey(subject_pk), nullable=False)

    @declared_attr
    def owner(cls):
        owner_class = cls.__commentable__['owner_class']
        return db.relationship(owner_class, lazy="joined", uselist=False)

    @declared_attr
    def __tablename__(cls):
        subject_class = cls.__commentable__['subject_class']
        return "%s_comment" % subject_class.__tablename__


class CommentableMixin(db.Model):
    """A mixin class to make subject could be commented.

    Example:
    >>> class Subject(mixins.comment.Commentable, db.Model):
    ...     subject_id = db.Column(db.Ingeger, primary_key=True)
    ...
    ...     __commentable__ = {'owner_class': User, 'owner_id': User.id,
                'subject_id': subject_id}
    >>>
    >>> subject = Subject()
    >>> comment = subject.add_comment("My first comment.", current_user())
    >>>
    >>> comment in subject.comments
    True
    """

    __abstract__ = True
    __commentable__ = {'owner_class': None, 'owner_id': None,
                       'subject_id': None}

    @declared_attr
    def comments(cls):
        #: make the meta data of the subject class
        arguments = dict(cls.__commentable__)
        arguments['subject_class'] = cls

        #: create a comment class
        class_name = "%sComment" % cls.__name__
        class_bases = (BaseComment,)
        class_members = {'__commentable__': arguments}
        comment_class = type(class_name, class_bases, class_members)
        comment_class.__doc__ = "The comment of the %s." % class_name

        #: assign the comment class to the subject class
        setattr(cls, class_name, comment_class)
        setattr(cls, "comment_class", comment_class)

        #: create and return the relationship to the comment
        backref = db.backref("subject", lazy="joined", uselist=False)
        return db.relationship(comment_class, lazy="dynamic", backref=backref)

    def post_comment(self, content, owner):
        model = self.comment_class(subject=self, owner=owner, content=content)
        self.comments.append(model)
        return model
