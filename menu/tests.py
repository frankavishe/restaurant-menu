from decimal import Decimal

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .admin import MenuItemAdmin
from .models import Category, MenuItem
from .validators import validate_image_size


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name="Starters")
        self.assertEqual(str(category), "Starters")

    def test_slug_auto_generated_from_name(self):
        category = Category.objects.create(name="Main Course")
        self.assertEqual(category.slug, "main-course")

    def test_explicit_slug_is_preserved(self):
        category = Category.objects.create(name="Drinks", slug="beverages")
        self.assertEqual(category.slug, "beverages")


class MenuItemModelValidationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Starters")

    def _make_item(self, **overrides):
        defaults = dict(
            name="Soup",
            description="Tasty soup",
            price=Decimal("9.99"),
            category=self.category,
        )
        defaults.update(overrides)
        return MenuItem(**defaults)

    def test_valid_item_passes_full_clean(self):
        item = self._make_item()
        item.full_clean()  # should not raise

    def test_negative_price_rejected(self):
        item = self._make_item(price=Decimal("-1.00"))
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_disallowed_image_extension_rejected(self):
        bad_file = SimpleUploadedFile("dish.gif", b"fake-bytes", content_type="image/gif")
        item = self._make_item(image=bad_file)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_allowed_image_extension_accepted(self):
        good_file = SimpleUploadedFile("dish.png", b"fake-bytes", content_type="image/png")
        item = self._make_item(image=good_file)
        item.full_clean()  # should not raise

    def test_validate_image_size_rejects_oversized_file(self):
        class FakeFile:
            size = 6 * 1024 * 1024  # 6MB, over the 5MB cap (FR-009a)

        with self.assertRaises(ValidationError):
            validate_image_size(FakeFile())

    def test_validate_image_size_accepts_file_under_limit(self):
        class FakeFile:
            size = 1 * 1024 * 1024  # 1MB

        validate_image_size(FakeFile())  # should not raise

    def test_str_returns_name(self):
        item = self._make_item()
        self.assertEqual(str(item), "Soup")


class MenuListViewTests(TestCase):
    def setUp(self):
        self.starters = Category.objects.create(name="Starters")
        self.drinks = Category.objects.create(name="Drinks")
        self.soup = MenuItem.objects.create(
            name="Soup", description="Tasty soup", price=Decimal("9.99"), category=self.starters
        )
        self.cola = MenuItem.objects.create(
            name="Cola", description="Fizzy drink", price=Decimal("2.50"), category=self.drinks
        )

    def test_list_shows_all_items_with_no_filter(self):
        response = self.client.get(reverse("menu_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Soup")
        self.assertContains(response, "Cola")
        self.assertIsNone(response.context["active_category"])

    def test_filter_by_category_slug_shows_only_that_category(self):
        response = self.client.get(reverse("menu_list"), {"category": self.starters.slug})
        self.assertContains(response, "Soup")
        self.assertNotContains(response, "Cola")
        self.assertEqual(response.context["active_category"], self.starters)

    def test_unmatched_category_slug_falls_back_to_full_list(self):
        response = self.client.get(reverse("menu_list"), {"category": "does-not-exist"})
        self.assertContains(response, "Soup")
        self.assertContains(response, "Cola")
        self.assertIsNone(response.context["active_category"])

    def test_empty_menu_renders_empty_state(self):
        MenuItem.objects.all().delete()
        response = self.client.get(reverse("menu_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No menu items")


class MenuItemDetailViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Starters")
        self.item = MenuItem.objects.create(
            name="Soup", description="Tasty soup", price=Decimal("9.99"), category=self.category
        )

    def test_existing_item_returns_200_with_details(self):
        response = self.client.get(reverse("menu_item_detail", args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Soup")
        self.assertContains(response, "9.99")

    def test_missing_item_returns_404(self):
        response = self.client.get(reverse("menu_item_detail", args=[999999]))
        self.assertEqual(response.status_code, 404)


class MenuItemAdminImagePreviewTests(TestCase):
    def test_image_preview_blank_image_returns_placeholder(self):
        category = Category.objects.create(name="Starters")
        item = MenuItem.objects.create(
            name="Soup", description="Tasty soup", price=Decimal("9.99"), category=category
        )
        admin_instance = MenuItemAdmin(MenuItem, admin.site)
        self.assertEqual(admin_instance.image_preview(item), "—")
