# -*- coding: utf-8 -*-

from acore_paths import api


def test():
    _ = api

    _ = api.dir_home
    _ = api.dir_azeroth_server
    _ = api.dir_server_bin
    _ = api.path_azeroth_server_authserver_conf_dist
    _ = api.path_azeroth_server_worldserver_conf_dist
    _ = api.path_azeroth_server_authserver_conf
    _ = api.path_azeroth_server_worldserver_conf
    _ = api.dir_azeroth_server_data
    _ = api.dir_azeroth_server_data_dot_zip
    _ = api.dir_azeroth_server_logs
    _ = api.dir_modules
    _ = api.path_mod_eluna_conf_dist
    _ = api.path_mod_eluna_conf
    _ = api.dir_server_lua_scripts
    _ = api.dir_git_repos
    _ = api.dir_acore_soap_app_project
    _ = api.path_acore_soap_app_cli
    _ = api.dir_acore_db_app_project
    _ = api.path_acore_db_app_cli
    _ = api.dir_acore_server_bootstrap_project
    _ = api.path_acore_server_bootstrap_cli


if __name__ == "__main__":
    from acore_paths.tests import run_cov_test

    run_cov_test(__file__, "acore_paths.api", preview=False)
