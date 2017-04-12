# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationLinksFormatter(object):
    """
    Formatter for rendering a list of hypermedia links for an annoation.
    """

    def __init__(self, links_service):
        self.links_service = links_service

    def preload(self, ids):
        pass

    def format(self, annotation_resource):
        annotation = annotation_resource.annotation

        return {'links': self.links_service.get_all(annotation)}
