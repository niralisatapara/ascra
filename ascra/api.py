import frappe
import datetime
from frappe.utils import flt, getdate, nowdate
from frappe.utils.safe_exec import get_safe_globals
from frappe.email.doctype.notification.notification import get_context
from erpnext.controllers.item_variant import copy_attributes_to_variant, make_variant_item_code
from six import string_types
import json

def item_validate(self,method):
	set_attribute(self)
	uom_conversion_factor_based_formaula(self)

def set_attribute(self):
	if self.attributes:
		for attribute in self.attributes:
			if attribute.attribute == "Width":
				self.width = attribute.attribute_value
			if attribute.attribute == "Height":
				self.height = attribute.attribute_value
			if attribute.attribute == "Yield":
				self.yield_ = attribute.attribute_value

def uom_conversion_factor_based_formaula(self):
	if self.uoms and not self.has_variants:
		for item in self.uoms:
			if item.formula:
				formula = item.formula.strip().replace("\n", " ") if item.formula else None
				if formula:
					item.conversion_factor = flt(frappe.safe_eval(formula, None, get_context(self.as_dict())))
					
# override method for javascript changes
@frappe.whitelist()
def create_variant(item, args):
	if isinstance(args, string_types):
		args = json.loads(args)

	template = frappe.get_doc("Item", item)
	variant = frappe.new_doc("Item")
	variant.variant_based_on = 'Item Attribute'
	variant_attributes = []

	# changes to update item values width, height and yield
	variant.width = args.get('Width')
	variant.height = args.get('Height')
	variant.yield_ = args.get('Yield')
	# changes end

	for d in template.attributes:
		variant_attributes.append({
			"attribute": d.attribute,
			"attribute_value": args.get(d.attribute)
		})

	variant.set("attributes", variant_attributes)
	copy_attributes_to_variant(template, variant)
	make_variant_item_code(template.item_code, template.item_name, variant)

	return variant