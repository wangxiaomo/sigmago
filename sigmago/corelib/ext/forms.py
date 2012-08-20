#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask.ext.wtf
import flask.ext.wtf.form
import wtforms.ext.i18n.form
from flask.ext.babel import lazy_gettext as _


__all__ = ("Form", "unique")


# ---------
# Base Form
# ---------

class Form(flask.ext.wtf.Form, wtforms.ext.i18n.form.Form):
    """Mixed the secret form and the i18n form."""
    pass


# ----------
# Validators
# ----------

def unique(model_class, column):
    """A validator to ensure the record is unique in the database."""
    def validate_unique(form, field):
        if model_class.query.filter(column == field.data).count() == 0:
            return True
        message = _(u"The %(field)s has been used.", field=field.label.text)
        raise flask.ext.wtf.ValidationError(message)
    return validate_unique
