from photologue.models import Gallery

from django.http import JsonResponse
from .settings import MEDIA_URL


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args))


def json_list(request):
    request_from = request.GET.get('from', 'generic')
    # Add all public galleries to queryset
    queryset = Gallery.objects.on_site().is_public()

    # Add all galleries that contain the `from` text.
    # Use title__iexact for case insensitive matching (h1 does not get h15)
    queryset |= Gallery.objects.filter(title__startswith=request_from)
    response_data = {}
    response_data['from'] = request_from
    response_data['galleries'] = {}
    total = 0
    for x in xrange(len(queryset)):
        gallery = queryset[x]
        g = {}
        g['title'] = gallery.title
        g['photos'] = {}
        photo_count = 0
        for photo in gallery.photos.all():
            g['photos'][
                photo_count] = {}
            g['photos'][photo_count]['name'] = \
                photo.slug + '.' + str(photo.image).rsplit('.', 1)[-1]
            g['photos'][
                photo_count]['url'] = urljoin(MEDIA_URL, photo.image)
            photo_count += 1
        g['photo_count'] = photo_count
        response_data['galleries'][x] = g
        total += photo_count
    response_data['total'] = total
    return JsonResponse(response_data)
