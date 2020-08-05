from github import Github
import subprocess
import toml
import git
import sys
import urllib.request

# args:
# 1 : repo name
# 2 : bot token

issue_title = 'Automatic upgrade has failed'

repo_name = sys.argv[1]
bot_token = sys.argv[2]

def get_dependencies():
    with open('leanpkg.toml', 'r') as lean_toml:
        parsed_toml = toml.loads(lean_toml.read())
        return parsed_toml['dependencies'], parsed_toml['package']['lean_version']

def error_on_upgrade(err):
    print('Error running `leanproject up.')
    print(err)
    exit(1)

def up_to_date():
    print('Nothing to upgrade: everything is up to date.')
    exit(0)

def diff_url_from_dep(old_dep, new_dep):
    repo = old_dep['git'].strip('/')
    prev = old_dep['rev']
    curr = new_dep['rev']
    return f'{repo}/compare/{prev}...{curr}'

def open_issue_on_failure(body):
    repo = Github(bot_token).get_repo(repo_name)
    issues = repo.get_issues()
    if any(i.title == issue_title for i in issues):
        return
    repo.create_issue(issue_title, body)


def error_on_build(original_deps, original_lean, new_deps, new_lean):
    print('Failure building after upgrade.')
    s = 'Oh no! We have failed to automatically upgrade your project to the latest versions of Lean and its dependencies.'
    s += '\n\nIf your project currently builds, this is probably because of changes made in its dependencies:'
    for dep_name in original_deps:
        diff_url = diff_url_from_dep(original_deps[dep_name], new_deps[dep_name])
        s += f'\n* {dep_name}: [changes]({diff_url})'
    if original_lean != new_lean:
        s += f'\n\nThe error could also be caused by upgrading Lean from {original_lean} to {new_lean}.'
    s += """\n\nYou can see the errors by running:
```bash
leanproject up
leanproject build
```"""
    open_issue_on_failure(s)
    exit(1)

def close_open_issue():
    repo = Github(sys.argv[2]).get_repo(repo_name)
    issues = [i for i in repo.get_issues() if i.title == issue_title and i.state == 'open']
    for i in issues:
        i.create_comment('This issue has been resolved!')
        i.edit(state='closed')

def leanpkg_upgrade_proc():
    with open('leanpkg.toml', 'r') as lean_toml:
        local_toml = toml.loads(lean_toml.read())
    local_lean_version = local_toml['package']['lean_version']
    urllib.request.urlretrieve('https://raw.githubusercontent.com/leanprover-community/mathlib/master/leanpkg.toml', 'mathlib_leanpkg.toml')
    with open('leanpkg.toml', 'r') as lean_toml:   
        mathlib_toml = toml.loads(lean_toml.read())
    mathlib_lean_version = mathlib_toml['package']['lean_version']
    lean_version_prefix = 'leanprover-community/lean:'
    if local_lean_version.startswith(lean_version_prefix) and mathlib_lean_version.startswith(lean_version_prefix):
        local_lean_version_int = [int(i) for i in local_lean_version[len(lean_version_prefix):].split('.')]
        mathlib_lean_version_int = [int(i) for i in mathlib_lean_version[len(lean_version_prefix):].split('.')]
        if mathlib_lean_version_int > local_lean_version_int:
            local_toml['package']['lean_version'] = mathlib_lean_version
            with open('leanpkg.toml', 'w') as lean_toml:
                toml.dump(local_toml, lean_toml)
    return subprocess.Popen(['leanpkg', 'upgrade'])

def upgrade_and_build():
    original_deps, original_lean = get_dependencies()

    if 'mathlib' in original_deps:
        proc = subprocess.Popen(['leanproject', 'up'])
    else:
        proc = leanpkg_upgrade_proc()
    out, err = proc.communicate()

    if proc.returncode != 0:
        error_on_upgrade(err)

    new_deps, new_lean = get_dependencies()

    if new_deps == original_deps:
        up_to_date()

    proc = subprocess.Popen(['leanpkg', 'build'])
    out, err = proc.communicate()

    if proc.returncode != 0:
        error_on_build(original_deps, original_lean, new_deps, new_lean)
        return

    close_open_issue()

upgrade_and_build()