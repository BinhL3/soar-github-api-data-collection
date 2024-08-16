# Data Collection

GitHub API - Data Collection task. Write modular and robust code. We should be able to easily review and reuse the code. Try to store the information in a spreadsheet if you can .

Example Repository: [Pandas](https://github.com/pandas-dev/pandas)
[GitHub Advisory Database](https://github.com/advisories)

Get the following:

Number of stars, forks, and watches

Total Line of Code (LoC) in the project

All the used languages

LoC per language

Number of files per language

Total number of contributors

Identify the core developers:

The core developers are the ones who's merged commits make up 80% of the merged commits. If the top 4 contributors are responsible for the 80% of the changes in the project, these 4 are the core contributors.

List of all the identified CVEs and CWEs found in the project’s history and the relevant information about them: [example of an entry](https://github.com/advisories/GHSA-pcwp-26pw-j98w) It’s all possible through the [API](https://docs.github.com/en/rest/security-advisories/global-advisories?apiVersion=2022-11-28). Some of the information can be:

The CVE, CWE, and GHSA IDs.

Vulnerability Severity and base metrics

Description

Affected file and code

Person committing the code, the time of the commit, com
