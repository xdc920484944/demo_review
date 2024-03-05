from openai import OpenAI
import requests
from config import GPT_KEY
# 设置你的API密钥
model = "gpt-3.5-turbo-0125"

# 设置 GitHub API 的基本 URL 和要获取提交的存储库信息
# 小改一点点，第八行修改
base_url = 'https://api.github.com'
owner = 'xdc920484944'  # 存储库所有者的用户名
repo = 'Graduation-project'  # 存储库的名称


def send_2_tpg():
    client = OpenAI(api_key=GPT_KEY)

    content = '你能审核python代码并对其进行优化吗'

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


def get_all_commits():
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = [commit["sha"] for commit in response.json()]
        return commits
    else:
        print("Error:", response.status_code)
        return None


def get_commit_changes(owner, repo, commit_sha):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_data = response.json()
        changes = []
        for file in commit_data["files"]:
            file_name = file["filename"]
            diff_url = file["raw_url"]
            diff_response = requests.get(diff_url)
            if diff_response.status_code == 200:
                diff_text = diff_response.text
                changes.append({"file_name": file_name, "diff": diff_text})
            else:
                print(f"Failed to fetch diff for {file_name}: {diff_response.status_code}")
        return changes
    else:
        print("Error:", response.status_code)
        return None


if __name__ == '__main__':
    # 获取sha
    # commits = get_all_commits()
    # if commits:
    #     print("All commit SHAs:", commits)
    # 获取变更代码位置
    commit_sha = '0e1b8995d220446b790f18a7fa42e31b21bfa1b3'
    files_changed = get_commit_changes(owner, repo, commit_sha)
    if files_changed:
        print("Files changed in commit:", files_changed)
