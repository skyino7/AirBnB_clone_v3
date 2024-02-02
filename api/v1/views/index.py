#!/usr/bin/python3
"""Views for the index"""

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status"""
    return {
        "status": "OK",
    }
