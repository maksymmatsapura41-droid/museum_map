from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Square, Comment


def home(request):
    return render(request, "grid/home.html")


@csrf_exempt
def save_comment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        row = data.get("row")
        col = data.get("col")
        text = data.get("text")

        if row is None or col is None or not text:
            return JsonResponse({"error": "Missing data"}, status=400)

        square, created = Square.objects.get_or_create(row=row, col=col)
        comment = Comment.objects.create(square=square, text=text)

        return JsonResponse({
            "message": "Saved successfully",
            "square": f"{row}, {col}",
            "comment_id": comment.id
        })

    return JsonResponse({"error": "Invalid request"}, status=405)


def get_comments(request):
    row = request.GET.get("row")
    col = request.GET.get("col")

    if row is None or col is None:
        return JsonResponse({"error": "Missing row or col"}, status=400)

    try:
        square = Square.objects.get(row=row, col=col)
        comments = list(square.comments.values("id", "text"))
    except Square.DoesNotExist:
        comments = []

    return JsonResponse({"comments": comments})
def delete_comments(request,pk):
    square = Square.objects.get(pk=pk)
    square.delete()
    return JsonResponse({"message": "Deleted successfully"}, status=200)
