import os
import subprocess

# git pullして成功ならbranch+trueを返す
def git_pull():
    cwd = os.path.dirname(os.path.abspath(__file__))
    # リポジトリのパスを取得
    repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=cwd).strip().decode('utf-8')
    # branch名を取得
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_root).strip().decode('utf-8')

    try:
        subprocess.check_call(['git', 'pull'], cwd=repo_root)
        return branch, True
    except subprocess.CalledProcessError:
        return branch, False
