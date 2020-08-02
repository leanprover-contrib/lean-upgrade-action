import subprocess
import toml
import git 

def get_dependencies():
    with open('leanpkg.toml', 'r') as lean_toml:
        parsed_toml = toml.loads(lean_toml.read())
        return parsed_toml['dependencies'], parsed_toml['package']['lean_version']

def error_on_upgrade(err):
    pass

def up_to_date():
    pass

def diff_url_from_dep(old_dep, new_dep):
    repo = old_dep['git'].strip('/')
    prev = old_dep['rev']
    curr = new_dep['rev']
    return f'{repo}/compare/{prev}...{curr}'

def error_on_build(original_deps, original_lean, new_deps, new_lean):
    print('Failure building after upgrade.')
    s = 'Oh no! We have failed to automatically upgrade your project to the latest versions of Lean and its dependencies.'

def upgrade_and_build():
    original_deps, original_lean = get_dependencies()

    proc = subprocess.Popen(['leanproject', 'upgrade'])
    out, err = proc.communicate()

    if proc.returncode != 0:
        error_on_upgrade(err)
        return

    new_deps, new_lean = get_dependencies()

    if new_deps == original_deps:
        up_to_date()
        return 

    proc = subprocess.Popen(['leanpkg', 'build'])
    out, err = proc.communicate() 

    if proc.returncode != 0:
        error_on_build(original_deps, original_lean, new_deps, new_lean)
        return 

    def report_issue(self, version_history, mathlib_prev = None):
        if self.is_new:
            version_key = remote_ref_from_lean_version(self.version)
            ppversion = '.'.join(str(s) for s in self.version)
            project = projects[self.project]
            branch_url = f'https://github.com/{project.organization}/{self.project}/tree/lean-{ppversion}'
            mathlib_curr = version_history[version_key]['mathlib']['latest_test']
            # if mathlib_prev is not None and mathlib_prev != :
            git_diff_url = f'https://github.com/leanprover-community/mathlib/compare/{mathlib_prev}...{mathlib_curr}' \
                if mathlib_prev is not None and mathlib_prev != mathlib_curr \
                else None

            s = \
f"""This is an automated message from the [leanprover-contrib](https://github.com/leanprover-contrib/leanprover-contrib) repository.

Your project's [lean-{ppversion}]({branch_url}) branch has failed to build with recent updates to mathlib and/or its other dependencies."""

            if git_diff_url is not None:
                s += f'\n\nThis is often due to changes in mathlib, but could also happen due to changes in other dependencies or your own changes to your branch. '
                s += f'If it is due to mathlib, the conflicting changes occur in [this range]({git_diff_url}).'

            s += f'\n\nThe failure occurred using Lean version {ppversion}.'
            if self.traceback is not None:
                s += f'\n\nThis failure may have been caused by a failure in the {self.find_trans_fail().project} on which your project depends.'
            issue = github_reports.open_issue_on_failure(
                f'{project.organization}/{self.project}',
                f'Build failure on automatic dependency update on `lean-{ppversion}`',
                s,
                project.owners)
            version_history[version_key][self.project]['issue'] = issue