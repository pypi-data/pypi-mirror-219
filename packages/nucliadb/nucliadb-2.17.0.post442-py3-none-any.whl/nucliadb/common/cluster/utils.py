# Copyright (C) 2021 Bosutech XXI S.L.
#
# nucliadb is offered under the AGPL v3.0 and as commercial software.
# For commercial licensing, contact us at info@nuclia.com.
#
# AGPL:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
from typing import Optional, Union

from nucliadb.common.cluster.chitchat import (
    ChitchatMonitor,
    start_chitchat,
    stop_chitchat,
)
from nucliadb.common.cluster.manager import KBShardManager, StandaloneKBShardManager
from nucliadb_utils.utilities import Utility, clean_utility, get_utility, set_utility

from .settings import settings


async def setup_cluster(
    service_name: str,
) -> Union[KBShardManager, StandaloneKBShardManager]:
    await start_chitchat(service_name)
    mng: Union[KBShardManager, StandaloneKBShardManager]
    if settings.standalone_mode:
        mng = StandaloneKBShardManager()
    else:
        mng = KBShardManager()
    set_utility(Utility.SHARD_MANAGER, mng)
    return mng


async def teardown_cluster():
    await stop_chitchat()
    if get_utility(Utility.SHARD_MANAGER):
        clean_utility(Utility.SHARD_MANAGER)


def get_shard_manager() -> KBShardManager:
    return get_utility(Utility.SHARD_MANAGER)  # type: ignore


def get_chitchat() -> Optional[ChitchatMonitor]:
    return get_utility(Utility.CHITCHAT)
