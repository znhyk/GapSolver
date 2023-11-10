from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(USER_TABLE)
admin.site.register(LEARNER_TABLE)
admin.site.register(TEACHER_TABLE)
admin.site.register(BOOK_TABLE)
admin.site.register(TESTBANK_TABLE)
admin.site.register(TEST_TABLE)
admin.site.register(REVIEW_TABLE)
