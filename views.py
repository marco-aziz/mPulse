import csv, os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, List
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Members
from .serializers import MemberSerializer
from .mparser import MParser


class MemberView(generics.ListAPIView):
	"""
	View class for Members model list/detail 
	Support GET requests:
		with params 	detail view
		without params  list view
	Only for authenticated requests
	"""
	permission_classes = (IsAuthenticated, )
	serializer_class = MemberSerializer

	def get_queryset(self):
		"""
		Over rides gerenic's GET
		"""

		# Fetches Member model instances
		queryset = Members.objects.all()

		# Fetches Params from request, None if not found
		_id = self.request.query_params.get('id', None)
		account_id = self.request.query_params.get('aid', None)
		phone_number = self.request.query_params.get('ph', None)
		client_member_id = self.request.query_params.get('cmid', None)

		# Checks if any and filters queryset
		if _id:
			queryset = queryset.filter(pk=_id)
		elif account_id:
			queryset = queryset.filter(account_id=account_id)
		elif phone_number:
			queryset = queryset.filter(phone_number=phone_number)
		elif client_member_id:
			queryset = queryset.filter(client_member_id=client_member_id)

		# If no params were passed, all is returned
		return queryset


class MemberCreate(generics.CreateAPIView):
	"""
	View class for Members model instance creation
	Fully utilizes generics
	Only for authenticated users
	"""
	permission_classes = (IsAuthenticated, )
	queryset = Members.objects.all()
	serializer_class = MemberSerializer


class FileUploadView(APIView):
	"""
	View class for Members model batch create with file upload
	Utilizes mparser
	Only for authenticated users
	"""
	permission_classes = (IsAuthenticated, )
	queryset = Members.objects.all()
	serializer_class = MemberSerializer
	parser_classes = (MParser, )

	def put(self, request, format=None):
		"""
		Supports PUT request, most suited for file uploads
		"""

		# Gets file from request and saves temporarily for reading
		file_obj = request.FILES.get('file', None)
		fs = FileSystemStorage()
		filename = fs.save('temp.csv', file_obj)

		# Message Dict for storing progress updates for each line
		# Counter for progress reporting [0]: SUCCESS, [1]: DUP, [2]: FAIL
		messages = {}
		line_counter = 1
		status_counter = [0, 0, 0]

		# Opens the csv file and reading Dict
		with open('temp.csv', 'r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for line in csv_reader:

				# Gets model field names and checks if ALL in Dict keys
				keys_array = set([ f.name for f in Members._meta.fields ])
				if keys_array.issubset(line.keys()):
					
					# all fields are populated
					# Fetches Member model instances with same account id
					# Then filters this querysets once for phone_number and another for client_member_id
					qs = Members.objects.filter(account_id=line['account_id'])
					qs1 = qs.filter(phone_number=line['phone_number'])
					qs2 = qs.filter(client_member_id=line['client_member_id'])

					# "We want to ensure that, per account_id, phone_number OR client_member_ids are unique "
					# not count is True iff unique
					if not qs1.count() or not qs2.count() :
						Members.objects.create(
							first_name=line['first_name'],
							last_name=line['last_name'],
							phone_number=line['phone_number'],
							client_member_id=line['client_member_id'],
							account_id=line['account_id']
						)

						# adding messages to message Dict and updating total line counter
						messages[str(line_counter).rjust(4, '0')] = '[SUCCESS]: Member Subscribed'
						status_counter[0] += 1
					else:
						messages[str(line_counter).rjust(4, '0')] = '[DUP]: Member was already subscribed with phone number or client id'
						status_counter[1] += 1
				else:
					messages[str(line_counter).rjust(4, '0')] = '[FAIL]: inconsistent field names'
					status_counter[2] += 1
				line_counter += 1
		#Deleting the uploaded file
		os.remove('temp.csv')
		messages['RESULT'] = 'Of {} records: {} SUCCESS , {} Duplicate , {} FAIL '.format(line_counter-1, status_counter[0],status_counter[1],status_counter[2])
		
		#Formulating and returning response
		return Response(messages, status=204)






























