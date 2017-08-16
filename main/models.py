from django.db import models


class List(models.Model):
    user = models.IntegerField()
    title = models.CharField(max_length=30)


class Entry(models.Model):
    title = models.CharField(max_length=50)
    quantity = models.IntegerField(null=True, blank=True)
    grocery_list = models.ForeignKey(
        List, on_delete=models.CASCADE, null=True, blank=True, related_name="entries")
