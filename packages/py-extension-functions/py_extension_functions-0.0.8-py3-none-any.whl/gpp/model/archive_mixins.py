from django.contrib.auth import get_user_model
from django.db import models
import django
if django.VERSION >= (4, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _  # pragma: no cover


class ArchiveModelMixin(models.Model):
    """
        model 삭제시 archive
    """

    archive_date = models.DateTimeField(_('created date'), blank=True, editable=False)

    old_pk = models.BigIntegerField(_('old pk'), db_index=True, blank=False, editable=False)

    archive_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='+',
        null=True, blank=False, db_constraint=False,
        db_index=False,
    )

    class Meta:
        abstract = True
