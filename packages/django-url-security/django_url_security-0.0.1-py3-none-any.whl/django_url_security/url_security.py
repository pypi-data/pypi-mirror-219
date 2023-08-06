from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import (
    Http404,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.test import RequestFactory, TestCase
from parameterized import parameterized

from .core import (
    ViewInfo,
    figure_out_view_kwargs,
    find_permission_spec_for_view_info,
    get_all_view_infos,
    get_spec_file_path,
    get_view_permission_specs,
    view_should_be_public,
)


def get_test_name(testcase_func, param_num, param):
    base_name = f'{testcase_func.__name__}_{param_num}'
    (view_info,) = param.args
    # Some url patterns don't have a name so use the url regex instead
    view_info_test_name = view_info.name or view_info.simplified_regex
    return f'{base_name}_{parameterized.to_safe_name(view_info_test_name)}'


class UrlSecurityTestCase(TestCase):
    """
    Test that all url entries have appropriate permissions requirements
    Permissions are specified in `view_permission_specifications.csv`.

    This test is a work-in-progress, designed to require every url entry be given attention,
    but does not force the completion or correctness of the specifications.

    The statuses in the spec file must be manually updated.

    "I added/changed a view and now these tests are failing. What's up with that?"
    - This test suite checks that private views are actually private.
    - Your view needs an entry in the spec. You need to run `manage.py export_url_security_file`,
      which will call `generate_permission_spec_file.print_permission_spec_file()`,
      and then edit the now-updated `view_permission_specifications.csv`.
    - Find the newly-added or modified line, which should have a `NEW?` status, and set it to `OK`.
    - Run the tests again. If you can't get the test for your new url to pass, you may need to
      change the status to one of those below (e.g. if it needs fixtures, because they haven't
      been implemented yet).

    What the statuses mean:
    - "OK" means the test(s) for that view are passing.
      An unauthenticated request is accepted if the view is specced as public; rejected if private.
    - "FAILING" means the test is returning a failure.
      This may indicate a problem with the view, or that the test scaffolding needs further work.
    - "NEEDS_FIXTURE" means the test is failing or throwing an error, and it has been identified
      that this is because it's looking for a database object that doesn't exist.
      Fixtures have not been implemented at this stage.
      If these are private views, they should be wrapped in a `requires_login` check so that
      unauthenticated requests return a 403 rather that prompting a database hit and a 404.
    - "ERROR" means the test is throwing an error that is not identified as fixture-related.
    - "NEW?" means the line has been added when the spec file was last generated, and needs to
      have details added.

    The `assert_outcome_matches_status` method below takes the statuses into account, and ignores
    tests that match the expected outcome given their specified status.
    E.G. a test that's marked as "FAILING" will be ignored, rather than report a failure, if its
    assertion fails. If it passes or throws an error, the test will show a failure.

    To make progress on improving the currently-problematic specs, change the status of the spec
    in the spec file to `OK`, and you'll see the real errors with tracebacks on the next test run.
    """

    weird_ones = {
        "<class 'nap.http.decorators.except_response'>": {
            "ViewInfo(view_func=<nap.http.decorators.except_response object at 0x7fac40e0d0d0>, regex='^api/v1/^job/$', name='job-request')",  # noqa: E501
        },
        "<class 'method'>": {
            "ViewInfo(view_func=<bound method JSONRPCAPI.jsonrpc of <jsonrpc.backend.django.JSONRPCAPI object at 0x7fac40e511f0>>, regex='^liss/^rpc/?^$', name='endpoint')",  # noqa: E501
            "ViewInfo(view_func=<bound method AdminSite.login of <django.contrib.admin.sites.AdminSite object at 0x7fac80536400>>, regex='^secret/login/', name='admin:login')",  # noqa: E501
        },
    }

    # django.views.generic.base.RedirectView don't get names

    def setUp(self) -> None:
        self.request_factory = RequestFactory()

    def request(self, view_func, url_pattern, method='GET', user=None, path='/fakeurl/'):
        request = self.request_factory.request(method=method, path=path)
        request.user = user or AnonymousUser()
        view_kwargs = figure_out_view_kwargs(view_func, url_pattern)
        try:
            response = view_func(request, **view_kwargs)
        except PermissionDenied:
            # Some views raise 403s and rely on them being caught
            response = HttpResponseForbidden()
        except Http404:
            # Some views raise 404s and rely on them being caught
            response = HttpResponseNotFound()
        return response

    def get(self, view_func, url_pattern, **kwargs):
        return self.request(view_func, url_pattern, method='get', **kwargs)

    # def test_landing_page_view_is_public(self):
    #     view_infos = get_all_view_infos()
    #
    #     types = defaultdict(set)
    #
    #     for view_info in view_infos:
    #         types[type(view_info.view_func)].add(view_info)
    #
    #     # print(types)
    #
    #     landing_page_view_info = [info for info in view_infos if info.name == 'home'][0]
    #     print(landing_page_view_info)
    #     view_func = landing_page_view_info.view_func
    #     print(view_func.view_class)
    #     print(view_func.view_class.http_method_names)
    #     print(view_func.view_class.response_class)
    #     print(view_func.view_class.template_name)
    #     print(view_func.view_initkwargs)
    #
    #     self.assert_view_is_public(view_func)

    @parameterized.expand(
        lambda: ((info,) for info in get_all_view_infos() if view_should_be_public(info)),
        name_func=get_test_name,
        skip_on_empty=True,
    )
    def test_public_views_are_public(self, view_info: ViewInfo):
        permission_spec = find_permission_spec_for_view_info(view_info)
        if not permission_spec:  # sourcery skip: no-conditionals-in-tests
            self.fail(f'No permission spec found for view {view_info}')
        self.assert_outcome_matches_status(
            permission_spec,
            lambda: self.assert_view_is_public(view_info.view_func, view_info.url_pattern),
        )

    @parameterized.expand(
        lambda: ((info,) for info in get_all_view_infos() if not view_should_be_public(info)),
        name_func=get_test_name,
        skip_on_empty=True,
    )
    def test_non_public_views_are_not_public(self, view_info: ViewInfo):
        permission_spec = find_permission_spec_for_view_info(view_info)
        if not permission_spec:  # sourcery skip: no-conditionals-in-tests
            self.fail(f'No permission spec found for view {view_info}')
        self.assert_outcome_matches_status(
            permission_spec,
            lambda: self.assert_view_is_not_public(view_info.view_func, view_info.url_pattern),
        )

    def assert_outcome_matches_status(self, permission_spec, callable_assertion):
        if permission_spec.status == 'FAILING':
            try:
                callable_assertion()
            except AssertionError as err:
                if '404' in str(err):
                    self.fail('Test marked as ERROR returned 404 - mark as NEEDS_FIXTURE instead')
                else:
                    self.skipTest('Test needs attention - currently failing')
            else:
                self.fail('Expected test to fail but it passed')
        elif permission_spec.status == 'ERROR':
            try:
                callable_assertion()
            except Exception:
                self.skipTest('Test needs attention - currently throwing an error')
            else:
                self.fail("Expected test to raise error but it didn't")
        elif permission_spec.status == 'IGNORE':
            self.skipTest(
                'Test needs attention - currently ignored until we figure out how to deal with it',
            )
        elif permission_spec.status == 'NEEDS_FIXTURE':
            try:
                callable_assertion()
            except AssertionError as err:
                if '404' in str(err):
                    self.skipTest('Test needs attention - awaiting fixtures')
                else:
                    self.fail(
                        'Test marked as NEEDS_FIXTURE not returning 404'
                        ' - mark as ERROR or FAILING instead?',
                    )
            else:
                self.fail("Expected test to fail based on missing fixture but it didn't")
        else:
            callable_assertion()

    def assert_view_is_public(self, view_func, url_pattern):
        # TODO: Refine this to deal with redirects to public resources
        response = self.get(view_func, url_pattern=url_pattern)
        self.assertEqual(response.status_code, 200)

    def assert_view_is_not_public(self, view_func, url_pattern):
        # TODO: Refine this to check where the redirects go
        # 302 to login page = good. 302 elsewhere = ???
        acceptable_status_codes = [301, 302, 401, 403, 405]
        response = self.get(view_func, url_pattern=url_pattern)
        self.assertIn(response.status_code, acceptable_status_codes)

    def test__specification_file_exists(self):
        """
        Test that the permission specification file exists.
        (Named with __ to ensure it runs first)
        """
        spec_file_path = get_spec_file_path()
        self.assertTrue(
            spec_file_path.exists(),
            (
                f'No permission specification file found at {spec_file_path}, please run '
                '`manage.py export_url_security_file` to generate it.'
            ),
        )

    def test_all_url_entries_are_specified(self):
        """
        Test that all url entries have a corresponding permission specification,
        and that all permission specifications have corresponding url entries.
        If this test is failing because you've added new url entries, run
        `generate_permission_spec_file.py`.
        """
        url_pattern_set = {
            (view_info.simplified_regex, view_info.name or '') for view_info in get_all_view_infos()
        }
        view_permission_spec_set = {
            (perm_spec.simplified_regex, perm_spec.pattern_name)
            for perm_spec in get_view_permission_specs()
        }
        # TODO: Break this down into two assertions so we can show a helpful message
        self.assertSetEqual(url_pattern_set, view_permission_spec_set)


"""
TODO:
- Wrap the views that are "NEEDS_FIXTURE" with a @login_required decorator or similar
  so that they return a 403 for an unauthenticated user before hitting the database
- Consider including line numbers from the permission spec file in the test output
- Some public views redirect to a public resource (favicon) and some private views redirect
  to a login page. Deal with these in assert_view_is_public and assert_view_is_not_public.
- Write a check that makes sure all url patterns have a name?
- Some kind of warning about shadowed/hidden urls that will never be reached
- Define an enum for PermissionSpec.status
- django-sql-explorer views render a login page (200) for an unauthenticated user. What do?
- Deal with POSTing to views - look for a 400? (Not going to be able to synthesise payloads)
- Take it all to the next level by defining permissions_required in PermissionSpec.
"""
