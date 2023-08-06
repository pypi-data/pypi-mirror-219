#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for all cli commands"""


import pytest

# # from argtoolbox import DefaultProgram
# from pyfmsync.commands import PROG
#
#
# @pytest.fixture()
# def cli():
#     """TODO"""
#     PROG.add_config_options()
#     PROG.config.config_file = "test-pyfmsync.cfg"
#     PROG.load()
#     PROG.init_parser()
#     PROG.add_pre_commands()
#     PROG.reload()
#     PROG.add_commands()
#     return PROG
#
#
# class CommandProvider:
#     """Provide ids and values for fixture."""
#
#     data = [
#         ["guess", "Dark.S01.MULTi.1080p.WEB-DL.x264-Polygon"],
#         ["boards", "list"],
#         ["columns", "5e84f440e1288b0d394ddf44", "list"],
#         ["labels", "5e84f440e1288b0d394ddf44", "list"],
#         ["cards", "5e84f440e1288b0d394ddf44", "list"],
#         ["members", "5e84f440e1288b0d394ddf44", "list"],
#         ["actions", "5e84f440e1288b0d394ddf44", "list"],
#         ["client", "list"],
#         ["client", "undownloaded"],
#         ["client", "sync-checklists"],
#         ["client", "add-comment", "5f2ff8e23e1569173cb151e9", "coucou"],
#         ["server", "sync-checklists"],
#         ["server", "add", "-f", "Dark.S01.MULTi.1080p.WEB-DL.x264"],
#         ["client", "list", "Dark - Season 1", "--archive"],
#     ]
#
#     @classmethod
#     def get_ids(cls):
#         """Return param ids"""
#         for row in cls.data:
#             yield "-".join(row)
#
#     @classmethod
#     def get_params(cls):
#         """Return param values"""
#         return cls.data
#
#
# @pytest.fixture(
#     params=CommandProvider.get_params(),
#     ids=CommandProvider.get_ids())
# def command(request):
#     """TODO"""
#     return request.param
#
#
# def test_list(cli, command):
#     """TODO"""
#     args = cli.parser.parse_args(command)
#     assert hasattr(args, '__func__')
#     assert args.__func__(args)
#
#
# def test_list_actions(cli, caplog):
#     """TODO"""
#     args = cli.parser.parse_args(
#         ["actions", "5e84f440e1288b0d394ddf44", "list"])
#     assert hasattr(args, '__func__')
#     assert args.__func__(args)
#     print(caplog.record_tuples)
#     captured = filter(
#         lambda x: "Missing cell rendering for" in x[2],
#         caplog.record_tuples)
#     if captured:
#         pytest.xfail("Missing cell rendering")
#
#
# def run(cli, command):
#     """TODO"""
#     args = cli.parser.parse_args(command)
#     assert args.__func__(args)
#
#
# def test_complex_card_scenario(cli, capsys):
#     """TODO"""
#     run(cli, ["server", "add", "automated-test-card"])
#     run(cli, ["client", "list", "--cli", "automated-test-card"])
#     captured = capsys.readouterr()
#     print(captured)
#     card_id = captured.out.strip('\n')
#     print("card_id:", card_id)
#     assert card_id
#     cmd = ["client", "add-comment"]
#     cmd.append(card_id)
#     cmd.append("coucou")
#     run(cli, cmd)
#     cmd = ["server", "update"]
#     cmd.append(card_id)
#     cmd.append("--clean")
#     cmd.append("--override-name")
#     cmd.append("automated-test-card")
#     run(cli, cmd)
#     run(cli, ["client", "list", "--archive", "automated-test-card"])
