#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

import os
from tabulate import tabulate

from mlt.commands import Command
from mlt.utils import git_helpers
from mlt.utils.constants import TEMPLATES_DIR


class TemplatesCommand(Command):
    def action(self):
        """lists templates available"""
        template_repo = self.args["--template-repo"]
        with git_helpers.clone_repo(template_repo) as temp_clone:
            templates_directory = os.path.join(temp_clone, TEMPLATES_DIR)
            templates = self._parse_templates(templates_directory)
            if not templates:
                if template_repo.startswith("git@") or \
                   template_repo.startswith("https://"):
                    print("Please verify git is installed and setup "
                          "properly and you have read access to the repo.")
                else:
                    print("Please make sure template repo directory exists "
                          "and you have read access to the directory.")
            else:
                print(tabulate(templates,
                               headers=['Template', 'Version', 'Description'],
                               tablefmt="simple"))

    def _parse_templates(self, templates_directory):
        """parses template dirs in sorted order, pulling data from READMEs"""
        result = []
        if not os.path.exists(templates_directory):
            return result
        for filename in sorted(os.listdir(templates_directory)):
            if not os.path.isdir(filename):
                continue
            description = '<none>'
            version = '<none>'
            readme_file = os.path.join(
                templates_directory, filename, "README.md")
            version_file = os.path.join(
                templates_directory, filename, "version.txt")
            if os.path.isfile(readme_file):
                with open(readme_file) as f:
                    for line in f:
                        line = line.strip()
                        if not line or line[0] == '#':
                            continue
                        description = line
                        break
            if os.path.isfile(version_file):
                with open(version_file) as f:
                    version = f.readline().strip()
            result.append([filename, version, description])
        return result
