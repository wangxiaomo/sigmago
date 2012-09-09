#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import datetime
import contextlib

from sigmago.corelib.ext import db
from sigmago.corelib.models import (TimestampMixin, CommentableMixin,
                                    BaseComment)
from tests import SigmagoTestCase


class TimestampMixinTestCase(SigmagoTestCase):
    """Test the timestamp mixin class."""

    class TimeInterval(object):
        """A interval object to record start time and end time."""

        def __init__(self):
            self.start_time = None
            self.end_time = None

        def is_valid(self):
            return self.start_time and self.end_time

    class BlogPost(TimestampMixin, db.Model):
        """A mock class for testing TimestampMixin."""

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String)

    def test_created_time(self):
        with self.time_interval() as interval:
            model = self.make_blog_post()
        self.assert_time_in_interval(model.created, interval)
        self.assert_time_in_interval(model.updated, interval)

    def test_updated_time(self):
        model = self.make_blog_post()
        old_created = model.created
        old_updated = model.updated

        time.sleep(0.1)

        with self.time_interval() as interval:
            model.title = "NEW TEST"
            db.session.commit()

        self.assertNotEqual(model.updated, old_updated)
        self.assertEqual(model.created, old_created)
        self.assert_time_in_interval(model.updated, interval)

    def make_blog_post(self, **kwargs):
        """Creates a blog post model and stores it into database."""
        model = self.BlogPost(title="TEST")
        db.session.add(model)
        db.session.commit()
        return model

    @contextlib.contextmanager
    def time_interval(self):
        """Make a context to record the start time and end time."""
        interval = self.TimeInterval()
        interval.start_time = datetime.datetime.utcnow()
        yield interval
        interval.end_time = datetime.datetime.utcnow()

    def assert_time_in_interval(self, time, interval):
        """Asserts a datetime is in a expect time interval."""
        self.assertTrue(interval.is_valid(), "time interval is not prepared.")
        self.assertGreaterEqual(time, interval.start_time)
        self.assertLessEqual(time, interval.end_time)


class CommentableMixinTestCase(SigmagoTestCase):
    """Test the commentable mixin class."""

    class CommentablePost(CommentableMixin, db.Model):
        """A mock class for testing CommentableMixin."""

        class CommentUser(db.Model):
            """A mock class for testing CommentableMixin."""

            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String)

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String)

        __commentable__ = {'owner_class': CommentUser,
                           'owner_id': CommentUser.id,
                           'subject_id': id}

    def make_commentable_post(self, title):
        model = self.CommentablePost(title=title)
        return model

    def test_meta(self):
        """Test the meta data generating of mixed class."""
        model = self.make_commentable_post("TITLE")
        self.assertTrue(issubclass(model.comment_class, BaseComment))

    def test_post_comment(self):
        """Test to post a comment."""
        #: create models
        model = self.make_commentable_post("TITLE")
        user = self.CommentablePost.CommentUser(name="tonyseek")
        #: post it
        comment = model.post_comment("aha", user)
        #: store into db
        db.session.add(model)
        db.session.commit()
        #: check data
        self.assertEqual(model.title, "TITLE")
        self.assertEqual(model.comments.count(), 1)
        self.assertIs(comment, model.comments.first())
        self.assertEqual(comment.content, "aha")
