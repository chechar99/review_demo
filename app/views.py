from django.shortcuts import render
from models import Company, Review
from tokenapi.decorators import token_required
from django.core.exceptions import PermissionDenied
from tokenapi.http import JsonResponse, JsonError
from django.forms.models import model_to_dict


def get_client_ip(request):
    """
    Get client ip address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@token_required
def set_review(request):
    """
    Set review by user
    """
    user = request.user
    if not user.is_authenticated():
        return JsonError("PermissionDenied")

    review = Review()
    review.title = request.POST.get("title")
    review.rating = request.POST.get("rating")
    review.summary = request.POST.get("summary")
    review.ip_address = get_client_ip(request)
    review.reviewer = user
    review.company_id = request.POST.get("company_id")
    review.save()
    return JsonResponse({'status': 'success', 'review_id': review.id})


@token_required
def get_review_list(request):
    """
    Set review by user
    """
    user = request.user
    if not user.is_authenticated():
        raise PermissionDenied()
    reviews = Review.objects.filter(reviewer=user)
    review_list = []
    for review in reviews:
        review_list.append(model_to_dict(review))
    return JsonResponse({'status': 'success', 'data': review_list})
