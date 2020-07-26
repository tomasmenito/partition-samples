import uuid

from django.db import models


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_id = models.UUIDField()
    buyer_id = models.UUIDField()
    purchased_at = models.DateTimeField(null=False)
