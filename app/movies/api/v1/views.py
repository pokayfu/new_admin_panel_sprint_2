from typing import Any
from django.contrib.postgres.aggregates import ArrayAgg
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.db.models import Q
from django.http import JsonResponse

from movies.models import (
    Filmwork,
    PersonFilmwork,
)


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        filmworks = Filmwork.objects.values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleType.ACTOR),
                distinct=True,
            ),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleType.DIRECTOR),
                distinct=True,
            ),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleType.WRITER),
                distinct=True,
            )
        )
        return filmworks


    def render_to_response(
        self, context: dict[str, Any], **response_kwargs
    ) -> JsonResponse:
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, **_) -> dict[str, Any]:
        queryset = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        
        if page.has_previous():
            prev_page = page.previous_page_number()
        else:
            prev_page = None
        if page.has_next():
            next_page = page.next_page_number()
        else:
            next_page = None

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": list(page),
        }
        return context

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg = "id"

    def get_context_data(self, **_) -> dict[str, Any]:
        return _
