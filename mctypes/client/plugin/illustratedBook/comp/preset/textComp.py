
# -*- coding: utf-8 -*-
from ...comp.baseComp import BaseComp
from ...bookConfig import BookConfig

class TextComp(BaseComp):

    def __init__(self, textAlign = BookConfig.TextAlign.Left):
        # type: (int) -> TextComp
        """
            文本组件初始化
        """
        pass

    def SetDataBeforeShow(self, text, textSize):
        # type: (str, int) -> TextComp
        """
            在显示组件之前，设置组件的数据
        """       
        pass 

    def SetAlpha(self, alpha):
        # type: (float) -> TextComp
        """
            设置文本字体透明度
        """       
        pass        

    def SetColor(self, color):
        # type: (tuple[float, float, float, float]) -> TextComp
        """
            设置文本字体颜色
        """       
        pass        


