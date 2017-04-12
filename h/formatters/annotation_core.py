# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationCoreFormatter(object):
    """
    Formatter for annotation core fields.

    This formatter returns the annotation's core fields -- principally those
    for which we don't need to load any auxiliary data to render.
    """

    def preload(self, ids):
        pass

    def format(self, annotation_resource):
        annotation = annotation_resource.annotation

        result = {
            'group': annotation.groupid,
            'id': annotation.id,
            'tags': annotation.tags or [],
            'target': _target(annotation),
            'text': annotation.text or '',
            'uri': annotation.target_uri,
            'user': annotation.userid,
        }

        if annotation.references:
            result['references'] = annotation.references

        return result


def _target(annotation):
    target = {'source': annotation.target_uri}
    if annotation.target_selectors:
        target['selector'] = annotation.target_selectors
    return [target]
