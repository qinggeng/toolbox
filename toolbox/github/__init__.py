import os
import shutil
import tempfile
import git

#################################################################################
def clone_and_copy_repo(source_url, branch, files, target_dir, github_username=None, github_password=None, github_token=None):
    """
    从 GitHub 上克隆一个仓库到本地临时目录，并将其中的某些文件和文件夹拷贝到目标目录，最后删除克隆的内容。
    @param source_url: GitHub 仓库的 URL。
    @param branch: 要克隆的分支。
    @param files: 要拷贝的文件和文件夹列表。
    @param target_dir: 目标目录。
    @param github_username: GitHub 账户的用户名。
    @param github_password: GitHub 账户的密码。
    @param github_token: GitHub 访问令牌。
    """
    # 创建本地临时目录
    temp_dir = tempfile.mkdtemp()

    try:
        # 克隆仓库到本地临时目录
        if github_username and github_password:
            git.Repo.clone_from(source_url, temp_dir, branch=branch, auth=(github_username, github_password))
        elif github_token:
            git.Repo.clone_from(source_url, temp_dir, branch=branch, auth_token=github_token)
        else:
            git.Repo.clone_from(source_url, temp_dir, branch=branch)

        # 拷贝指定文件和文件夹到目标目录
        for file in files:
            src = os.path.join(temp_dir, file)
            dst = os.path.join(target_dir, file)
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

    finally:
        # 删除本地临时目录
        shutil.rmtree(temp_dir)
