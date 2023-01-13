
# -*- coding: utf-8 -*-
from ...comp.baseComp import BaseComp
from ...bookConfig import BookConfig

class ButtonComp(BaseComp):

    def __init__(self):
        # type: () -> ButtonComp
        """
            按钮组件初始化
        """
        pass

    def SetDataBeforeShow(self, defaultImage=BookConfig.Images.blank, pressCallBack=None, moveInCallBack=None, text="", pressImage=None, hoverImage=None):
        # type: (str, dict, dict, str, str, str) -> ButtonComp
        """
            在显示组件之前，设置组件的数据
        """       
        pass

    def SetAlpha(self, alpha):
        # type: (float) -> ButtonComp
        """
            设置按钮中图片的透明度
        """       
        pass

    def SetTextColor(self, color):
        # type: (tuple[float, float, float, float]) -> ButtonComp
        """
            设置按钮中文字的颜色
        """       
        pass

    def SetTextSize(self, newSize):
        # type: (int) -> ButtonComp
        """
            设置按钮中文字的颜色
        """       
        pass

    def SetTextAlpha(self, alpha):
        # type: (float) -> ButtonComp
        """
            设置按钮中文字的透明度
        """       
        pass
