from django.db import models
from django.utils.translation import ugettext_lazy as _


class List(models.Model):
    user = models.IntegerField()
    title = models.CharField(max_length=30, verbose_name=_('Title'))

    def __str__(self):
        return self.title


class Entry(models.Model):
    DRINKS = 'DR'
    FOODS = 'FO'
    CATEGORIES = (
        (DRINKS, _('Drinks')),
        (FOODS, _('Foods')),
    )

    title = models.CharField(max_length=50, verbose_name=_('Title'))
    category = models.CharField(max_length=2,
                                choices=CATEGORIES)
    quantity = models.IntegerField(
        null=True, blank=True, verbose_name=_('Quantity'))
    grocery_list = models.ForeignKey(
        List, on_delete=models.CASCADE, null=True,
        blank=True, related_name="entries")

    class Meta:
        order_with_respect_to = "grocery_list"
