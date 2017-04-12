# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock

from h.formatters.annotation_document import AnnotationDocumentFormatter


class TestAnnotationDocumentFormatter(object):

    def test_format(self, factories):
        ann = factories.Annotation()
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationDocumentFormatter()

        result = formatter.format(rsrc)

        assert result == {
            'document': {'title': [ann.document.title]},
        }

    def test_format_no_document(self, factories):
        ann = factories.Annotation()
        ann.document = None
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationDocumentFormatter()

        result = formatter.format(rsrc)

        assert result == {'document': {}}

    def test_format_no_document_title(self, factories):
        ann = factories.Annotation()
        ann.document.title = None
        rsrc = mock.Mock(spec_set=['annotation'], annotation=ann)
        formatter = AnnotationDocumentFormatter()

        result = formatter.format(rsrc)

        assert result == {'document': {}}

    def test_preload(self):
        """Test that the preload method exists."""
        formatter = AnnotationDocumentFormatter()
        formatter.preload(['a', 'b', 'c'])
