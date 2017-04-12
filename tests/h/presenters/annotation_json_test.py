# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from zope.interface import implementer

from h.formatters.interfaces import IAnnotationFormatter
from h.presenters.annotation_json import AnnotationJSONPresenter
from h.resources import AnnotationResource


@implementer(IAnnotationFormatter)
class FakeFormatter(object):
    def __init__(self, data=None):
        self.data = data or {}

    def preload(self, ids):
        pass

    def format(self, annotation):
        return self.data


@implementer(IAnnotationFormatter)
class IDDuplicatingFormatter(object):
    """This formatter take the annotation's ID and adds it in another key.

    The main purpose of it is to confirm that the presenter is passing in the
    AnnotationResource object.
    """

    def preload(self, ids):
        pass

    def format(self, annotation_resource):
        return {'duplicated-id': annotation_resource.annotation.id}


class TestAnnotationJSONPresenter(object):
    def test_asdict(self, document_asdict, group_service, fake_links_service):
        ann = mock.Mock(extra={'extra-1': 'foo', 'extra-2': 'bar'})
        resource = AnnotationResource(ann, group_service, fake_links_service)

        document_asdict.return_value = {'foo': 'bar'}

        expected = {'document': {'foo': 'bar'},
                    'links': {'giraffe': 'http://giraffe.com',
                              'toad': 'http://toad.net'},
                    'extra-1': 'foo',
                    'extra-2': 'bar'}

        result = AnnotationJSONPresenter(resource).asdict()

        assert result == expected

    def test_asdict_extra_cannot_override_other_data(self, document_asdict, group_service, fake_links_service):
        ann = mock.Mock(extra={'flagged': 'yasss'})
        resource = AnnotationResource(ann, group_service, fake_links_service)
        document_asdict.return_value = {}

        formatters = [
            FakeFormatter({'flagged': 'nope'}),
        ]

        presented = AnnotationJSONPresenter(resource, formatters).asdict()
        assert presented['flagged'] == 'nope'

    def test_asdict_extra_uses_copy_of_extra(self, document_asdict, group_service, fake_links_service):
        extra = {'foo': 'bar'}
        ann = mock.Mock(id='my-id', extra=extra)
        resource = AnnotationResource(ann, group_service, fake_links_service)
        document_asdict.return_value = {}

        AnnotationJSONPresenter(resource).asdict()

        # Presenting the annotation shouldn't change the "extra" dict.
        assert extra == {'foo': 'bar'}

    def test_asdict_merges_formatters(self, group_service, fake_links_service):
        ann = mock.Mock(id='the-real-id', extra={})
        resource = AnnotationResource(ann, group_service, fake_links_service)

        formatters = [
            FakeFormatter({'flagged': 'nope'}),
            FakeFormatter({'nipsa': 'maybe'})
        ]
        presenter = AnnotationJSONPresenter(resource, formatters)
        presented = presenter.asdict()

        assert presented['flagged'] == 'nope'
        assert presented['nipsa'] == 'maybe'

    def test_immutable_formatters(self, group_service, fake_links_service):
        """Double-check we can't mutate the formatters list after the fact.

        This is an extra check just to make sure we can't accidentally change
        the constructor so that it simply aliases the list that's passed in,
        leaving us open to all kinds of mutability horrors.

        """
        ann = mock.Mock(id='the-real-id', extra={})
        resource = AnnotationResource(ann, group_service, fake_links_service)

        formatters = [FakeFormatter({'flagged': 'nope'})]
        presenter = AnnotationJSONPresenter(resource, formatters)
        formatters.append(FakeFormatter({'enterprise': 'synergy'}))
        presented = presenter.asdict()

        assert 'enterprise' not in presented

    def test_formatter_uses_annotation_resource(self, group_service, fake_links_service):
        annotation = mock.Mock(id='the-id', extra={})
        resource = AnnotationResource(annotation, group_service, fake_links_service)

        formatters = [IDDuplicatingFormatter()]
        presenter = AnnotationJSONPresenter(resource, formatters)

        output = presenter.asdict()

        assert output['duplicated-id'] == 'the-id'

    def test_exception_for_wrong_formatter_type(self):
        with pytest.raises(ValueError) as exc:
            AnnotationJSONPresenter(mock.Mock(), formatters=[mock.Mock()])

        assert 'not implementing IAnnotationFormatter interface' in exc.value.message

    @pytest.fixture
    def document_asdict(self, patch):
        return patch('h.presenters.annotation_json.DocumentJSONPresenter.asdict')
