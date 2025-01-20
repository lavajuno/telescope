from django.db import models

class System(models.Model):
    """
    """

    display_name = models.CharField(max_length=64, unique=True)
    agent_id = models.CharField(max_length=32, unique=True)
    agent_secret = models.CharField(max_length=64)
    