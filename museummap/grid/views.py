from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Square, Comment, Route, RoutePoint, Drawing


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

        row = int(row)
        col = int(col)

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

    row = int(row)
    col = int(col)

    try:
        square = Square.objects.get(row=row, col=col)
        comments = list(square.comments.values("id", "text"))
    except Square.DoesNotExist:
        comments = []

    return JsonResponse({"comments": comments})


@csrf_exempt
def delete_comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        comment_id = data.get("id")

        if comment_id is None:
            return JsonResponse({"error": "Missing comment id"}, status=400)

        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return JsonResponse({"message": "Deleted successfully"})
        except Comment.DoesNotExist:
            return JsonResponse({"error": "Comment not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=405)


@csrf_exempt
def save_route(request):
    if request.method == "POST":
        data = json.loads(request.body)

        title = data.get("title")
        description = data.get("description", "")
        squares = data.get("squares", [])

        if not title or not squares:
            return JsonResponse({"error": "Missing title or squares"}, status=400)

        route = Route.objects.create(title=title, description=description)

        for index, square_data in enumerate(squares, start=1):
            row = square_data.get("row")
            col = square_data.get("col")

            if row is None or col is None:
                continue

            square, created = Square.objects.get_or_create(row=int(row), col=int(col))
            RoutePoint.objects.create(
                route=route,
                square=square,
                order=index
            )

        return JsonResponse({
            "message": "Route saved successfully",
            "route_id": route.id,
            "title": route.title
        })

    return JsonResponse({"error": "Invalid request"}, status=405)


def get_routes(request):
    routes = list(Route.objects.values("id", "title", "description"))
    return JsonResponse({"routes": routes})


def get_route_detail(request, route_id):
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return JsonResponse({"error": "Route not found"}, status=404)

    points = [
        {
            "order": point.order,
            "row": point.square.row,
            "col": point.square.col
        }
        for point in route.points.select_related("square").all()
    ]

    return JsonResponse({
        "id": route.id,
        "title": route.title,
        "description": route.description,
        "points": points
    })


def get_shared_coordinates(request):
    shared_points = (
        RoutePoint.objects
        .values("square__row", "square__col")
        .annotate(route_count=Count("route", distinct=True))
        .filter(route_count__gt=1)
        .order_by("-route_count", "square__row", "square__col")
    )

    shared_coordinates = [
        {
            "row": point["square__row"],
            "col": point["square__col"],
            "route_count": point["route_count"]
        }
        for point in shared_points
    ]

    return JsonResponse({"shared_coordinates": shared_coordinates})


def get_shared_coordinate_detail(request):
    row = request.GET.get("row")
    col = request.GET.get("col")

    if row is None or col is None:
        return JsonResponse({"error": "Missing row or col"}, status=400)

    row = int(row)
    col = int(col)

    try:
        square = Square.objects.get(row=row, col=col)
    except Square.DoesNotExist:
        return JsonResponse({"error": "Square not found"}, status=404)

    route_points = (
        RoutePoint.objects
        .filter(square=square)
        .select_related("route")
        .order_by("route__title", "order")
    )

    routes = []
    seen_route_ids = set()

    for point in route_points:
        if point.route.id not in seen_route_ids:
            routes.append({
                "id": point.route.id,
                "title": point.route.title,
                "description": point.route.description,
                "order": point.order
            })
            seen_route_ids.add(point.route.id)

    return JsonResponse({
        "row": row,
        "col": col,
        "routes": routes
    })


@csrf_exempt
def save_drawing(request):
    if request.method == "POST":
        data = json.loads(request.body)

        row = data.get("row")
        col = data.get("col")
        stroke_data = data.get("stroke_data", [])
        caption = data.get("caption", "")

        if row is None or col is None or not stroke_data:
            return JsonResponse({"error": "Missing drawing data"}, status=400)

        row = int(row)
        col = int(col)

        square, created = Square.objects.get_or_create(row=row, col=col)

        drawing = Drawing.objects.create(
            square=square,
            stroke_data=stroke_data,
            caption=caption
        )

        return JsonResponse({
            "message": "Drawing saved successfully",
            "drawing_id": drawing.id
        })

    return JsonResponse({"error": "Invalid request"}, status=405)


def get_drawings(request):
    row = request.GET.get("row")
    col = request.GET.get("col")

    if row is None or col is None:
        return JsonResponse({"error": "Missing row or col"}, status=400)

    row = int(row)
    col = int(col)

    try:
        square = Square.objects.get(row=row, col=col)
        drawings = list(
            square.drawings.values("id", "stroke_data", "caption", "created_at")
        )
    except Square.DoesNotExist:
        drawings = []

    return JsonResponse({"drawings": drawings})