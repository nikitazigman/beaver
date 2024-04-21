import hashlib

import pytest

from code_api.models import CodeDocument
from django.urls import reverse
from language_api.models import Language
from rest_framework import status
from rest_framework.test import APITestCase
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

    CodeDocument.objects.all().delete()
    Tag.objects.all().delete()
    Language.objects.all().delete()


class BulkCreateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("code-document-bulk-create")
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

    def test_bulk_create_code_documents_with_valid_data(self):
        response = self.client.post(
            self.url, data=self.valid_data, format="json"
        )

        created_code_documents = CodeDocument.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for document, data in zip(created_code_documents, self.valid_data):
            self.assertEqual(document.title, data["title"])
            self.assertEqual(document.language.name, data["language"])
            self.assertEqual(document.code, data["code"])
            self.assertEqual(document.link_to_project, data["link_to_project"])
            self.assertEqual(
                list(document.tags.values_list("name", flat=True)),
                data["tags"],
            )


class BulkUpdateViewTestCase(APITestCase):
    def setUp(self):
        code_document_1 = CodeDocument.objects.create(
            id="03ead967-0bb6-4a02-97a1-4f7d8d27ce04",
            title="Test document 1",
            code="print('Test Code 1')",
            link_to_project="https://leetcode.com/problems/longest-common-prefix/",
            language=Language.objects.get(name="Python"),
            code_content_hash=hashlib.sha256(
                b"print('Test Code 1')"
            ).hexdigest(),
        )
        code_document_1.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        code_document_2 = CodeDocument.objects.create(
            id="747c10f1-518f-4be7-9397-e2ca13dcd9f9",
            title="Test document 2",
            code="print('Test Code 2')",
            link_to_project="https://leetcode.com/problems/reverse-integer/",
            language=Language.objects.get(name="Python"),
            code_content_hash=hashlib.sha256(
                b"print('Test Code 2')"
            ).hexdigest(),
        )
        code_document_2.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        self.url = reverse("code-document-bulk-update")
        self.valid_data = [
            {
                "id": "03ead967-0bb6-4a02-97a1-4f7d8d27ce04",
                "title": "Updated document 1",
                "code": "print('Updated code 1')",
                "link_to_project": "https://leetcode.com/problems/merge-k-sorted-lists/",
                "language": "Python",
                "tags": ["tag1", "tag2"],
            },
            {
                "id": "747c10f1-518f-4be7-9397-e2ca13dcd9f9",
                "title": "Updated document 2",
                "code": "console.log('Updated code 2');",
                "link_to_project": "https://leetcode.com/problems/combination-sum-ii/",
                "language": "Python",
                "tags": ["tag1", "tag2"],
            },
        ]

    def test_bulk_update_code_documents_with_valid_data(self):
        response = self.client.put(
            self.url, data=self.valid_data, format="json"
        )

        updated_code_documents = CodeDocument.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for document, data in zip(updated_code_documents, self.valid_data):
            self.assertEqual(document.title, data["title"])
            self.assertEqual(document.language.name, data["language"])
            self.assertEqual(document.code, data["code"])
            self.assertEqual(document.link_to_project, data["link_to_project"])
            self.assertEqual(
                list(document.tags.values_list("name", flat=True)),
                data["tags"],
            )


class BulkDeleteViewTestCase(APITestCase):
    def setUp(self):
        code_document_1 = CodeDocument.objects.create(
            id="f363f562-bc30-42aa-b96c-ff5c01c57e2c",
            title="Test document 1",
            code="print('Test Code 1')",
            link_to_project="https://leetcode.com/problems/maximum-subarray/",
            language=Language.objects.get(name="Python"),
            code_content_hash=hashlib.sha256(
                b"print('Test Code 1')"
            ).hexdigest(),
        )
        code_document_1.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        code_document_2 = CodeDocument.objects.create(
            id="19d5a9e6-f960-4014-a496-efa752d0855c",
            title="Test document 2",
            code="print('Test Code 2')",
            link_to_project="https://leetcode.com/problems/unique-paths-ii/",
            language=Language.objects.get(name="Python"),
            code_content_hash=hashlib.sha256(
                b"print('Test Code 2')"
            ).hexdigest(),
        )
        code_document_2.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        self.url = reverse("code-document-bulk-delete")
        self.valid_data = {
            "ids": [
                "f363f562-bc30-42aa-b96c-ff5c01c57e2c",
                "19d5a9e6-f960-4014-a496-efa752d0855c",
            ]
        }

    def test_bulk_delete_code_documents_with_valid_data(self):
        self.assertEqual(CodeDocument.objects.count(), 2)

        response = self.client.delete(
            self.url, data=self.valid_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CodeDocument.objects.count(), 0)


class CodeDocumentListViewTestCase(APITestCase):
    def test_get_code_documents(self):
        code_document_1 = CodeDocument.objects.create(
            id="f363f562-bc30-42aa-b96c-ff5c01c57e2c",
            title="Test document 1",
            code="print('Test Code 1')",
            link_to_project="https://leetcode.com/problems/search-a-2d-matrix/",
            language=Language.objects.get(name="Python"),
            code_content_hash=hashlib.sha256(
                b"print('Test Code 1')"
            ).hexdigest(),
        )
        code_document_1.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        code_document_2 = CodeDocument.objects.create(
            id="19d5a9e6-f960-4014-a496-efa752d0855c",
            title="Test document 2",
            code="print('Test Code 2')",
            link_to_project="https://leetcode.com/problems/partition-list/",
            language=Language.objects.get(name="Python"),
            code_content_hash=hashlib.sha256(
                b"print('Test Code 2')"
            ).hexdigest(),
        )
        code_document_2.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )
        self.url = reverse("code-documents")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test document 1")
        self.assertEqual(response.data[1]["title"], "Test document 2")

    def test_get_code_documents_with_title_filter(self):
        response = self.client.get(self.url + "?language=Python")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test document 1")
        self.assertEqual(response.data[1]["title"], "Test document 2")

    def test_get_code_documents_with_tags_filter(self):
        response = self.client.get(self.url + "?tags=tag1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
