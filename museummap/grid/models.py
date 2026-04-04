from django.db import models


class Square(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()

    def __str__(self):
        return f"{self.row}, {self.col}"


class Comment(models.Model):
    square = models.ForeignKey(Square, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

    def __str__(self):
        return self.text[:30]