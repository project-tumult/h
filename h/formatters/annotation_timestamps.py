# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter
from h.util.datetime import utc_iso8601


@implementer(IAnnotationFormatter)
class AnnotationTimestampsFormatter(object):
    """
    Formatter for annotation timestamp fields.

    This formatter returns the annotation's created/updated fields in an
    appropriate string format.
    """

    def preload(self, ids):
        pass

    def format(self, annotation_resource):
        annotation = annotation_resource.annotation

        return {
            'created': utc_iso8601(annotation.created),
            'updated': utc_iso8601(annotation.updated),
        }
