from __future__ import annotations

import ckan.plugins.toolkit as tk


def get_actions():
    return {
        "iso19115_package_show": package_show,
    }


def package_show(context, data_dict):
    pkg = tk.get_action("package_show")(context, data_dict)
    return pkg
