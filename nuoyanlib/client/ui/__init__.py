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
#   Last Modified : 2025-01-29
#
# ====================================================


"""
nuoyanlib UI库。
"""


from ..._core._sys import is_client
if not is_client():
    raise ImportError("Cannot import nuoyanlib.client.ui in server environment.")
del is_client


from ..._core._client._comp import (
    ScreenNode,
    ViewBinder,
    ViewRequest,
)


from .item_fly_anim import *
from .item_grid_manager import *
from .item_tips_box import *
from .screen_node import *
from .ui_utils import *
