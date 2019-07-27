import json
import logging
from collections import Counter

import flask
from flask import Response, jsonify
from fetch import github_profile, bitbucket_profile


app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)

@app.route("/org-profile/<org>", methods=["GET"])
def org_profile(org):
    """
    Endpoint to health check API
    """
    app.logger.info("profile for %s", org)
    data = {
        'github_profile': github_profile(org=org),
        'bitbucket_profile': bitbucket_profile(org=org)
    }
    # create a shortcut way to access the actual profile data to work with
    gh_profile = data['github_profile']['profile']
    bb_profile = data['bitbucket_profile']['profile']
    merged_profile = {
        'total_watchers_count': sum([
            bb_profile['total_watchers_count'],
            gh_profile['total_watchers_count']]),
        'total_repo_count': sum([
            bb_profile['repo_count'],
            gh_profile['orig_vs_forked_count']['original'],
            gh_profile['orig_vs_forked_count']['forked']]),
        'languages': gh_profile['languages'] + bb_profile['languages']
    }
    data['merged_profile'] = merged_profile
    app.logger.info("data %s", json.dumps(data, indent=4))
    return json.dumps(data), {'Content-Type': 'application/json'}
