# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid.security import Everyone, principals_allowed_by_permission
from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter


@implementer(IAnnotationFormatter)
class AnnotationPermissionsFormatter(object):
    """
    Formatter for annotation permissions.

    This formatter returns the 'permissions' object for rendered annotations.
    """

    def preload(self, ids):
        pass

    def format(self, annotation_resource):
        return {'permissions': self._permissions(annotation_resource)}

    def _permissions(self, annotation_resource):
        """
        Return a permissions dict for the given annotation.

        Converts our simple internal annotation storage format into the legacy
        complex permissions dict format that is still used in some places.
        """
        annotation = annotation_resource.annotation
        read = annotation.userid

        if annotation.shared:
            read = 'group:{}'.format(annotation.groupid)

            principals = principals_allowed_by_permission(annotation_resource, 'read')
            if Everyone in principals:
                read = 'group:__world__'

        return {'read': [read],
                'admin': [annotation.userid],
                'update': [annotation.userid],
                'delete': [annotation.userid]}
