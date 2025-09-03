import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ISPInternetPlan(Document):

	def validate(self):

		self.validate_price()
		self.validate_speed()


	def validate_price(self):
		"""Validar que el precio no sea 0 o menor"""
		if flt(self.get('price')) <= 0:
			frappe.throw(_("Price must be greater than 0"))


	def validate_speed(self):
		"""Validar download_speed y upload_speed"""
		for field in ['download_speed', 'upload_speed']:
			value = self.get(field)
			if value:
				value = str(value).upper()
				if not value.endswith('M') or not value[:-1].isdigit():
					frappe.throw(_("{value} is not a valid {field}").format(value=value, field=field))
