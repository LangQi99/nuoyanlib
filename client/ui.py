# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Email         : 1279735247@qq.com
#   Last Modified : 2023-01-13
#
# ====================================================


from ..mctypes.client.ui.screenNode import ScreenNode as _ScreenNode


# noinspection PyUnresolvedReferences
def get_ui_screen_pos(instance, path):
    # type: (_ScreenNode, str) -> tuple[float, float]
    """
    获取控件在屏幕上的坐标（而不是相对于父控件的坐标）。
    该函数获取的坐标以控件左上角为锚点。
    示例：
    from ...nuoyanLib.client.ui import get_ui_screen_pos
    class MyUi(ScreenNode):
        def __init__(self, namespace, name, param):
            pass
        def Create(self):
            btnPath = "/panel/button"
            btnPos = get_ui_screen_pos(self, btnPath)
    -----------------------------------------------------------
    【instance: ScreenNode】 UI类实例
    【path: str】 控件路径
    -----------------------------------------------------------
    return: Tuple[float, float] -> 坐标元组
    """
    pos = [0, 0]
    while path:
        parentPos = instance.GetBaseUIControl(path).GetPosition()
        pos[0] += parentPos[0]
        pos[1] += parentPos[1]
        path = get_parent_path(path)
    return tuple(pos)


def get_parent_path(path):
    # type: (str) -> str
    """
    获取父控件路径。
    示例：
    get_parent_path("/panel/parent/btnPath")
    # "/panel/parent"
    -----------------------------------------------------------
    【path: str】 控件路径
    -----------------------------------------------------------
    return: str -> 父控件路径
    """
    return "/".join(path.split("/")[:-1])




















