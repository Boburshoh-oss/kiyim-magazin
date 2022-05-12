from django.db import models


# Create your models here.
class Card(models.Model):
    card_id      = models.CharField(max_length=250,blank=True)
    date_added   = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.card_id

class CardItem(models.Model):
    user = models.ForeignKey("account.Account",on_delete=models.CASCADE,null=True)
    product      = models.ForeignKey("store.Product",on_delete=models.CASCADE)
    variations   = models.ManyToManyField("store.Variation")
    card         = models.ForeignKey("cards.Card",on_delete=models.CASCADE,null=True)
    quantity     = models.IntegerField()
    is_active    = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self) -> str:
        return f"{self.product.title}"            