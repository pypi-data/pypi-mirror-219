# Copyright 2023 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from tests import *
from unify.properties import Properties, ClusterSetting

class TestProperties(unittest.TestCase):

    def test_singleton_memory(self):
        """Ensure singleton for a single ClusterSetting type"""

        p1 = Properties(ClusterSetting.MEMORY)
        p2 = Properties(ClusterSetting.MEMORY)

        self.assertEqual(
            id(p1),
            id(p2),
            msg='Properties p1 and p2 do not point to the same object'
        )

    def test_singleton_memory_and_file(self):
        """Ensure singleton for multiple ClusterSetting types"""

        p1 = Properties(ClusterSetting.MEMORY)
        p2 = Properties(ClusterSetting.MEMORY)

        self.assertEqual(id(p1), id(p2),
            msg='Properties(MEMORY) and Properties(MEMORY) not the same object')

        p3 = Properties(ClusterSetting.FILE)

        self.assertNotEqual(id(p1), id(p3),
            msg='Properties(FILE) and Properties(MEMORY) _are_ the same object')

        p4 = Properties(ClusterSetting.FILE)
        self.assertEqual(id(p3), id(p4),
            msg='Properties(FILE) and Properties(FILE) not the same object')

    def test_store_cluster(self):
        """When multiple Properties are created, store_cluster() works as expected"""
        p1 = Properties(ClusterSetting.MEMORY)

        old_len = len(p1.clusters)

        p1.store_cluster('sean@ean.io', 'fakepassword1', 'https://bogus.ean.io/', name='bogus1')

        self.assertEqual(len(p1.clusters), old_len + 1, msg='Ensure exactly one new cluster stored')

        p2 = Properties(ClusterSetting.MEMORY)
        p2.store_cluster('sean@ean.io', 'fakepassword2', 'https://bogus2.ean.io/', name='bogus2')

        self.assertEqual(len(p1.clusters), old_len + 2, msg='Ensure exactly two new clusters stored')

