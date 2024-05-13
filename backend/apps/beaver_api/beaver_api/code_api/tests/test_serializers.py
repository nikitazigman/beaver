import hashlib

from code_api.models import CodeDocument
from code_api.serializers import CodeDocumentSerializer

import pytest

from django.core.exceptions import ValidationError
from django.test import TestCase
from language_api.models import Language
from tags_api.models import Tag


@pytest.fixture(autouse=True, scope="class")
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

    CodeDocument.objects.all().delete()
    Tag.objects.all().delete()
    Language.objects.all().delete()


class CodeDocumentSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Test document 1",
            "code": "print('Hello, World!')",
            "link_to_project": "https://leetcode.com/problems/integer-to-roman/",
            "language": Language.objects.get(name="Python"),
            "tags": [
                Tag.objects.get(name="tag1"),
                Tag.objects.get(name="tag2"),
            ],
        }

    def test_create_method(self):
        serializer = CodeDocumentSerializer()
        instance = serializer.create(self.valid_data)

        self.assertIsInstance(instance, CodeDocument)
        self.assertEqual(instance.title, self.valid_data["title"])
        self.assertEqual(instance.code, self.valid_data["code"])
        self.assertEqual(
            instance.link_to_project, self.valid_data["link_to_project"]
        )
        self.assertEqual(instance.language, self.valid_data["language"])
        self.assertEqual(instance.tags.count(), 2)

        encoded_code_content = self.valid_data["code"].encode("utf-8")
        hashed_code_content = hashlib.sha256(encoded_code_content).hexdigest()
        self.assertEqual(instance.code_content_hash, hashed_code_content)

    def test_update_method(self):
        instance = CodeDocument.objects.create(
            title="Test document",
            code="print('Hello, World!')",
            link_to_project="https://leetcode.com/problems/integer-to-roman/",
            language=Language.objects.get(name="Python"),
        )

        tags = [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        instance.tags.set(tags)

        validated_data = {
            "title": "Updated document",
            "code": "console.log('Hello, World!');",
            "link_to_project": "https://leetcode.com/problems/palindrome-number/",
            "language": Language.objects.get(name="JavaScript"),
            "tags": [
                Tag.objects.get(name="tag1"),
                Tag.objects.get(name="tag2"),
            ],
        }
        serializer = CodeDocumentSerializer()
        updated_instance = serializer.update(instance, validated_data)

        self.assertEqual(updated_instance.title, validated_data["title"])
        self.assertEqual(updated_instance.code, validated_data["code"])
        self.assertEqual(
            updated_instance.link_to_project, validated_data["link_to_project"]
        )
        self.assertEqual(updated_instance.language, validated_data["language"])
        self.assertEqual(updated_instance.tags.count(), 2)

    def test_validate_link_to_project_with_valid_url(self):
        url = "https://leetcode.com/problems/integer-to-roman/"
        serializer = CodeDocumentSerializer()
        validated_url = serializer.validate_link_to_project(url)
        self.assertEqual(validated_url, url)

    def test_validate_link_to_project_with_invalid_url(self):
        invalid_url = "invalid_url"
        serializer = CodeDocumentSerializer()
        with self.assertRaises(ValidationError):
            serializer.validate_link_to_project(invalid_url)
