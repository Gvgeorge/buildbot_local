# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from twisted.trial import unittest

from buildbot import config
from buildbot.process.results import FAILURE
from buildbot.process.results import SUCCESS
from buildbot.steps import maxq
from buildbot.test.fake.remotecommand import ExpectShell
from buildbot.test.util import steps
from buildbot.test.util.misc import TestReactorMixin


class TestShellCommandExecution(steps.BuildStepMixin, TestReactorMixin,
                                unittest.TestCase):

    def setUp(self):
        self.setUpTestReactor()
        return self.setup_build_step()

    def tearDown(self):
        return self.tear_down_build_step()

    def test_testdir_required(self):
        with self.assertRaises(config.ConfigErrors):
            maxq.MaxQ()

    def test_success(self):
        self.setup_step(
            maxq.MaxQ(testdir='x'))
        self.expectCommands(
            ExpectShell(workdir='wkdir', command=["run_maxq.py", "x"])
            .stdout('no failures\n')
            .exit(0)
        )
        self.expectOutcome(result=SUCCESS, state_string='success')
        return self.run_step()

    def test_nonzero_rc_no_failures(self):
        self.setup_step(
            maxq.MaxQ(testdir='x'))
        self.expectCommands(
            ExpectShell(workdir='wkdir', command=["run_maxq.py", "x"])
            .stdout('no failures\n')
            .exit(2)
        )
        self.expectOutcome(result=FAILURE,
                           state_string='1 maxq failures')
        return self.run_step()

    def test_failures(self):
        self.setup_step(
            maxq.MaxQ(testdir='x'))
        self.expectCommands(
            ExpectShell(workdir='wkdir', command=["run_maxq.py", "x"])
            .stdout('\nTEST FAILURE: foo\n' * 10)
            .exit(2)
        )
        self.expectOutcome(result=FAILURE,
                           state_string='10 maxq failures')
        return self.run_step()
