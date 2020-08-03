from github import Github
import subprocess
import toml
import git
import sys

# args:
# 1 : repo name
# 2 : bot token

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

def open_issue_on_failure(repo_name, title, body):
    repo = Github(sys.argv[2]).get_repo(repo_name)
    issues = repo.get_issues()
    if any(i.title == title for i in issues):
        return
    repo.create_issue(title, body)


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
    open_issue_on_failure(sys.argv[1], 'Automatic upgrade has failed', s)
    exit(1)


def upgrade_and_build():
    original_deps, original_lean = get_dependencies()

    proc = subprocess.Popen(['leanproject', 'up'])
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

print('repo: ', sys.argv[1])
upgrade_and_build()