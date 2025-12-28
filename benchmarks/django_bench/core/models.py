from django.db import models

class Booking(models.Model):
  book_ref = models.CharField(max_length=6, primary_key=True)
  book_date = models.DateTimeField()
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    db_table = 'bookings'
    managed = False

  def __str__(self):
    return self.book_ref


class Ticket(models.Model):
  ticket_no = models.CharField(max_length=13, primary_key=True)
  book_ref = models.ForeignKey(
    Booking, db_column='book_ref', to_field='book_ref',
    on_delete=models.DO_NOTHING, related_name='tickets')
  passenger_id = models.TextField()
  passenger_name = models.TextField()
  outbound = models.BooleanField()

  class Meta:
    db_table = 'tickets'
    managed = False
    unique_together = (('book_ref', 'passenger_id', 'outbound'),)

  def __str__(self):
    return self.ticket_no
