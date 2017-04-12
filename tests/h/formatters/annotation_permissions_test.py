# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from pyramid import security
from pyramid.authorization import ACLAuthorizationPolicy

from h.formatters.annotation_permissions import AnnotationPermissionsFormatter


@pytest.mark.usefixtures('policy')
class TestAnnotationPermissionsFormatter(object):

    @pytest.mark.parametrize('shared,group_world_readable,expected_read_principal', [
        # Unshared annotations are always only readable by their owner.
        (False, False, 'acct:luke'),
        (False, True, 'acct:luke'),

        # Shared annotations are readable by their group...
        (True, False, 'group:abcd1234'),

        # ...unless the group is world-readable, in which case they're
        # readable by everyone.
        (True, True, 'group:__world__'),
    ])
    def test_format(
        self,
        factories,
        group_world_readable,
        shared,
        expected_read_principal,
    ):
        ann = factories.Annotation(userid='acct:luke',
                                   groupid='abcd1234',
                                   shared=shared)
        rsrc = mock.Mock(spec_set=['annotation', '__acl__'], annotation=ann)
        if group_world_readable:
            rsrc.__acl__ = [(security.Allow, security.Everyone, 'read')]
        else:
            rsrc.__acl__ = [security.DENY_ALL]
        formatter = AnnotationPermissionsFormatter()

        result = formatter.format(rsrc)

        assert result == {
            'permissions': {
                'read': [expected_read_principal],
                'admin': ['acct:luke'],
                'update': ['acct:luke'],
                'delete': ['acct:luke'],
            }
        }

    def test_preload(self):
        """Test that the preload method exists."""
        formatter = AnnotationPermissionsFormatter()
        formatter.preload(['a', 'b', 'c'])

    @pytest.fixture
    def policy(self, pyramid_config):
        """Set up a fake authentication policy with a real ACL authorization policy."""
        policy = ACLAuthorizationPolicy()
        pyramid_config.testing_securitypolicy(None)
        pyramid_config.set_authorization_policy(policy)
