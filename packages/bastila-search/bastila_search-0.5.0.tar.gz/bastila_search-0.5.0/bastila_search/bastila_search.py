import requests
import json
import re
import sys
import fnmatch

from pathlib import Path

base_url = 'https://bastila.dev'


def load_config():
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def fetch_patterns(session):
    response = session.get(f'{base_url}/api/check/standard-changes/')
    response.raise_for_status()
    standards = response.json()

    return standards['results']


def read_gitignore():
    gitignore_paths = []
    try:
        with open('.gitignore', 'r') as f:
            for line in f:
                gitignore_paths.append(line.strip())
    except FileNotFoundError:
        print('.gitignore file not found.')
    return gitignore_paths


def is_ignored(path, gitignore_paths):
    for ignore_pattern in gitignore_paths:
        if fnmatch.fnmatch(path, ignore_pattern):
            return True
    return False


def search_files(patterns):
    results = []
    gitignore_paths = read_gitignore()

    # Loop over every pattern
    for pattern in patterns:
        # Extract file paths to search or exclude
        include_paths = pattern.get('include_paths', ['**/*'])
        exclude_paths = pattern.get('exclude_paths', [])

        snippet_instances = 0
        # Loop over every file
        for include_pattern in include_paths:
            for path in Path('.').glob(include_pattern):
                if path.is_dir():
                    continue

                # Convert Path object to string
                path_str = str(path)

                # Skip file if it is in .gitignore or in exclude_paths
                if is_ignored(path_str, gitignore_paths):
                    continue
                if any(fnmatch.fnmatch(path_str, exclude_pattern) for exclude_pattern in exclude_paths):
                    continue

                with open(path, 'rb') as f:
                    content = f.read()

                patterns_in_file = re.findall(pattern['snippet'].encode(), content)
                snippet_instances += len(patterns_in_file)

        pattern_failed = pattern['previous_count'] and (snippet_instances > pattern['previous_count'])
        results.append({
            'id': pattern['id'],
            'previous_count': pattern['previous_count'],
            'count': snippet_instances,
            'is_successful': not pattern_failed,
            'fix_recommendation': "Use {0} instead of {1}".format(pattern['fix_recommendation'], pattern['snippet'])
        })

    return results


def post_results(session, result):
    response = session.post(
        f'{base_url}/api/check/check-results/',
        data=json.dumps(result)
    )
    response.raise_for_status()
    return response


def create_check(session):
    response = session.post(
        f'{base_url}/api/check/code-checks/',
        data=json.dumps({})
    )
    response.raise_for_status()
    return response.json()


def main():
    config = load_config()

    if config is None:
        print("Configuration not found. Please run the command bastila_setup to set up the necessary parameters.")
        sys.exit(1)
    else:
        BASTILA_KEY = config["BASTILA_KEY"]
        PREVENT_REGRESSION = config["PREVENT_REGRESSION"]

    session = requests.Session()
    session.headers.update({
        'Authorization': f'Api-Key {BASTILA_KEY}',
        'Content-Type': 'application/json'
    })
    print('Starting Bastila Search')

    try:
        print('Starting check')
        create_check(session)
    except Exception as e:
        print(e)
        sys.exit(1)

    try:
        print('Fetching patterns')
        patterns = fetch_patterns(session)
    except Exception as e:
        print(e)
        sys.exit(1)

    results = []
    try:
        print('Searching files')
        results = search_files(patterns)
    except Exception as e:
        print(e)
        sys.exit(1)

    is_regression = False
    for result in results:
        if not result['is_successful']:
            print(result['fix_recommendation'])
            is_regression = True

    if is_regression:
        print('Check Failed')
        if PREVENT_REGRESSION:
            sys.exit(1)
        else:
            print('You are allowing regressions so we did not throw an error')
    else:
        print('Bastila check succeeded')
    print('Bastila check complete')


if __name__ == '__main__':
    main()
