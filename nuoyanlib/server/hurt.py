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
#   Last Modified : 2025-01-25
#
# ====================================================


from copy import copy as _copy
import mod.server.extraServerApi as _server_api
from mod.common.minecraftEnum import (
    EntityType as _EntityType,
    AttrType as _AttrType,
    ActorDamageCause as _ActorDamageCause,
)
from .._core._server._comp import (
    CompFactory as _CompFactory,
    LvComp as _LvComp,
)
from ..utils.calculator import (
    is_in_sector as _is_in_sector,
    pos_distance_to_line as _pos_distance_to_line,
)
from ..utils.vector import vec_angle as _vec_angle
from .entity import (
    entity_filter as _entity_filter,
    get_entities_in_area as _get_entities_in_area,
    get_all_entities as _get_all_entities,
)


__all__ = [
    "EntityFilter",
    "explode_hurt",
    "aoe_damage",
    "sector_aoe_damage",
    "rectangle_aoe_damage",
    "hurt_by_set_health",
    "hurt",
    "percent_damage",
    "line_damage",
]


_sdk_damage_cause = [v for k, v in _ActorDamageCause.__dict__.items() if not k.startswith("_")]


class EntityFilter:
    """
    实体过滤器，预设了一些常用的过滤条件。
    过滤器接受一个实体ID作为参数，且返回一个bool值，返回True时表示该实体符合条件。
    """

    @staticmethod
    def mob(eid):
        """
        | 过滤生物实体。

        -----

        :param str eid: 实体ID

        :return: 返回True时表示该实体为生物实体
        :rtype: bool
        """
        return _CompFactory.CreateEngineType(eid).GetEngineType() & _EntityType.Mob == _EntityType.Mob


    @staticmethod
    def non_mob(eid):
        """
        | 过滤非生物实体。

        -----

        :param str eid: 实体ID

        :return: 返回True时表示该实体为非生物实体
        :rtype: bool
        """
        return not EntityFilter.mob(eid)

    @staticmethod
    def has_health(eid):
        """
        | 过滤当前生命值>0的实体。

        -----

        :param str eid: 实体ID

        :return: 返回True时表示该实体当前生命值>0
        :rtype: bool
        """
        return _CompFactory.CreateAttr(eid).GetAttrValue(_AttrType.HEALTH) > 0


def explode_hurt(
        radius,
        pos,
        source_id,
        dim,
        fire=False,
        breaks=True,
        tile_drops=True,
        mob_loot=True,
        hurt_source=False,
):
    """
    | 造成爆炸伤害。
    
    -----

    :param float radius: 爆炸强度
    :param tuple[float,float,float] pos: 爆炸中心坐标
    :param str source_id: 爆炸伤害源的实体ID
    :param int dim: 爆炸维度
    :param bool fire: 是否造成火焰，默认为否
    :param bool breaks: 是否破坏方块，默认为是
    :param bool tile_drops: 破坏方块后是否生成掉落物，默认为是
    :param bool mob_loot: 生物被炸死后是否生成掉落物，默认为是
    :param bool hurt_source: 是否对爆炸伤害源实体造成伤害，默认为否

    :return: 无
    :rtype: None
    """
    for plr in _server_api.GetPlayerList():
        if _CompFactory.CreateDimension(plr).GetEntityDimensionId() == dim:
            player_id = plr
            break
    else:
        return
    orig_rule = _LvComp.Game.GetGameRulesInfoServer()
    _LvComp.Game.SetGameRulesInfoServer({'option_info': {'tile_drops': tile_drops, 'mob_loot': mob_loot}})
    comp = _CompFactory.CreateHurt(source_id)
    try:
        if not hurt_source:
            comp.ImmuneDamage(True)
        _LvComp.Explosion.CreateExplosion(pos, radius, fire, breaks, source_id, player_id)
    finally:
        _LvComp.Game.SetGameRulesInfoServer(orig_rule)
        if not hurt_source:
            comp.ImmuneDamage(False)


def line_damage(
        radius,
        start_pos,
        end_pos,
        dim,
        damage,
        cause=_ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        filter_ids=None,
        filter_types=None,
        filter_type_str=None,
        before_hurt_callback=None,
        after_hurt_callback=None,
        force=False,
):
    """
    | 对一条线段上的生物造成伤害。
    
    -----

    :param float radius: 伤害半径（生物到直线上的最大距离）
    :param tuple[float,float,float] start_pos: 线段起点坐标
    :param tuple[float,float,float] end_pos: 线段终点坐标
    :param int dim: 维度
    :param int damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，比如玩家使用抛射物造成伤害，该值应为抛射物实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为是
    :param list[str]|None filter_ids: 过滤的实体ID列表，列表中的实体将不会受到伤害，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filter_type_str: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param function|None before_hurt_callback: 对生物造成伤害之前调用的函数，该函数第一个参数为受伤生物的实体ID，第二个为攻击者的实体ID，第三个参数为攻击者的子实体ID；该函数可返回一个新的实体ID，新的实体ID将会替换原受伤生物的实体ID进入最终返回的受伤生物实体ID列表中，默认为None
    :param function|None after_hurt_callback: 对生物造成伤害之后调用的函数，该函数第一个参数为受伤生物的实体ID，第二个为攻击者的实体ID，第三个参数为攻击者的子实体ID；默认为None
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否

    :return: 受伤生物的实体ID列表
    :rtype: list[str]
    """
    if not start_pos or not end_pos or radius <= 0 or damage <= 0:
        return []
    if filter_ids is None:
        filter_ids = []
    else:
        filter_ids = filter_ids[:]
    if attacker_id:
        filter_ids.append(attacker_id)
    entities = _get_all_entities()
    entities = _entity_filter(
        entities, {_EntityType.Mob}, {str(dim)}, filter_ids, filter_types, filter_type_str
    )
    hurt_ents = []
    for eid in entities:
        ep = _CompFactory.CreatePos(eid).GetFootPos()
        dis = _pos_distance_to_line(ep, start_pos, end_pos)
        if dis > radius:
            continue
        v1 = tuple(a - b for a, b in zip(start_pos, ep))
        v2 = tuple(a - b for a, b in zip(end_pos, ep))
        if _vec_angle(v1, v2) < 1.57:
            continue
        if before_hurt_callback:
            ret_eid = before_hurt_callback(eid, attacker_id, child_id)
            if ret_eid:
                eid = ret_eid
        hurt(eid, damage, cause, attacker_id, child_id, knocked, force)
        if after_hurt_callback:
            after_hurt_callback(eid, attacker_id, child_id)
        hurt_ents.append(eid)
    return hurt_ents


def hurt_mobs(
        entity_id_list,
        damage,
        cause=_ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        force=False,
):
    """
    | 对多个生物造成伤害。（无视攻击冷却）
    
    -----

    :param list[str] entity_id_list: 实体ID列表
    :param int damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，比如玩家使用抛射物造成伤害，该值应为抛射物实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为是
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否

    :return: 无
    :rtype: None
    """
    for entity_id in entity_id_list:
        hurt(entity_id, damage, cause, attacker_id, child_id, knocked, force)


def aoe_damage(
        radius,
        pos,
        dim,
        damage,
        cause=_ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        filter_ids=None,
        filter_types=None,
        before_hurt_callback=None,
        after_hurt_callback=None,
        force=False,
):
    """
    | 在指定坐标造成范围伤害。
    
    -----

    :param float radius: 伤害半径
    :param tuple[float,float,float] pos: 产生范围伤害的中心点坐标
    :param int dim: 维度
    :param int damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，比如玩家使用抛射物造成伤害，该值应为抛射物实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为是
    :param list[str]|None filter_ids: 过滤的实体ID列表，列表中的实体将不会受到伤害，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param function|None before_hurt_callback: 对生物造成伤害之前调用的函数，该函数第一个参数为受伤生物的实体ID，第二个为攻击者的实体ID，第三个参数为攻击者的子实体ID；该函数可返回一个新的实体ID，新的实体ID将会替换原受伤生物的实体ID进入最终返回的受伤生物实体ID列表中；默认为None
    :param function|None after_hurt_callback: 对生物造成伤害之后调用的函数，该函数第一个参数为受伤生物的实体ID，第二个为攻击者的实体ID，第三个参数为攻击者的子实体ID；默认为None
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否

    :return: 受伤生物的实体ID列表
    :rtype: list[str]
    """
    if not pos or radius <= 0 or damage <= 0:
        return []
    if filter_ids is None:
        filter_ids = []
    else:
        filter_ids = filter_ids[:]
    if attacker_id:
        filter_ids.append(attacker_id)
    start_pos = tuple(i - radius for i in pos)
    end_pos = tuple(i + radius for i in pos)
    entities = _LvComp.Game.GetEntitiesInSquareArea(None, start_pos, end_pos, dim)
    entities = _entity_filter(entities, (pos, radius), {_EntityType.Mob}, filter_ids, filter_types)
    hurt_ents = []
    for eid in entities:
        if before_hurt_callback:
            ret_eid = before_hurt_callback(eid, attacker_id, child_id)
            if ret_eid:
                eid = ret_eid
        hurt(eid, damage, cause, attacker_id, child_id, knocked, force)
        if after_hurt_callback:
            after_hurt_callback(eid, attacker_id, child_id)
        hurt_ents.append(eid)
    return hurt_ents


def sector_aoe_damage(
        sector_radius,
        sector_angle,
        damage,
        cause=_ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        filter_ids=None,
        filter_types=None,
        force=False,
):
    """
    | 朝攻击者视线前方造成扇形范围伤害。（无视攻击冷却）
    
    -----

    :param float sector_radius: 扇形半径
    :param float sector_angle: 扇形张开的角度
    :param int damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者ID，默认无攻击者
    :param str|None child_id: 伤害来源的子实体ID，默认无子实体
    :param bool knocked: 是否击退，默认为是
    :param list[str]|None filter_ids: 过滤的实体ID列表，列表中的实体将不会受到伤害，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否

    :return: 受到伤害的实体ID列表
    :rtype: list[str]
    """
    if filter_ids is None:
        filter_ids = []
    filter_ids = _copy(filter_ids)
    filter_ids.append(attacker_id)
    attacker_pos = _CompFactory.CreatePos(attacker_id).GetFootPos()
    attacker_rot = _CompFactory.CreateRot(attacker_id).GetRot()[1]
    dim = _CompFactory.CreateDimension(attacker_id).GetEntityDimensionId()
    entity_list = _get_entities_in_area(attacker_pos, sector_radius, dim, filter_ids, filter_types, True)
    result = []
    for eid in entity_list:
        pos = _CompFactory.CreatePos(eid).GetFootPos()
        test = _is_in_sector(
            (pos[0], attacker_pos[1], pos[2]), attacker_pos, sector_radius, sector_angle, attacker_rot
        )
        if test:
            hurt(eid, damage, cause, attacker_id, child_id, knocked, force)
            result.append(eid)
    return result


def rectangle_aoe_damage(
        min_vertex,
        max_vertex,
        dim,
        damage,
        cause=_ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        hurt_attacker=False,
        hurt_child=False,
        ent_filter=None,
        force=False,
):
    """
    | 对指定矩形区域内所有实体造成伤害。
    
    -----

    :param tuple[float,float,float] min_vertex: 矩形最小顶点坐标
    :param tuple[float,float,float] max_vertex: 矩形最大顶点坐标，最大顶点坐标必须大于最小顶点坐标，否则不会对任何实体造成伤害
    :param int dim: 维度
    :param int damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者ID，默认None
    :param str|None child_id: 伤害来源的子实体ID，默认None
    :param bool knocked: 是否击退，默认为True
    :param bool hurt_attacker: 是否对攻击者造成伤害，默认为False
    :param bool hurt_child: 是否对子实体造成伤害，默认为False
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为False

    :return: 受到伤害的实体ID列表
    :rtype: list[str]
    """
    result = []
    entities_list = _LvComp.Game.GetEntitiesInSquareArea(None, min_vertex, max_vertex, dim)
    for eid in entities_list:
        if not hurt_attacker and eid == attacker_id:
            continue
        if not hurt_child and eid == child_id:
            continue
        if ent_filter and not ent_filter(eid):
            continue
        hurt(eid, damage, cause, attacker_id, child_id, knocked, force)
        result.append(eid)
    return result


def hurt_by_set_health(entity_id, damage):
    """
    | 通过设置生命值的方式对实体造成伤害。
    
    -----

    :param str entity_id: 实体ID
    :param int damage: 伤害

    :return: 无
    :rtype: None
    """
    attr = _CompFactory.CreateAttr(entity_id)
    health = attr.GetAttrValue(_AttrType.HEALTH)
    new_health = int(health) - int(damage)
    attr.SetAttrValue(_AttrType.HEALTH, new_health)


def hurt(
        entity_id,
        damage,
        cause=_ActorDamageCause.EntityAttack,
        attacker=None,
        child_id=None,
        knocked=True,
        force=False,
):
    """
    | 对指定生物造成伤害。
    
    -----

    :param str entity_id: 生物ID
    :param int damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 伤害来源的子实体ID，默认无子实体
    :param bool knocked: 是否造成击退，默认为是
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否
    
    :return: 无
    :rtype: None
    """
    if cause in _sdk_damage_cause:
        custom_tag = None
    else:
        custom_tag = cause
        cause = _ActorDamageCause.Custom
    hurt_result = _CompFactory.CreateHurt(entity_id).Hurt(int(damage), cause, attacker, child_id, knocked, custom_tag)
    if not hurt_result and force:
        hurt_by_set_health(entity_id, damage)


def percent_damage(
        entity_id,
        percent,
        type_name,
        cause=_ActorDamageCause.EntityAttack,
        attacker=None,
        child_id=None,
        knocked=True,
        force=False,
):
    """
    | 对生物造成百分比伤害。
    
    -----

    :param str entity_id: 生物ID
    :param float percent: 百分比
    :param str type_name: 伤害基准（可选值为"max_health"、"health"、"hunger"、"attacker_damage"）
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 伤害来源的子实体ID，默认无子实体
    :param bool knocked: 是否造成击退，默认为是
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否
    
    :return: 无
    :rtype: None
    """
    attr = _CompFactory.CreateAttr(entity_id)
    value = 0
    if type_name == "max_health":
        value = attr.GetAttrMaxValue(_AttrType.HEALTH)
    elif type_name == "health":
        value = attr.GetAttrValue(_AttrType.HEALTH)
    elif type_name == "hunger":
        value = attr.GetAttrValue(_AttrType.HUNGER)
    elif type_name == "attacker_damage" and attacker:
        value = _CompFactory.CreateAttr(attacker).GetAttrValue(_AttrType.DAMAGE)
    if value > 0:
        damage = int(value * percent)
        if damage > 999999999:
            damage = 999999999
        elif damage < 0:
            damage = 0
        hurt(entity_id, damage, cause, attacker, child_id, knocked, force)





















