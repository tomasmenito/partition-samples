import uuid

import architect
from django.db import models

options = {
    "type": "range",
    "subtype": "date",
    "constraint": "month",
    "column": "purchased_at",    
}

@architect.install('partition', **options)
class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_id = models.UUIDField()
    buyer_id = models.UUIDField()
    purchased_at = models.DateTimeField(null=False)
