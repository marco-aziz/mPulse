from rest_framework import serializers
from .models import Members

class MemberSerializer(serializers.ModelSerializer):
	"""
	Serializer class for Members model
	"""
	class Meta:
		"""
		specifiying fields
		no field for id, pk is default
		"""
		model = Members
		fields = (
			'first_name',
			'last_name',
			'phone_number',
			'client_member_id',
			'account_id'
		)