from django.db import models


class Members(models.Model):
	"""
	Model class for Members model
	"""
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.IntegerField()
	client_member_id = models.IntegerField()
	account_id = models.IntegerField()

	def __str__(self):
		return str(self.pk)

	
	def fields(self):
		"""
		Returns model field names
		Used for validation in views
		"""
		return [ f.name for f in self._meta.fields + self._meta.many_to_many ]
