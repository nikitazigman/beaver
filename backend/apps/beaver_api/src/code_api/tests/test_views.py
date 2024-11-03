from collections.abc import Generator
from datetime import datetime, timedelta

import pytest

from code_api.models import CodeDocument
from django.urls import reverse
from language_api.models import Language
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from tags_api.models import Tag
from users.models import BeaverUser


@pytest.fixture(autouse=True, scope="class")
def setup_db() -> Generator[None, None, None]:
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


class BulkUpdateViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(self) -> None:
        last_synchronization: datetime = datetime.now() - timedelta(days=1)
        code_document_1: CodeDocument = CodeDocument.objects.create(
            title="Test document 1",
            code="print('Test Code 1')",
            link_to_project="https://leetcode.com/problems/longest-common-prefix/",
            language=Language.objects.get(name="Python"),
            last_synchronization=last_synchronization,
        )
        code_document_1.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        code_document_2: CodeDocument = CodeDocument.objects.create(
            title="Test document 2",
            code="print('Test Code 2')",
            link_to_project="https://leetcode.com/problems/reverse-integer/",
            language=Language.objects.get(name="Python"),
            last_synchronization=last_synchronization,
        )
        code_document_2.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        self.url = reverse("code-document-bulk-update")
        self.valid_data: list[dict] = [
            {
                "title": "Test document 1",
                "code": "print('Updated code 1')",
                "link_to_project": "https://leetcode.com/problems/merge-k-sorted-lists/",
                "language": "Python",
                "tags": ["tag1", "tag2"],
                "last_synchronization": last_synchronization,
                "contributors": [
                    {
                        "name": "John",
                        "last_name": "Doe",
                        "address": "test@test.com",
                    }
                ],
            },
            {
                "title": "Test document 2",
                "code": "console.log('Updated code 2');",
                "link_to_project": "https://leetcode.com/problems/combination-sum-ii/",
                "language": "Python",
                "tags": ["tag1", "tag2"],
                "last_synchronization": last_synchronization,
                "contributors": [
                    {
                        "name": "John",
                        "last_name": "Doe",
                        "address": "test@test.com",
                    }
                ],
            },
        ]

    def setUp(self):
        # Create a user and obtain a token for authentication
        self.user: BeaverUser = BeaverUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token: Token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_bulk_update_code_documents_with_valid_data(self):
        response = self.client.post(
            path=self.url, data=self.valid_data, format="json"
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

    def test_create_new_code_document(self):
        nonexistent_data = [
            {
                "title": "New Doc",
                "code": "print('new doc')",
                "link_to_project": "https://example.com",
                "language": "Python",
                "tags": ["tag1", "tag2"],
                "last_synchronization": datetime.now(),
                "contributors": [
                    {
                        "name": "John",
                        "last_name": "Doe",
                        "address": "test@test.com",
                    }
                ],
            }
        ]

        self.assertEqual(CodeDocument.objects.count(), 2)
        response = self.client.post(self.url, nonexistent_data, format="json")
        self.assertEqual(CodeDocument.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_code_document_with_invalid_data_submission(self):
        invalid_data = [dict(data, code="") for data in self.valid_data]
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BulkDeleteViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.last_sync = datetime.now() - timedelta(days=1)
        code_document_1 = CodeDocument.objects.create(
            title="Test document 1",
            code="print('Test Code 1')",
            link_to_project="https://leetcode.com/problems/maximum-subarray/",
            language=Language.objects.get(name="Python"),
            last_synchronization=self.last_sync,
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
            last_synchronization=datetime.now() - timedelta(days=2),
        )
        code_document_2.tags.set(
            [Tag.objects.get(name="tag1"), Tag.objects.get(name="tag2")]
        )

        self.url = reverse("code-document-bulk-delete")
        self.valid_data = {"timestamp": self.last_sync}

    def setUp(self):
        # Create a user and obtain a token for authentication
        self.user = BeaverUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_bulk_delete_code_documents(self):
        self.assertEqual(CodeDocument.objects.count(), 2)

        response = self.client.post(
            self.url, data=self.valid_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CodeDocument.objects.count(), 1)
