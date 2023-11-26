# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-11-26
#
# ====================================================


from typing import List
from mod.common.minecraftEnum import ItemPosType


def clear_items(player_id: str, item_pos_type: int, pos: int) -> dict: ...
def get_item_pos(
    entity_id: str,
    pos_type: int,
    item_id: str,
    item_aux: int = -1,
    count: int = 1,
) -> List[int]: ...
def change_item_count(
    player_id: str,
    pos_type: int = ItemPosType.CARRIED,
    pos: int = 0,
    change: int = -1,
) -> None: ...
def deduct_inv_item(player_id: str, name: str, aux: int = -1, count: int = 1) -> bool: ...















