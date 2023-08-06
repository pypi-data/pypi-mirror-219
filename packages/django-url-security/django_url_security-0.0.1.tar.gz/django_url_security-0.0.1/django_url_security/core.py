import csv
import functools
import re
from importlib import import_module
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
)

from django.contrib.admindocs.views import simplify_regex
from django.core.exceptions import ViewDoesNotExist
from django.urls import (
    URLPattern,
    URLResolver,
)

DEFAULT_URL_SECURITY_SPEC_FILENAME = 'url_security_spec.csv'


def get_spec_file_path() -> Path:
    from django.conf import settings

    base_dir = Path(settings.BASE_DIR)
    default_spec_file_path = base_dir / DEFAULT_URL_SECURITY_SPEC_FILENAME

    spec_file_path = Path(getattr(settings, 'URL_SECURITY_SPEC_FILE_PATH', default_spec_file_path))
    if not spec_file_path.is_absolute():
        spec_file_path = base_dir / spec_file_path

    return spec_file_path


class ViewInfo(NamedTuple):
    name: str
    url_pattern: Any
    view_func: Callable
    # regex: re.Pattern
    simplified_regex: str
    # default_args: dict
    # lookup_str: str


class PermissionSpec(NamedTuple):
    """
    A specification for what permissions should be required to access a given view
    via a url pattern
    """

    # Note: "OK" is used for passing specs to make all the other statuses stand out visually
    status: str  # ["NEW?", "FAILING", "ERROR", "NEEDS_FIXTURE", "OK"  ]
    pattern_name: str
    reference: str
    simplified_regex: str
    is_public: bool = True
    notes: str = ''


def extract_views_from_urlpatterns(urlpatterns, base='', namespace=None) -> List[ViewInfo]:
    """
    Return a list of ViewInfo objects from a list of urlpatterns.
    Originally copied from django_extensions.management.commands.show_urls.Command
    """
    views = []

    for p in urlpatterns:
        if isinstance(p, URLPattern):
            # For a single pattern, include it in the list
            try:
                name = f'{namespace}:{p.name}' if namespace else p.name
                views.append(
                    ViewInfo(
                        name=name,
                        url_pattern=p,
                        view_func=p.callback,
                        simplified_regex=simplify_regex(f'{base}{p.pattern}'),
                    ),
                )
            except ViewDoesNotExist:
                continue
        elif isinstance(p, URLResolver):
            # For an `include`, recurse into its patterns
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            if namespace and p.namespace:
                _namespace = f'{namespace}:{p.namespace}'
            else:
                _namespace = p.namespace or namespace
            views.extend(
                extract_views_from_urlpatterns(
                    patterns,
                    base=f'{base}{p.pattern}',
                    namespace=_namespace,
                ),
            )
        elif hasattr(p, '_get_callback'):
            # Not sure what this case covers
            try:
                views.append(
                    ViewInfo(
                        name=p.name,
                        url_pattern=p,
                        view_func=p._get_callback(),
                        simplified_regex=simplify_regex(f'{base}{p.pattern}'),
                    ),
                )
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            # Not sure what this case covers either
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(
                extract_views_from_urlpatterns(
                    patterns,
                    base=f'{base}{p.pattern}',
                    namespace=namespace,
                ),
            )
        else:
            raise TypeError(f'{p} does not appear to be a urlpattern object')  # noqa: TRY003
    return views


@functools.lru_cache(maxsize=1)
def get_all_view_infos() -> List[ViewInfo]:
    from django.conf import settings

    urlconf = settings.ROOT_URLCONF

    urls = import_module(urlconf) if isinstance(urlconf, str) else urlconf
    patterns = urls.urlpatterns

    return extract_views_from_urlpatterns(patterns)


@functools.lru_cache(maxsize=1)
def get_view_permission_specs(spec_file_path=None) -> List[PermissionSpec]:
    """Provide an interface to get the PermissionSpecs."""
    spec_file_path = spec_file_path or get_spec_file_path()

    if not spec_file_path.exists():
        return []

    with spec_file_path.open() as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            PermissionSpec(
                status='NEEDS_PERMISSIONS' if row['status'] == 'implemented' else row['status'],
                pattern_name=row['pattern_name'] or '',
                reference=row['reference'],
                simplified_regex=row['simplified_regex'],
                is_public=row['is_public'] == 'PUBLIC',
                notes=row['notes'],
            )
            for row in reader
        ]


def view_should_be_public(view_info: ViewInfo):
    permissions_spec = find_permission_spec_for_view_info(view_info)
    return permissions_spec and permissions_spec.is_public


def find_permission_spec_for_view_info(view_info: ViewInfo):
    patterns_with_matching_names = [
        permission_spec
        for permission_spec in get_view_permission_specs()
        if (
            permission_spec.pattern_name == (view_info.name or '')
            and permission_spec.simplified_regex == view_info.simplified_regex
            and permission_spec.reference == get_view_reference(view_info.view_func)
        )
    ]
    if len(patterns_with_matching_names) == 1:
        return patterns_with_matching_names[0]
    elif len(patterns_with_matching_names) == 0:
        return None
    else:
        # TODO: Deal with multiple matches
        return None


def get_view_reference(func) -> str:
    """Extracted from django_extensions.management.commands.show_urls"""
    if hasattr(func, '__name__'):
        # Functional views will have __name__
        func_name = func.__name__
    elif hasattr(func, '__class__'):
        # Class-based views will have __class__
        func_name = f'{func.__class__.__name__}()'
    else:
        # Dunno what will get here
        func_name = re.sub(r' at 0x[0-9a-f]+', '', repr(func))

    return f'{func.__module__}.{func_name}'


def figure_out_view_kwargs(view_func, url_pattern) -> Dict[str, str]:
    """
    Produce a kwarg dict like {'exam_pk': '1', 'sitting_id': '2'}
    to satisfy the view function argument requirements.
    """
    default_kwargs = url_pattern.default_args
    # Getting the groups from the regex seems to work. We could also inspect the func params.
    named_groups = url_pattern.pattern.regex.groupindex.keys()
    kwargs = {group_name: str(index) for index, group_name in enumerate(named_groups, start=1)}
    return {**default_kwargs, **kwargs}
