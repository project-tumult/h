# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

import mock

from h.formatters.annotation_timestamps import AnnotationTimestampsFormatter


class TestAnnotationTimestampsFormatter(object):

    def test_format(self, factories):
        c = datetime.datetime(2017, 4, 12, 9, 17, 33, 788355)
        u = datetime.datetime(2017, 4, 12, 9, 20, 21, 120736)
        ann = factories.Annotation(created=c, updated=u)
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationTimestampsFormatter()

        result = formatter.format(rsrc)

        assert result == {
            'created': '2017-04-12T09:17:33.788355+00:00',
            'updated': '2017-04-12T09:20:21.120736+00:00',
        }

    def test_preload(self):
        """Test that the preload method exists."""
        formatter = AnnotationTimestampsFormatter()
        formatter.preload(['a', 'b', 'c'])
