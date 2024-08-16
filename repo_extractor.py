import requests
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

headers = {'Authorization': f'token {os.environ.get("ACCESS_TOKEN")}'}

GITHUB_API_BASE_URL = "https://api.github.com"

EXTENSION_TO_LANGUAGE = {
    'py': 'Python',
    'pyx': 'Cython',
    'c': 'C',
    'h': 'C',
    'js': 'JavaScript',
    'html': 'HTML',
    'htm': 'HTML',
    'sh': 'Shell',
    'meson': 'Meson',
    'tpl': 'Smarty',
    'css': 'CSS',
    'dockerfile': 'Dockerfile',
    'xslt': 'XSLT',
}

def get_total_contributors(owner, repo):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/contributors?per_page=1&anon=true"
    response = requests.get(url, headers=headers)
    if 'Link' in response.headers:
        last_page_url = response.headers['Link'].split(',')[1].split(';')[0].strip()[1:-1]
        last_page_number = int(last_page_url.split('=')[-1])
        return last_page_number
    else:
        return len(response.json())

def get_contributors_commits(owner, repo):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/contributors?per_page=100&anon=true"
    contributors = []
    while url:
        response = requests.get(url, headers=headers)
        contributors.extend(response.json())
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    return contributors

def identify_core_developers(contributors):
    contributors_filtered = [
        contrib for contrib in contributors
        if contrib.get('type') != 'Anonymous' and 'contributions' in contrib
    ]
    
    contributors_sorted = sorted(contributors_filtered, key=lambda x: x['contributions'], reverse=True)
    
    total_commits = sum(contrib['contributions'] for contrib in contributors_sorted)
    core_devs = []
    commits_accumulated = 0
    
    for contrib in contributors_sorted:
        login = contrib.get('login') or contrib.get('name') or contrib.get('email', 'Unknown')
        core_devs.append({
            "login": login,
            "commits": contrib['contributions']
        })
        commits_accumulated += contrib['contributions']
        if commits_accumulated / total_commits >= 0.8:
            break

    return core_devs


def get_language_stats(owner, repo):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=headers)
    languages = response.json()

    files_per_language = {lang: 0 for lang in languages.keys()}

    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(url, headers=headers)
    files = response.json().get("tree", [])

    for file in files:
        if file["type"] == "blob":
            extension = file["path"].split('.')[-1].lower()
            language = EXTENSION_TO_LANGUAGE.get(extension)

            if language and language in files_per_language:
                files_per_language[language] += 1

    return languages, files_per_language

def extract_info(owner, repo):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception("Invalid route")
    data = response.json()

    total_contributors = get_total_contributors(owner, repo)    
    contributors = get_contributors_commits(owner, repo)
    core_developers = identify_core_developers(contributors)

    languages, files_per_language = get_language_stats(owner, repo)
    total_loc = sum([languages[i] for i in languages])

    info = {
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("watchers_count"),
        "languages": languages,
        "files_per_language": files_per_language,
        "total_loc": total_loc,
        "total_contributors": total_contributors,
        "core_developers": core_developers,
        "core_developers_num": len(core_developers),
    }

    return info

info = extract_info("pandas-dev", "pandas")
#print(json.dumps(info, indent=2))

with open("./info.json", "w") as outfile: 
    json.dump(info, outfile, indent=2)