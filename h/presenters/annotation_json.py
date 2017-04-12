# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import copy

from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement

from h.formatters.interfaces import IAnnotationFormatter
from h.presenters.annotation_base import AnnotationBasePresenter


class AnnotationJSONPresenter(AnnotationBasePresenter):

    """Present an annotation in the JSON format returned by API requests."""

    def __init__(self, annotation_resource, formatters=None):
        super(AnnotationJSONPresenter, self).__init__(annotation_resource)

        self._formatters = []

        if formatters is not None:
            for formatter in formatters:
                self._add_formatter(formatter)

    def _add_formatter(self, formatter):
        try:
            verifyObject(IAnnotationFormatter, formatter)
        except DoesNotImplement:
            raise ValueError('formatter is not implementing IAnnotationFormatter interface')

        self._formatters.append(formatter)

    def asdict(self):
        annotation = copy.copy(self.annotation.extra) or {}

        for formatter in self._formatters:
            annotation.update(formatter.format(self.annotation_resource))

        return annotation
