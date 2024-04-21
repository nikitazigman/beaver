from code_api.serializers import CodeDocumentSerializer

import pytest

from django.test import TestCase
from language_api.models import Language
from tags_api.models import Tag


@pytest.fixture(autouse=True)
def setup_db():
    Tag.objects.create(id="939551ed-b25d-4dec-9258-733277616709", name="tag1")
    Tag.objects.create(id="b7c16bf7-d4ad-404f-9402-f41d4cefdc53", name="tag2")
    Language.objects.create(
        id="e4e7b1b0-6b7b-4d6b-8b0f-6e1c7f7b3f2f", name="Python"
    )
    Language.objects.create(
        id="a5cda6e9-8f10-4430-87a9-8a7ef78f054a", name="JavaScript"
    )

    yield

    Tag.objects.all().delete()
    Language.objects.all().delete()


class CodeDocumentSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = [
            {
                "title": "Test document 1",
                "code": "print('Hello, World!')",
                "link_to_project": "https://leetcode.com/problems/integer-to-roman/",
                "language": "Python",
                "tags": ["tag1", "tag2"],
            },
            {
                "title": "Test document 2",
                "code": "console.log('Hello, World!');",
                "link_to_project": "https://leetcode.com/problems/palindrome-number/",
                "language": "Python",
                "tags": ["tag1", "tag2"],
            },
        ]
        self.serializer = CodeDocumentSerializer(
            data=self.valid_data, many=True
        )

    def test_serializer_with_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_with_invalid_data(self):
        self.serializer = CodeDocumentSerializer(data={})
        self.assertFalse(self.serializer.is_valid())
