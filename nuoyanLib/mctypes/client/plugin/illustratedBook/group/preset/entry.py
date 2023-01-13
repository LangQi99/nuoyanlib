
# -*- coding: utf-8 -*-
from ...group.pageGroup import PageGroup


class Entry(PageGroup):

    def GetParent(self):
        # type: () -> float
        """
            获取父页组（其父页组是Category对象）
        """ 
        pass
        

    def isLocked(self):
        # type: () -> bool
        """
            返回该章节解锁状态
        """ 
        pass


    def Lock(self):
        # type: () -> None
        """
            将该章节上锁
        """ 
        pass

    def Unlock(self):
        # type: () -> None
        """
            将该章节解锁
        """
        pass
