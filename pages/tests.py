from decimal import Decimal

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
