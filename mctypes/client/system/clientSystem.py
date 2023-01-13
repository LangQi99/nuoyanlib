# -*- coding: utf-8 -*-

from ...common.system.baseSystem import BaseSystem

class ClientSystem(BaseSystem):
    def NotifyToServer(self, eventName, eventData):
        # type: (str, dict) -> None
        """
        客户端发送事件到服务器
        """
        pass

    def CreateEngineSfx(self, path, pos=None, rot=None, scale=None):
        # type: (str, tuple[float,float,float], tuple[float,float,float], tuple[float,float,float]) -> int|None
        """
        创建序列帧特效
        """
        pass

    def CreateEngineSfxFromEditor(self, path, pos=None, rot=None, scale=None):
        # type: (str, tuple[float,float,float], tuple[float,float,float], tuple[float,float,float]) -> int|None
        """
        指使用资源包中effects/xxx.json，按照编辑器中编辑好的参数创建序列帧。支持环状序列帧
        """
        pass

    def CreateEngineParticle(self, path, pos):
        # type: (str, tuple[float,float,float]) -> int|None
        """
        用于创建粒子特效
        """
        pass

    def CreateEngineEffectBind(self, path, bindEntity, aniName):
        # type: (str, str, str) -> int|None
        """
        指用编辑器保存资源包中models/bind/xxx_bind.json生成编辑好的所有挂点的所有特效。生成的特效会自动进行挂接及播放，编辑器中设为不可见的特效也会进行播放。并且使用这种方式创建的特效，开发者不用维护entity进出视野导致的挂接特效被移除，引擎会在entity每次进入视野时自动创建所有特效。
        """
        pass

    def DestroyEntity(self, entityId):
        # type: (int) -> bool
        """
        销毁特效
        """
        pass

