# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock

from h.formatters.annotation_core import AnnotationCoreFormatter


class TestAnnotationCoreFormatter(object):

    def test_format(self, factories):
        ann = factories.Annotation(id='e22AJlHYQNCG70aXL7gr1w',
                                   groupid='abcd1234',
                                   tags=['food', 'poaceae'],
                                   text='Donkeys eat grass',
                                   target_uri='http://donkey.blog/grass.html',
                                   target_selectors=[{'type': 'TestSelector',
                                                      'foo': 'bar'}],
                                   userid='acct:donkey@example.com')
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationCoreFormatter()

        result = formatter.format(rsrc)

        assert result == {
            'id': 'e22AJlHYQNCG70aXL7gr1w',
            'group': 'abcd1234',
            'tags': ['food', 'poaceae'],
            'target': [{
                'source': 'http://donkey.blog/grass.html',
                'selector': [{'type': 'TestSelector',
                              'foo': 'bar'}],
            }],
            'text': 'Donkeys eat grass',
            'uri': 'http://donkey.blog/grass.html',
            'user': 'acct:donkey@example.com',
        }

    def test_format_null_fields(self, factories):
        ann = factories.Annotation(id='e22AJlHYQNCG70aXL7gr1w',
                                   groupid='abcd1234',
                                   tags=None,
                                   text=None,
                                   target_uri='http://donkey.blog/grass.html',
                                   target_selectors=None,
                                   userid='acct:donkey@example.com')
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationCoreFormatter()

        result = formatter.format(rsrc)

        assert result == {
            'id': 'e22AJlHYQNCG70aXL7gr1w',
            'group': 'abcd1234',
            'tags': [],
            'target': [{'source': 'http://donkey.blog/grass.html'}],
            'text': '',
            'uri': 'http://donkey.blog/grass.html',
            'user': 'acct:donkey@example.com',
        }

    def test_format_references(self, factories):
        ann = factories.Annotation(references=['NWLbqh-EEeeKchviwhAw5g',
                                               'YowHaBhuEeeHgRtyzPIREQ'])
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationCoreFormatter()

        result = formatter.format(rsrc)

        assert result['references'] == ['NWLbqh-EEeeKchviwhAw5g',
                                        'YowHaBhuEeeHgRtyzPIREQ']

    def test_preload(self):
        """Test that the preload method exists."""
        formatter = AnnotationCoreFormatter()
        formatter.preload(['a', 'b', 'c'])
