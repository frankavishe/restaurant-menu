from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from menu.models import Category, MenuItem

from .forms import ContactForm
from .models import ContactMessage


class ContactMessageModelTests(TestCase):
    def test_str_includes_name_and_timestamp(self):
        message = ContactMessage.objects.create(
            name="Visitor",
            contact_info="visitor@example.com",
            message="Hello there",
        )
        self.assertIn("Visitor", str(message))

    def test_valid_message_passes_full_clean(self):
        message = ContactMessage(
            name="Visitor",
            contact_info="visitor@example.com",
            message="x" * 2000,
        )
        message.full_clean()  # should not raise


class ContactFormTests(TestCase):
    def _data(self, **overrides):
        defaults = dict(name="Visitor", contact_info="visitor@example.com", message="Hello there")
        defaults.update(overrides)
        return defaults

    def test_valid_email_contact_info_accepted(self):
        form = ContactForm(data=self._data())
        self.assertTrue(form.is_valid())

    def test_valid_phone_contact_info_accepted(self):
        form = ContactForm(data=self._data(contact_info="+1 555-123-4567"))
        self.assertTrue(form.is_valid())

    def test_malformed_contact_info_rejected(self):
        form = ContactForm(data=self._data(contact_info="not-an-email-or-phone"))
        self.assertFalse(form.is_valid())
        self.assertIn("contact_info", form.errors)

    def test_missing_required_field_rejected(self):
        form = ContactForm(data=self._data(name=""))
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_message_over_2000_chars_rejected(self):
        form = ContactForm(data=self._data(message="x" * 2001))
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_message_at_2000_chars_accepted(self):
        form = ContactForm(data=self._data(message="x" * 2000))
        self.assertTrue(form.is_valid())


class HomeViewTests(TestCase):
    def test_featured_items_capped_at_six(self):
        category = Category.objects.create(name="Starters")
        for i in range(7):
            MenuItem.objects.create(
                name=f"Dish {i}",
                description="Tasty",
                price=Decimal("5.00"),
                category=category,
                is_featured=True,
            )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["featured_items"]), 6)

    def test_no_featured_items_shows_fallback_message(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No featured dishes")


class ContactViewTests(TestCase):
    def test_get_renders_blank_form(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_bound)

    def test_valid_post_persists_and_redirects_with_sent_flag(self):
        response = self.client.post(reverse("contact"), {
            "name": "Visitor",
            "contact_info": "visitor@example.com",
            "message": "Hello there",
        })
        self.assertRedirects(response, f"{reverse('contact')}?sent=1")
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_post_does_not_persist_and_shows_errors(self):
        response = self.client.post(reverse("contact"), {
            "name": "",
            "contact_info": "visitor@example.com",
            "message": "Hello there",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)

    def test_message_over_limit_rejected_without_saving(self):
        response = self.client.post(reverse("contact"), {
            "name": "Visitor",
            "contact_info": "visitor@example.com",
            "message": "x" * 2001,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_confirmation_shown_when_sent_query_param_present(self):
        response = self.client.get(f"{reverse('contact')}?sent=1")
        self.assertContains(response, "Thanks for reaching out")


class ContactMessageAdminActionTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="pw12345"
        )
        self.client.force_login(self.superuser)
        self.msg = ContactMessage.objects.create(
            name="Visitor", contact_info="visitor@example.com", message="hi"
        )

    def test_mark_as_read_action(self):
        url = reverse("admin:pages_contactmessage_changelist")
        response = self.client.post(url, {
            "action": "mark_as_read",
            "_selected_action": [str(self.msg.pk)],
        }, follow=True)
        self.msg.refresh_from_db()
        self.assertTrue(self.msg.is_read)
        self.assertEqual(response.status_code, 200)

    def test_mark_as_unread_action(self):
        self.msg.is_read = True
        self.msg.save()
        url = reverse("admin:pages_contactmessage_changelist")
        response = self.client.post(url, {
            "action": "mark_as_unread",
            "_selected_action": [str(self.msg.pk)],
        }, follow=True)
        self.msg.refresh_from_db()
        self.assertFalse(self.msg.is_read)
        self.assertEqual(response.status_code, 200)


class AdminBrandingTests(TestCase):
    def test_login_page_shows_custom_site_header(self):
        response = self.client.get(reverse("admin:login"))
        self.assertContains(response, "Restaurant Name Admin")

    def test_index_page_shows_custom_header_and_stats(self):
        User.objects.create_superuser(
            username="admin", email="admin@example.com", password="pw12345"
        )
        self.client.login(username="admin", password="pw12345")
        category = Category.objects.create(name="Mains")
        MenuItem.objects.create(
            name="Burger", description="x", price=Decimal("9.99"),
            category=category, is_featured=True,
        )
        ContactMessage.objects.create(
            name="Visitor", contact_info="visitor@example.com", message="hi"
        )

        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "Restaurant Name Admin")
        self.assertEqual(response.context["category_count"], 1)
        self.assertEqual(response.context["menu_item_count"], 1)
        self.assertEqual(response.context["featured_item_count"], 1)
        self.assertEqual(response.context["unread_message_count"], 1)
