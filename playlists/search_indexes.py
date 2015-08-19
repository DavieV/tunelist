import datetime
from haystack import indexes
from django.contrib.auth.models import User

class UserIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	date_joined = indexes.DateTimeField(model_attr='date_joined')

	def get_model(self):
		return User

	def index_queryset(self, using=None):
		'''
		Used when the entire index for a model is updated
		'''
		return self.get_model().objects.filter(
			date_joined__lte=datetime.datetime.now()
		)
