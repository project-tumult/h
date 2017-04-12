# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from h.formatters.annotation_links import AnnotationLinksFormatter
from h.services.links import LinksService


class TestAnnotationLinksFormatter(object):

    def test_format(self, links_service):
        rsrc = mock.Mock(spec_set=['annotation'], annotation=mock.sentinel.ann)
        formatter = AnnotationLinksFormatter(links_service)

        result = formatter.format(rsrc)

        assert result == {
            'links': {
                'hippo': 'http://hippo.com/happiness',
                'giraffe': 'http://giraffe.com/myneckhurts',
            }
        }

    def test_passes_annotation_to_links_service(self, links_service):
        rsrc = mock.Mock(spec_set=['annotation'], annotation=mock.sentinel.ann)
        formatter = AnnotationLinksFormatter(links_service)

        formatter.format(rsrc)

        links_service.get_all.assert_called_once_with(mock.sentinel.ann)

    def test_preload(self, links_service):
        """Test that the preload method exists."""
        formatter = AnnotationLinksFormatter(links_service)
        formatter.preload(['a', 'b', 'c'])

    @pytest.fixture
    def links_service(self):
        service = mock.Mock(spec_set=LinksService(base_url='http://example.com',
                                                  registry={}))
        service.get_all.return_value = {
            'hippo': 'http://hippo.com/happiness',
            'giraffe': 'http://giraffe.com/myneckhurts',
        }
        return service
