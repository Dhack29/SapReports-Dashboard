from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'employee' # Assuming this is an existing Postgres table
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
