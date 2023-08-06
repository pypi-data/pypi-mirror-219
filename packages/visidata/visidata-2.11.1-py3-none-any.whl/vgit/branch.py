import re

from visidata import vd, Column, VisiData, ItemColumn, AttrColumn, Path, AttrDict, RowColorizer, date, Progress

from .gitsheet import GitSheet

vd.option('color_git_current_branch', 'underline', 'color of current branch on branches sheet')
vd.option('color_git_remote_branch', 'cyan', 'color of remote branches on branches sheet')


@VisiData.api
def git_branch(vd, args):
    nonListArgs = '--track --no-track --set-upstream-to -u --unset-upstream -m -M -c -C -d -D --edit-description'.split()
    if any(x in args for x in nonListArgs):
        return

    return GitBranch('git-branch-list', source=Path('.'), git_args=args)


def _remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


class GitBranchNameColumn(Column):
    def calcValue(self, row):
        return _remove_prefix(row.localbranch, 'remotes/')

    def putValue(self, row, val):
        self.sheet.loggit('branch', '-v', '--move', row.localbranch, val)


class GitBranch(GitSheet):
    help = '''
        # git branch
        List of all branches, including relevant metadata.

        - `d` to mark a branch for deletion
        - `e` on the _branch_ column to rename the branch
        - `z Ctrl+S` to commit changes
    '''
    defer = True
    rowtype = 'branches'  # rowdef: AttrDict from regex (in reload below)
    columns = [
        GitBranchNameColumn('branch', width=20),
#        Column('remote', getter=lambda c,r: r['localbranch'].startswith('remotes/') and '*' or '', width=3),
        ItemColumn('head_commitid', 'refid', width=0),
        ItemColumn('tracking', 'remotebranch'),
        ItemColumn('upstream'),
        ItemColumn('merge_base', 'merge_name', width=20),
        ItemColumn('extra', width=0),
        ItemColumn('head_commitmsg', 'msg', width=50),
        ItemColumn('last_commit', type=date),
        ItemColumn('last_author'),
    ]
    colorizers = [
        RowColorizer(10, 'color_git_current_branch', lambda s,c,r,v: r and r['current']),
        RowColorizer(10, 'color_git_remote_branch', lambda s,c,r,v: r and r['localbranch'].startswith('remotes/')),
    ]
    nKeys = 1

    def iterload(self):
        branches_lines = self.git_lines('branch',
                                        '--list',
                                        '-vv',
                                        '--no-color',
                                        *self.git_args)
        for line in branches_lines:
            if '->' in line:
                continue

            m = re.match(r'''(?P<current>\*?)\s+
                             (?P<localbranch>\S+)\s+
                             (?P<refid>\w+)\s+
                             (?:\[
                               (?P<remotebranch>[^\s\]:]+):?
                               \s*(?P<extra>.*?)
                             \])?
                             \s*(?P<msg>.*)''', line, re.VERBOSE)
            if m:
                yield AttrDict(m.groupdict())

        branch_stats = self.gitRootSheet.gitBranchStatuses
        for row in Progress(self.rows):
            merge_base = self.git_all("show-branch", "--merge-base", row.localbranch, self.gitRootSheet.branch, _ok_code=[0,1]).strip()
            row.update(dict(
                merge_name = self.git_all("name-rev", "--name-only", merge_base).strip() if merge_base else '',
                upstream = branch_stats.get(row.localbranch),
                last_commit = self.git_all("show", "--no-patch", '--pretty=%ai', row.localbranch).strip(),
                last_author = self.git_all("show", "--no-patch", '--pretty=%an', row.localbranch).strip()
            ))

    def commitAddRow(self, row):
        self.loggit('branch', row.localbranch)

    def commitDeleteRow(self, row):
        self.loggit('branch', '--delete', _remove_prefix(row.localbranch, 'remotes/'))


@GitSheet.lazy_property
def gitBranchStatuses(sheet):
    ret = {}  # localbranchname -> "+5/-2"
    for branch_status in sheet.git_lines('for-each-ref', '--format=%(refname:short) %(upstream:short) %(upstream:track)', 'refs/heads'):
        m = re.search(r'''(\S+)\s*
                          (\S+)?\s*
                          (\[
                          (ahead.(\d+)),?\s*
                          (behind.(\d+))?
                          \])?''', branch_status, re.VERBOSE)
        if not m:
            vd.status('unmatched branch status: ' + branch_status)
            continue

        localb, remoteb, _, _, nahead, _, nbehind = m.groups()
        if nahead:
            r = '+%s' % nahead
        else:
            r = ''
        if nbehind:
            if r:
                r += '/'
            r += '-%s' % nbehind
        ret[localb] = r

    return ret


GitSheet.addCommand('', 'git-branch-create', 'git("branch", input("create branch: ", type="branch"))', 'create a new branch off the current checkout')
GitBranch.addCommand('', 'git-branch-checkout', 'git("checkout", cursorRow.localbranch)', 'checkout this branch')


vd.addMenuItems('''
    Git > Branch > add > git-branch-create
    Git > Branch > delete > git-branch-delete
    Git > Branch > rename > git-branch-rename
    Git > Branch > checkout > git-branch-checkout
''')
