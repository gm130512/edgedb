#
# This source file is part of the EdgeDB open source project.
#
# Copyright 2019-present MagicStack Inc. and the EdgeDB authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import edgedb

from edb.testbase import server as tb


class TestEdgeQLSys(tb.QueryTestCase):

    ISOLATED_METHODS = False

    async def test_edgeql_sys_locks(self):
        with self.assertRaisesRegex(edgedb.InternalServerError,
                                    "key is expected to be >= 0"):
            await self.con.execute('select sys::advisory_lock(-1)')

        with self.assertRaisesRegex(edgedb.InternalServerError,
                                    "key is expected to be >= 0"):
            await self.con.execute('select sys::advisory_unlock(-1)')

        self.assertEqual(
            await self.con.fetch('select sys::advisory_unlock(10000)'),
            [False])

        await self.con.execute('select sys::advisory_lock(10000)')

        self.assertEqual(
            await self.con.fetch('select sys::advisory_unlock(10000)'),
            [True])
        self.assertEqual(
            await self.con.fetch('select sys::advisory_unlock(10000)'),
            [False])