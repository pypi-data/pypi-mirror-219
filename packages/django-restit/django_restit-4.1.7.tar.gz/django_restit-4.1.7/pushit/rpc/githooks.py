from rest import decorators as rd
from rest import views as rv
from rest import settings
from rest import helpers as rh
from taskqueue.models import Task
from pushit import utils
import time


@rd.urlPOST('hooks/git_update')
def rest_on_git_hook(request):
    sec_key = request.DATA.get("token")
    git_key = settings.get("GIT_KEY", "hookswhat")
    hook_request = None

    req_key = request.DATA.getHeader("HTTP_X_GITLAB_TOKEN")
    if req_key is not None:
        hook_request = utils.parseGitLab(request)
    else:
        req_key = request.DATA.getHeader("HTTP_X_HUB_SIGNATURE_256")
        if req_key is not None:
            hook_request = utils.parseGithub(request)    

    if sec_key != git_key and req_key is None:
        rh.error("GIT HOOK NO TOKEN", request.META)
        return rv.restPermissionDenied(request)

    git_projects = settings.get("GIT_PROJECTS", None)

    if hook_request.name not in git_projects:
        return rv.restStatus(request, False, error="no config for project")

    proj_info = utils.getProjectForBranch(git_projects.get(hook_request.name), hook_request.branch)
    if proj_info is None:
        return rv.restStatus(request, False, error="no branch for project")

    if hook_request.kind == "push":
        on_git_push_request(proj_info, hook_request)

    return rv.restStatus(request, True)


def on_git_push_request(info, hook_request):
    branch = info.get("branch")
    cmd = info.get("updater")
    use_tq = info.get("use_tq", False)

    if use_tq:
        data = dict(branch=branch, update_cmd=cmd)
        Task.Publish("pushit", "run_update", data, channel="tq_updater")
    else:
        asyncUpdater(cmd, branch)


@rd.rest_async
def asyncUpdater(cmd, branch):
    import random
    # randomize the hit so we avoid collisions (gitlabs issues)
    time.sleep(random.randint(2, 15))
    utils.updateCode(cmd, branch)

