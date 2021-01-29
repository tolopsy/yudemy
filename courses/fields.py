from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
	def __init__(self, for_fields=None, *args, **kwargs):
		self.for_fields = for_fields
		super(OrderField, self).__init__(*args, **kwargs)

	def pre_save(self, model_instance, add):
		if getattr(model_instance, self.attname) is None:
			try:
				all_model = self.model.objects.all()

				if self.for_fields:
					query  = {field: getattr(model_instance, field) for field in self.for_fields}
					all_model = all_model.filter(**query)

				last_item = all_model.latest(self.attname)
				value = getattr(last_item, self.attname) + 1

			except ObjectDoesNotExist:
				value = 0

			setattr(model_instance, self.attname, value)
			return value

		else:
			return super(OrderField, self).pre_save(model_instance, add)
