# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationDocumentFormatter(object):
    """
    Formatter for the  annotation document field.

    This formatter renders some limited metadata about the annotation's
    associated "document" into the document field.
    """

    def preload(self, ids):
        pass

    def format(self, annotation_resource):
        annotation = annotation_resource.annotation

        if not annotation.document:
            return {'document': {}}

        if not annotation.document.title:
            return {'document': {}}

        return {'document': {'title': [annotation.document.title]}}
