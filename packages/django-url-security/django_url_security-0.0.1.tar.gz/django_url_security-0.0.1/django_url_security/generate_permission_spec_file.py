import csv
from pathlib import Path

from django_url_security.core import (
    PermissionSpec,
    ViewInfo,
    find_permission_spec_for_view_info,
    get_all_view_infos,
    get_spec_file_path,
    get_view_reference,
)


def print_permission_spec_file(spec_file_path=None):
    """
    Used to update the permission spec file when adding new url patterns.
    Should be able to replace the file with the output of this function,
    and the new version will include the appropriate ("NEW?") entries.
    """
    spec_file_path = spec_file_path or get_spec_file_path()

    view_infos = get_all_view_infos()
    view_info_to_permission_spec_map = {
        view_info: find_permission_spec_for_view_info(view_info) for view_info in view_infos
    }
    new_permission_specs = [
        permission_spec or generate_permission_spec(view_info)
        for view_info, permission_spec in view_info_to_permission_spec_map.items()
    ]

    if isinstance(spec_file_path, str):
        spec_file_path = Path(spec_file_path)

    with spec_file_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=PermissionSpec._fields)
        writer.writeheader()
        writer.writerows(
            {
                'status': spec.status,
                'pattern_name': spec.pattern_name,
                'reference': spec.reference,
                'simplified_regex': spec.simplified_regex,
                'is_public': 'PUBLIC' if spec.is_public else 'private',
                'notes': spec.notes,
            }
            for spec in new_permission_specs
        )


def generate_permission_spec(view_info: ViewInfo):
    """Generate a new permission spec for when a new url pattern has been added."""
    return PermissionSpec(
        status='NEW?',
        pattern_name=view_info.name,
        reference=get_view_reference(view_info.view_func),
        simplified_regex=view_info.simplified_regex,
        is_public=False,
    )
