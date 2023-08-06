from decimal import Decimal
from django.db import models
import django
if django.VERSION >= (4, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _  # pragma: no cover


class CoordinateMixin(models.Model):

    longitude = models.DecimalField(_('longitude'), max_digits=30, decimal_places=10, null=False, blank=True, default=Decimal('0.0'))
    latitude = models.DecimalField(_('latitude'), max_digits=30, decimal_places=10, null=False, blank=True, default=Decimal('0.0'))

    class Meta:
        abstract = True

    @property
    def is_valid_coordinate(self) -> bool:
        # 124 – 132, 33 – 43
        if self.longitude and self.latitude and (124 - 1 <= self.longitude <= 132 + 1) and (33 - 1 <= self.latitude <= 43 + 1):
            return True
        return False
