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


class Route(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class RoutePoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="points")
    square = models.ForeignKey(Square, on_delete=models.CASCADE, related_name="route_points")
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.route.title} - step {self.order} - ({self.square.row}, {self.square.col})"


class Drawing(models.Model):
    square = models.ForeignKey(Square, on_delete=models.CASCADE, related_name="drawings")
    stroke_data = models.JSONField(default=list)
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Drawing for ({self.square.row}, {self.square.col})"