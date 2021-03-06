# -*- coding: utf-8 -*-
# Copyright (c) 2020 Salvador E. Tropea
# Copyright (c) 2020 Instituto Nacional de Tecnologïa Industrial
# License: Apache 2.0
# Project: KiAuto (formerly kicad-automation-scripts)
"""
Tests for eeschema_do miscellaneous stuff.

For debug information use:
pytest-3 --log-cli-level debug

"""

import os
import sys
import logging
# Look for the 'utils' module from where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))
prev_dir = os.path.dirname(script_dir)
sys.path.insert(0, prev_dir)
# Utils import
from utils import context
sys.path.insert(0, os.path.dirname(prev_dir))
from kiauto.misc import (EESCHEMA_CFG_PRESENT, KICAD_CFG_PRESENT, NO_SCHEMATIC, WRONG_SCH_NAME, EESCHEMA_ERROR,
                         WRONG_ARGUMENTS)

PROG = 'eeschema_do'
BOGUS_SCH = 'bogus.sch'


def test_eeschema_config_backup():
    """ Here we test the extreme situation that a previous run left a config
        back-up and the user must take action. """
    prj = 'good-project'
    ctx = context.TestContextSCH('Eeschema_config_bkp', prj)
    # Create a fake back-up
    if not os.path.isdir(ctx.kicad_cfg_dir):
        logging.debug('Creating KiCad config dir')
        os.makedirs(ctx.kicad_cfg_dir, exist_ok=True)
    old_config_file = ctx.eeschema_conf + '.pre_script'
    logging.debug('Eeschema old config: '+old_config_file)
    with open(old_config_file, 'wt') as f:
        f.write('Dummy back-up\n')
    # Run the command
    cmd = [PROG, 'run_erc']
    ctx.run(cmd, EESCHEMA_CFG_PRESENT)
    os.remove(old_config_file)
    m = ctx.search_err('Eeschema config back-up found')
    assert m is not None
    ctx.clean_up()


def test_kicad_common_config_backup():
    """ Here we test the extreme situation that a previous run left a config
        back-up and the user must take action. """
    prj = 'good-project'
    ctx = context.TestContextSCH('Eeschema_common_config_bkp', prj)
    # Create a fake back-up
    if not os.path.isdir(ctx.kicad_cfg_dir):
        logging.debug('Creating KiCad config dir')
        os.makedirs(ctx.kicad_cfg_dir, exist_ok=True)
    old_config_file = ctx.kicad_conf + '.pre_script'
    logging.debug('KiCad common old config: '+old_config_file)
    with open(old_config_file, 'wt') as f:
        f.write('Dummy back-up\n')
    # Run the command
    cmd = [PROG, 'run_erc']
    ctx.run(cmd, KICAD_CFG_PRESENT)
    os.remove(old_config_file)
    m = ctx.search_err('KiCad common config back-up found')
    assert m is not None
    ctx.clean_up()


def test_sch_not_found():
    """ When the provided .sch isn't there """
    prj = 'good-project'
    ctx = context.TestContextSCH('Schematic_not_found', prj)
    cmd = [PROG, 'run_erc']
    ctx.run(cmd, NO_SCHEMATIC, filename='dummy')
    m = ctx.search_err(r'ERROR:.* does not exist')
    assert m is not None
    ctx.clean_up()


def test_sch_no_extension():
    """ KiCad can't load a schematic file without extension """
    prj = 'good-project'
    ctx = context.TestContextSCH('SCH_no_extension', prj)
    cmd = [PROG, 'run_erc']
    ctx.run(cmd, WRONG_SCH_NAME, filename='Makefile')
    m = ctx.search_err(r'Input files must use an extension')
    assert m is not None
    ctx.clean_up()


def test_bogus_sch():
    """ A broken SCH file """
    ctx = context.TestContextSCH('Bogus_SCH', 'good-project')
    # Current KiCad 5.99 (20201125) creates the warning dialog, but doesn't give it focus.
    # So we never know about the problem.
    if ctx.kicad_version < context.KICAD_VERSION_5_99:
        sch = ctx.get_out_path(BOGUS_SCH)
        # Create an invalid SCH
        with open(sch, 'w') as f:
            f.write('dummy')
        cmd = [PROG, '-vv', '-r', 'run_erc']
        ctx.run(cmd, EESCHEMA_ERROR, filename=sch)
        assert ctx.search_err(r"eeschema reported an error") is not None
    ctx.clean_up()


def test_sch_wrong_command():
    """ Wrong command line arguments """
    ctx = context.TestContextSCH('SCH_Wrong_Command', 'good-project')
    cmd = [PROG, 'bogus']
    ctx.run(cmd, WRONG_ARGUMENTS)
    ctx.clean_up()
