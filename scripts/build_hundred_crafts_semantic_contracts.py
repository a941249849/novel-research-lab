#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "projects/hundred-crafts-night-procession"
BLUEPRINT = (
    ROOT
    / "system/research_assets/project_candidates/hundred-crafts-night-procession/series-blueprint.v0.3.json"
)
PROFILE = ROOT / "system/research_assets/deep_read/v0.29/signature_profiles.v1.json"
LIBRARY = ROOT / "system/research_assets/deep_read/v0.29/loss_resistant_mechanism_library.v1.json"
VOLUME1_OUTLINE = WORKSPACE / "production_runtime/plans/volume1_outline.v1.json"

CHARACTERS = {
    "char_zhou_li": ("周砺", "验损、承重边界与公共叫停"),
    "char_cheng_xueqing": ("程雪青", "测量、证据等级与标准失效"),
    "char_du_chengli": ("杜承礼", "角色授权、署名与知识使用边界"),
    "char_lin_dai": ("林岱", "风险隔舱、转运与下游清偿"),
    "char_ma_xiaoman": ("马小满", "过程复原、版本异议与补偿追索"),
}

PRIMARY = {
    1: ["char_zhou_li"],
    2: ["char_du_chengli"],
    3: ["char_lin_dai"],
    4: ["char_ma_xiaoman"],
    5: ["char_cheng_xueqing"],
    6: ["char_cheng_xueqing", "char_du_chengli"],
    7: ["char_zhou_li"],
    8: ["char_du_chengli", "char_ma_xiaoman"],
    9: ["char_cheng_xueqing", "char_ma_xiaoman"],
    10: ["char_lin_dai"],
    11: ["char_du_chengli", "char_cheng_xueqing"],
    12: ["char_lin_dai", "char_cheng_xueqing"],
    13: ["char_zhou_li"],
    14: ["char_ma_xiaoman"],
    15: list(CHARACTERS),
}

HIGHLIGHTS = {
    1: {
        "char_zhou_li": ("公开父亲完整责任账并撤回单方翻案", "在三套退构结构间找出共同承重点", "失去以无罪结案的私人目标", "主角第一次用公开自身损失换取居民否决权"),
    },
    2: {
        "char_du_chengli": ("亲手允许外行拒绝祖传角色", "从磨损、针脚和穿戴次序识别强制授权", "失去行内人独占解释权", "守艺者的高光来自放权而非垄断"),
    },
    3: {
        "char_lin_dai": ("开启自己当年封存且会牵连主港的风险舱", "在潮位窗口内完成分舱和逆向转运", "公开个人曾转嫁给下游的旧债", "最擅长封舱的人第一次负责开舱清偿"),
    },
    4: {
        "char_ma_xiaoman": ("保留互相冲突且对周家不利的档案版本", "从纸层、钟差和修补次序复原删改链", "无法用唯一真相替受害者完成和解", "记录者承认准确不是正义的终点"),
    },
    5: {
        "char_cheng_xueqing": ("宣布自己建立的统一尺度在九地失效", "给标准增加适用域、误差级和地方否决接口", "失去可用一个模型证明所有人的确定感", "科学能力通过声明边界而不是神化精确获得高光"),
    },
    6: {
        "char_cheng_xueqing": ("签署整批报废而不伪造成功率", "用试样和污染曲线证明开窑不可逆", "承担多个城市短期断供责任", "敢于证明失败比假成功更有公共价值"),
        "char_du_chengli": ("拆掉自己搭出的临时骨架", "判断彩扎受潮后的真实风载极限", "失去能证明传统技艺万能的作品", "守艺人主动终止不再安全的技艺方案"),
    },
    7: {
        "char_zhou_li": ("在父亲参与建造的旧城段上签署减材", "区分结构承重、历史价值和现实占用", "承认保存本身也会伤人", "修复者第一次以克制拆除完成救援"),
    },
    8: {
        "char_du_chengli": ("拒绝把社区纹样收进统一工谱", "识别纹样使用权与制作技法的分离", "失去扩大学艺谱系的机会", "专业权威通过承认无权占有而成立"),
        "char_ma_xiaoman": ("允许社区撤回已进入系统的版本", "建立可撤回而不抹除历史痕迹的版本链", "责任账不再拥有永久保存优先权", "记录系统首次服从当事人的退出权"),
    },
    9: {
        "char_cheng_xueqing": ("拒绝把统计有效写成个体安全", "分离批次、炮制、暴露和不良结果证据", "承认检测无法代替临床判断", "工程师在最需要答案时守住专业边界"),
        "char_ma_xiaoman": ("把失败病例和补偿责任写进同一公开账", "追出被拆分到多地的试用链", "承受急救能力下降的舆论追责", "弱者不再只是成功率分母"),
    },
    10: {
        "char_lin_dai": ("主张让仍能运转的百年系统按期退役", "把机械时序、工伤和生态恢复编成退出次序", "失去最熟悉的永久维护岗位", "维护者以结束维护完成职业成年"),
    },
    11: {
        "char_du_chengli": ("拒绝让九地角色权限被中央接口吞并", "把多种岗位授权压缩到最低互认层", "承担合拢效率下降", "地方知识不是被展示，而是获得可退出的制度位置"),
        "char_cheng_xueqing": ("接受九套互不完全换算的有效尺度", "建立跨区误差传播和失败回滚", "统一标准不再由她最终裁决", "标准制定者完成从中心到接口维护者的转变"),
    },
    12: {
        "char_lin_dai": ("封存来源不正当但能救急的材料", "逆查运输舱、生态损伤和劳动条件", "让富裕地区先承担短缺", "风险专家第一次拒绝把上游当成无名舱室"),
        "char_cheng_xueqing": ("撤销形式合规材料的准入", "证明证书完整与材料真实历史可以背离", "公开检测体系的系统盲点", "证据链从材料性能扩展到材料来处"),
    },
    13: {
        "char_zhou_li": ("在四十八小时危机中接受居民有成本的否决", "把验损结论拆成可选择的风险方案", "承担程序延迟造成的真实伤亡", "总验候选人拒绝成为替所有人决定的英雄"),
    },
    14: {
        "char_ma_xiaoman": ("拒绝按政治价值排列档案抢救顺序", "用物理损毁、现实补偿和当事人请求三轴排程", "无法保存全部历史凭证", "档案高光不是全知，而是公开不可避免的损失"),
    },
    15: {
        "char_zhou_li": ("拒绝终身总验席位", "证明任何单点权威都会重新制造暗载", "放弃完成父亲未完成事业的象征", "主角以拒绝垄断完成全书成长"),
        "char_cheng_xueqing": ("为公共标准写入定期失效", "建立可撤回、重验和版本并存协议", "接受标准会被后人推翻", "科学秩序获得自我否定能力"),
        "char_du_chengli": ("把角色授权交还各地共同维护", "完成署名、复制、退出的最低接口", "不再拥有完整传承谱", "传承因不被一人占有而存续"),
        "char_lin_dai": ("拆除最后一个永久风险舱", "把应急隔离改成有期限的公共能力", "失去以封存换稳定的终极后手", "他不再把未来当作下游"),
        "char_ma_xiaoman": ("允许《百工夜行录》保留互相冲突的终局版本", "建立公开异议和后人续记接口", "放弃替文明写下唯一结论", "书名在她手中成为可继续修订的公共记录"),
    },
}

DIMENSION_POLICIES = {
    "narrative_spine": (
        "十五卷必须由责任公开、权限变化和旧债清偿推动，不能只靠更大的事故升级。",
        "把升级型主线改写为公共维护权逐级扩大又逐级受限的因果链。",
    ),
    "character_highlight_architecture": (
        "五名核心角色必须凭不可替代的专业判断改变方案，并为高光承担永久代价。",
        "不迁移人物原型和关系组合，只保留独立目标、选择、代价、回收四步结构。",
    ),
    "progression_and_thresholds": (
        "成长只增加可验证能力、责任范围和叫停权限，每级都写明准入证据、禁区与追责。",
        "把战力境界转换为六能力四岗位责任谱，禁止无代价越级与临场新增权限。",
    ),
    "world_map_and_scale": (
        "地域扩张必须同时改变材料条件、证据规则、利益相关者和解决权限。",
        "不用换地图重复任务；以十五种地域旧账和公共工程尺度重建世界扩张。",
    ),
    "embedded_history_and_lore": (
        "每卷历史材料必须推翻一种当下误读并改变现实行动，不得作为百科插叙。",
        "用工案、账簿、刻痕、口述和异本承载历史，禁止人格化概念寓言与原作表达。",
    ),
    "faction_and_resource_game": (
        "阵营冲突围绕材料、署名、证据等级、维护预算和否决权展开，资源流向必须可追踪。",
        "不复制宗门或势力皮肤，把博弈转换为谁受益、谁承重、谁清偿的制度冲突。",
    ),
    "relationship_and_emotional_cost": (
        "关系变化必须来自专业选择与责任承担，和解不能抹去损失，背叛不能只服务反转。",
        "以信任、署名、父子责任和居民授权承载情感代价，不借用原作恋爱或复仇轨迹。",
    ),
    "foreshadowing_and_payoff": (
        "伏笔必须绑定物证、责任人、可见误读和计划回收卷，禁止只靠神秘名词吊胃口。",
        "把秘密线索改造成可复核的版本链和旧账因果，不复制专名、谜底或揭示顺序。",
    ),
    "climax_convergence": (
        "高潮必须让多种专业权限互相制约并共同签验，任何一人都不能包办答案。",
        "把战力合流改成证据、工序、否决和清偿的协同，不复制战斗编组与能力组合。",
    ),
    "reader_feedback_rhythm": (
        "每章提供可感知小闭环，每十章改变一次局面，每卷同时兑现旧账并打开新地域。",
        "不用升级打脸模板，以修复结果、关系反应、制度变化和新债形成持续反馈。",
    ),
    "style_and_life_force": (
        "宏大议题必须落在劳动动作、材料触感、生活选择和人物之间的不整齐反应上。",
        "禁止模仿任何作者句式和口癖，通过具体工作现场与地方生活形成项目自身声线。",
    ),
    "failure_modes_and_negative_lessons": (
        "主动阻断主角代签、历史百科化、权限膨胀、配角工具化和责任被英雄动机抵销。",
        "把语料中的失败教训写成可执行负约束，不迁移导致失败的情节外壳。",
    ),
}

DEFER_REASONS = {
    "narrative_spine": "当前卷级因果链已冻结，只能在新卷立项时比较后启用。",
    "character_highlight_architecture": "当前高光轮换已冻结，启用前须证明不会挤压既定角色主体性。",
    "progression_and_thresholds": "当前责任谱已锁定，新增阈值须先通过权限冲突审查。",
    "world_map_and_scale": "当前地域路线已冻结，新增扩张机制须先绑定具体地域证据。",
    "embedded_history_and_lore": "当前工案已绑定卷次，新增历史结构须先证明不会越卷泄漏。",
    "faction_and_resource_game": "对应阵营资产尚未进入本卷运行时，须在资产完成后重审。",
    "relationship_and_emotional_cost": "须先标明改变哪段信任、由谁选择以及造成何种永久损失。",
    "foreshadowing_and_payoff": "须先声明埋设物证、当下误读、回收位置和现实后果。",
    "climax_convergence": "须先证明每个岗位在高潮中仍保有独立否决权。",
    "reader_feedback_rhythm": "卷一章级闭环已冻结，须先通过节奏密度与重复性审查。",
    "style_and_life_force": "任何语料风格机制都须单独完成去模仿审查。",
    "failure_modes_and_negative_lessons": "只在命中具体项目风险时才可转成运行时硬规则。",
}

HISTORY = [
    ("梁底换名册", "梁底墨书与三次覆灰", "官造纪工匠共同救下戏楼", "临时承重者姓名被改成材料编号", "新裂缝与墨书位置重合", "众人以为是父亲伪造责任人", "三代修缮都沿用删名规则", "团队必须先公开承重者再决定修复"),
    ("卸装簿", "盔箱夹层中的穿戴与归还簿", "名角终身守护一城安定", "替补演员从未被允许卸装", "市民出现无法退出的公共角色", "团队把旧簿当成荣耀谱", "归还栏才是被故意裁去的制度核心", "解决方案转为恢复拒绝、归还和署名"),
    ("封舱潮记", "船板刻痕、货单和船员口述", "主港凭封舱术躲过百年风灾", "危险货物被逐代推往无名下游", "多港旧舱同时逼近开启阈值", "林岱以为照旧加固即可", "旧刻痕记录的是开启期限而非封存功绩", "必须公开转运与最终清偿人"),
    ("纸上无名案", "虫蛀案卷、补纸水印与口述副本", "档案修复保存了灾后秩序", "修复时删除了无法证明身份的受害者", "责任账出现只有痕迹没有姓名的人", "马小满试图寻找唯一原本", "不存在中立原本，删改本身就是事件", "异议版本进入正式责任链"),
    ("九尺争衡", "九种旧尺、换算碑和交易纠纷判词", "统一尺度结束长期争斗", "最弱地区承担全部换算误差", "跨区抢修按统一值连续失败", "程雪青认为地方经验不够精确", "旧判词明确统一尺只限特定材料和季节", "标准增加适用域和地方否决"),
    ("不开窑约", "窑门封泥、试片和报废账", "祖师开窑挽救三城", "失败批次与燃料伤害被从谱系中删除", "污染燃料迫使三窑共同决策", "团队把不开窑理解为怯懦禁忌", "原约要求证据不足时宁可公开失败", "团队选择报废并承担断供"),
    ("减城碑阴", "会馆碑阴、拆料编号和迁居契", "保城工程留下完整古城", "被拆社区只以空白编号存在", "危险历史层与现居空间冲突", "周砺以为保存越多越负责", "碑阴记录每次保存都对应一次迁移", "减材决定必须同时生成补偿清单"),
    ("无主纹册", "染样边角、织工歌次序和市场印样", "一位大师创造了救灾纹样", "纹样实际由多地女性劳动与路线共同生成", "标准系统无法识别分布式记忆", "杜承礼试图寻找原作者授权", "原作不是单人作品，也不存在永久总代表", "建立用途限定与社区撤回协议"),
    ("两面药簿", "批次药簿、炮制火候记和不良结果口述", "某方药在大灾中救活万人", "失败病例被拆散到产地之外", "退构缓解材料出现批次差异", "团队把古法视为稳定配方", "旧簿记录的是条件与风险，不是万能药方", "效用、毒性、知情和补偿同账"),
    ("停伐钟班表", "机械钟盘、工伤班表和家属补记", "林场机器从未停摆地支撑城市", "退休工与家属被当作永久备件", "旧时序继续驱动公共设施", "林岱认为维护即可避免阵痛", "班表末页原定退役日被反复涂去", "系统退役必须与转岗、旧伤和生态同步"),
    ("九地合手图", "九张不同比例工程图与译注", "中央总图让九地第一次协作", "地方否决和失败记录被译成噪声", "复合闸坝无法按一图合拢", "众人寻找一张正确总图", "九图只共享接口，从未承诺相同解释", "采用最低互认而非中央技能树"),
    ("万物来处册", "材料戳记、矿林账和运输舱单", "合规供应链保证公共工程质量", "生态损伤和无名劳动被隔离到上游", "证书完整的材料连续失效", "程雪青先怀疑检测造假", "证书只记录交付后性能，不记录来处代价", "不正当来源成为工程否决条件"),
    ("急修四十八条", "灾时令、居民涂改和拆除追记", "总验独断在大灾中救下全城", "被占土地和未来拆除者没有签名", "临时疏散城必须快速扩建", "周砺把旧令当成紧急授权模板", "居民涂改才记录了工程得以执行的真实条件", "紧急权力加入时限、复核和补偿"),
    ("天下旧账目录", "残损目录、财政拨付与个人证言", "国家档案保存了官造纪全部责任", "抢救顺序长期服从权势和可见度", "档案设施开始物理退构", "马小满想先保存最完整卷宗", "不完整证言可能是弱者唯一补偿凭证", "抢救顺序改由现实权利风险共同决定"),
    ("夜行录异本", "五人工作记录、地方异本和公开批注", "存在一部能解释百工枢的权威原典", "权威原典是后人为了垄断维护权拼成的假象", "四种文明方案争夺最终解释权", "众人以为找到原典即可结束争论", "《百工夜行录》从来是可增删、可反驳的公共记录", "终局制度写入失效、退出和后人续记"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    blueprint = json.loads(BLUEPRINT.read_text(encoding="utf-8"))
    volumes = blueprint["volumes"]
    highlight_volumes = []
    for volume in volumes:
        number = volume["volume"]
        agency = {
            character_id: {
                "domain": domain,
                "independent_action": (
                    f"{name}必须针对“{volume['irreversible_change']}”以{domain}作出独立判断；"
                    "该判断可以否决主方案，不能由周砺或组织代签。"
                ),
                "on_page_obligation": (
                    f"至少一次让{name}用可见证据提出方案、异议或叫停，"
                    f"并改变《{volume['working_title']}》的执行顺序。"
                ),
                "failure_consequence": (
                    f"若其判断被忽略，后果必须落到“{volume['new_debt']}”，"
                    "不得只用争吵代替代价。"
                ),
            }
            for character_id, (name, domain) in CHARACTERS.items()
        }
        signature = [
            {
                "character_id": character_id,
                "irreversible_choice": values[0],
                "competence_display": values[1],
                "cost": values[2],
                "reader_payoff": values[3],
            }
            for character_id, values in HIGHLIGHTS[number].items()
        ]
        highlight_volumes.append(
            {
                "volume": number,
                "working_title": volume["working_title"],
                "primary_spotlight": PRIMARY[number],
                "agency": agency,
                "signature_highlights": signature,
            }
        )
    write(
        WORKSPACE / "design/character_highlight_matrix.v1.json",
        {
            "version": "1.0",
            "project_id": "hundred-crafts-night-procession",
            "characters": [
                {
                    "character_id": character_id,
                    "name": name,
                    "irreducible_domain": domain,
                    "signature_highlight_volumes": [
                        number for number, entries in HIGHLIGHTS.items() if character_id in entries
                    ],
                }
                for character_id, (name, domain) in CHARACTERS.items()
            ],
            "volumes": highlight_volumes,
        },
    )
    ranks = [
        ("见习", "在监督下完成单项识材与记录", ["标记异常", "请求复核"], ["不得改变公共结构", "不得代签授权"], "错误由本人和监督者共同复盘"),
        ("成手", "独立完成可逆工序并通过事故复盘", ["执行可逆干预", "拒绝超出工种范围的任务"], ["不得主持跨工种方案", "不得隐瞒失败"], "承担本人操作、记录和及时停工责任"),
        ("主作", "主持一次多岗位工程且完整清偿后续责任", ["组织工序", "签署本工种方案", "触发局部叫停"], ["不得替受影响者授权", "不得取消异议"], "承担本工种方案的期限、交接和失效声明"),
        ("总验", "证明能公开自身方案的失败条件并接受外部否决", ["主持验损", "召集多方签验", "叫停重大工程"], ["不得决定谁承重", "不得成为终身职位", "不得越过地域知识权"], "承担信息完整、程序有效和权力按期退出责任"),
    ]
    previous = "v1.baseline"
    atlas_volumes = []
    for volume in volumes:
        atlas_volumes.append(
            {
                "volume": volume["volume"],
                "working_title": volume["working_title"],
                "scope": volume["scope"],
                "entry_conditions": [previous, *([volume["new_debt"]] if volume["volume"] > 1 else [])],
                "new_rule": volume["institutional_gain"],
                "irreversible_cost": volume["new_debt"],
                "evidence_routes": volume["evidence_routes"],
                "blocking_research": volume["blocking_research"],
            }
        )
        previous = volume["irreversible_change"]
    write(
        WORKSPACE / "design/world_progression_atlas.v1.json",
        {
            "version": "1.0",
            "project_id": "hundred-crafts-night-procession",
            "progression_rule": "成长提高责任范围、复核能力和叫停权限，不提供无代价战力碾压。",
            "competencies": [
                {"competency_id": key, "name": name, "mastery_proof": proof}
                for key, name, proof in [
                    ("material_reading", "识材", "能区分材料现状、来源与不可见代价"),
                    ("damage_verification", "验损", "能提出可证伪的失效判断"),
                    ("sequence_design", "成序", "能说明工序顺序及回滚点"),
                    ("multi_role_coordination", "合手", "能让不同岗位保有独立否决"),
                    ("burden_distribution", "分载", "能公开受益者、承重者和清偿人"),
                    ("accountable_record", "留档", "能保存版本、异议、期限和退出条件"),
                ]
            ],
            "authority_ranks": [
                {
                    "rank": rank,
                    "entry_proof": proof,
                    "permissions": permissions,
                    "prohibitions": prohibitions,
                    "liability": liability,
                }
                for rank, proof, permissions, prohibitions, liability in ranks
            ],
            "volumes": atlas_volumes,
        },
    )
    write(
        WORKSPACE / "design/embedded_history_engine.v1.json",
        {
            "version": "1.0",
            "project_id": "hundred-crafts-night-procession",
            "engine_name": "百工旧账",
            "narrative_rule": "历史材料必须改变当卷判断、权限或解法；不能作为脱离行动的设定插叙。",
            "form_rule": "使用工案、账簿、刻痕、口述、异本和维修记录，不使用人格化概念寓言。",
            "dossiers": [
                {
                    "volume": index,
                    "dossier_name": item[0],
                    "carrier": item[1],
                    "public_account": item[2],
                    "suppressed_burden": item[3],
                    "present_trigger": item[4],
                    "initial_misreading": item[5],
                    "reveal": item[6],
                    "plot_consequence": item[7],
                    "originality_guard": "只迁移历史副线参与现实决策的抽象功能；不复制《人祖传》的概念角色、蛊虫人格化、寓言句式、事件或价值命题。",
                }
                for index, item in enumerate(HISTORY, 1)
            ],
        },
    )
    volume1_outline = json.loads(VOLUME1_OUTLINE.read_text(encoding="utf-8"))
    history_stages = {
        3: "梁底墨书首次作为物证进入现场，但只展示局部字迹。",
        8: "第二份记录证明公开版本存在断点，旧账不再只是背景。",
        12: "梁底墨书中被反复覆灰的退名痕迹显形，促使团队重新检查名册记录的是责任退出而非材料归类。",
        18: "父亲拆除代偿装置，使周家版本从无罪叙述转为行为核查。",
        19: "公开叙述第一次被推翻：知情代价不能由英雄动机抵销。",
        29: "梁底换名册的删名规则显形，未识别承重者进入补偿范围。",
        41: "三代修缮沿用删名规则的证据闭合，历史直接改变当前修复权限。",
        54: "公开承重者与责任继承人，旧账开始决定现实签验顺序。",
        60: "多版本异议并列入账，拒绝用单一真相替代责任清偿。",
        66: "卷一保留可续记接口，并把旧账方法带入下一地域。",
    }
    progression_stages = (
        (1, 10, "见习阈值：识别异常、请求复核，禁止个人代签或单独承重。"),
        (11, 20, "成手前置：完成可逆隔舱与证据记录，同时显露风险转嫁代价。"),
        (21, 30, "成手验证：提出可回滚方案，让受影响者取得否决与异议权。"),
        (31, 40, "主作前置：经历材料失败、组织成立和多专业方案冲突。"),
        (41, 50, "主作验证：在暴雨压力下主持多岗位工序并公开失效条件。"),
        (51, 60, "总验前置：协调公开签验，但不得替居民决定承重与补偿。"),
        (61, 66, "卷末验收：证明权力可退出、节点可拆、账目可被后人反驳。"),
    )
    semantic_beats = []
    last_history = "旧账尚未显形；本章只允许用可验证痕迹预埋，不作说明性插叙。"
    for chapter in volume1_outline["chapters"]:
        number = int(chapter["chapter"])
        if number in history_stages:
            last_history = history_stages[number]
        progression = next(
            text for start, end, text in progression_stages if start <= number <= end
        )
        semantic_beats.append(
            {
                "chapter_id": f"chapter-{number:04d}",
                "pov": chapter["pov"],
                "character_pressure": (
                    f"{chapter['pov']}必须凭自身专业判断作出选择；"
                    "不得只负责向周砺解释、递交线索或赞同主角。"
                ),
                "progression_function": progression,
                "history_function": last_history,
                "reader_payoff": (
                    f"本章通过“{chapter['purpose']}”兑现一个可感知的小闭环，"
                    f"并以“{chapter['irreversible_change']}”留下不可逆后果。"
                ),
                "originality_guard": (
                    "只执行功能层约束；禁止迁移训练集专名、人物关系、事件链、"
                    "能力体系、寓言结构或可识别文风。"
                ),
            }
        )
    write(
        WORKSPACE / "production_runtime/plans/volume1_semantic_beat_contract.v1.json",
        {
            "version": "1.0",
            "project_id": "hundred-crafts-night-procession",
            "volume": 1,
            "chapter_count": 66,
            "history_dossier": "梁底换名册",
            "chapters": semantic_beats,
        },
    )
    paths = {
        "highlight": "projects/hundred-crafts-night-procession/design/character_highlight_matrix.v1.json",
        "atlas": "projects/hundred-crafts-night-procession/design/world_progression_atlas.v1.json",
        "history": "projects/hundred-crafts-night-procession/design/embedded_history_engine.v1.json",
        "beats": "projects/hundred-crafts-night-procession/production_runtime/plans/volume1_semantic_beat_contract.v1.json",
    }
    dimension_target = {
        "narrative_spine": [paths["atlas"]],
        "character_highlight_architecture": [paths["highlight"]],
        "progression_and_thresholds": [paths["atlas"]],
        "world_map_and_scale": [paths["atlas"]],
        "embedded_history_and_lore": [paths["history"]],
        "faction_and_resource_game": [paths["atlas"]],
        "relationship_and_emotional_cost": [paths["highlight"]],
        "foreshadowing_and_payoff": [paths["history"], paths["highlight"]],
        "climax_convergence": [paths["highlight"], paths["atlas"]],
        "reader_feedback_rhythm": [paths["highlight"], paths["history"]],
        "style_and_life_force": [paths["history"]],
        "failure_modes_and_negative_lessons": [paths["atlas"], paths["history"]],
    }
    selected_signature_decisions = [
        {
            "source_book": book,
            "source_dimension": dimension,
            "decision": decision,
            "rationale": rationale,
            "canonical_artifacts": [paths[target]],
            "originality_transformation": transformation,
        }
        for book, dimension, decision, rationale, target, transformation in [
            ("一念永恒", "reader_feedback_rhythm", "transform", "保留高压长线中的节奏释压与群体反馈。", "highlight", "把喜剧性转为班组磨合、职业窘境和代价后的生活回弹，不复制角色口癖与桥段。"),
            ("不死不灭", "climax_convergence", "defer", "保留跨时代因果汇聚的价值，但卷一证据不足以启动终局规模。", "history", "只预留责任代际传递，不复制轮回、灭世冲突或角色谱系。"),
            ("人道至尊", "faction_and_resource_game", "transform", "保留个体成长与族群生存互相牵制。", "atlas", "改为地域维护权、材料来处和公共资源分配，不复制种族体系与功法。"),
            ("仙逆", "relationship_and_emotional_cost", "transform", "保留成长每次越界都会永久改变关系与自我认知。", "highlight", "以专业信任、父子责任和居民授权承载代价，不复制复仇、轮回与人物声线。"),
            ("凡人修仙传", "progression_and_thresholds", "transform", "保留资源稀缺、谨慎验证和阶段门槛的可追踪性。", "atlas", "改为材料、权限、证据和责任门槛，不复制修炼、法宝与机缘结构。"),
            ("圣墟", "world_map_and_scale", "defer", "保留旧历史重释现实地图的扩张方式，待地域研究完成后启用。", "history", "使用工案和生态来处扩展尺度，不复制复苏、星空或血脉设定。"),
            ("大主宰", "climax_convergence", "transform", "保留多方专长在高潮中合流且各自不可替代。", "highlight", "用专业否决与共同签验形成合流，不复制学院、榜单和战斗编组。"),
            ("完美世界", "world_map_and_scale", "transform", "保留遗留制度与新地域层层揭示更大历史成本。", "history", "改为跨地域百工旧账，不复制纪元、血脉和宏大战场。"),
            ("将夜", "style_and_life_force", "transform", "保留宏大议题落回饮食、劳动、同伴和具体选择。", "highlight", "通过工作现场与居民生活建立温度，不模仿句式、幽默与人物关系。"),
            ("斗破苍穹", "reader_feedback_rhythm", "transform", "保留清晰阶段目标、兑现与升级反馈。", "atlas", "以权限和公共后果兑现成长，并拒绝羞辱翻盘、退婚模板与能力皮肤。"),
            ("武动乾坤", "character_highlight_architecture", "transform", "保留同伴在共同升级中拥有独立任务和回报。", "highlight", "五人依靠不同专业权力互相制约，不复制伙伴组合、血脉或战斗路径。"),
            ("永生", "faction_and_resource_game", "reject", "无限权力吞并一切资源的方向与公共责任主题冲突。", "atlas", "拒绝力量等于正当性的结构，只保留制度会争夺资源解释权这一反面警示。"),
            ("求魔", "relationship_and_emotional_cost", "transform", "保留身份认知被历史材料反复改写的情感压力。", "history", "通过档案版本、署名和责任继承重构，不复制身份谜底、宿命与叙事声线。"),
            ("牧神记", "embedded_history_and_lore", "transform", "保留文明遗迹不是装饰而是会推翻当下常识。", "history", "用技艺记录、维修痕迹和地方异本改变方案，不复制神话人物、遗迹体系与世界真相。"),
            ("诡秘之主", "foreshadowing_and_payoff", "transform", "保留组织、物件和信息层级构成可回查的长期伏笔网。", "history", "用责任账、版本链和地域证据回收，不复制序列、教会、仪式或克系语汇。"),
            ("遮天", "world_map_and_scale", "transform", "保留移动到新地域时规则、旧人和历史遗产共同升级。", "atlas", "十五卷按工程尺度和地域证据扩张，不复制星域、体质、秘境与角色回归桥段。"),
            ("雪中悍刀行", "character_highlight_architecture", "transform", "保留群像人物拥有独立立场、告别与高光回收。", "highlight", "高光来自专业选择和所付代价，不复制人物原型、江湖关系与散文化声线。"),
            ("蛊真人", "character_highlight_architecture", "transform", "保留长期角色拥有独立目标、阵营迁移和不可替代高光的功能。", "highlight", "改为五种专业权限互相制约的公共维护群像，不复制人物、立场或利益关系。"),
            ("蛊真人", "progression_and_thresholds", "transform", "保留阈值、资源、权限和失败条件从开篇可见且后期一致演化的功能。", "atlas", "改为六能力四岗位责任谱，不复制蛊虫、转数、道痕、仙窍或境界名称。"),
            ("蛊真人", "world_map_and_scale", "transform", "保留地图扩张同时改变规则、势力和资源结构的功能。", "atlas", "改为十五卷真实地域证据路线和公共工程尺度，不复制五域两天或尊者势力。"),
            ("蛊真人", "embedded_history_and_lore", "transform", "保留历史副线持续映照并推动现实主线的结构价值。", "history", "使用多版本工案和责任记录；明确禁止人格化概念寓言及《人祖传》表达结构。"),
            ("蛊真人", "style_and_life_force", "reject", "冷酷功利主角声线与本项目的公共群像身份冲突。", "highlight", "拒绝模仿冷静算计声线，只保留行动存在成本和对手会学习的结构原则。"),
        ]
    ]
    selected_signature_decisions = [
        item for item in selected_signature_decisions if item["decision"] != "defer"
    ]
    selected_by_cell = {
        (item["source_book"], item["source_dimension"]): item
        for item in selected_signature_decisions
    }
    signature_profiles = json.loads(PROFILE.read_text(encoding="utf-8"))["profiles"]
    signature_dimension_dispositions = []
    for profile in signature_profiles:
        for dimension, source in profile["dimensions"].items():
            selected = selected_by_cell.get((profile["book_title"], dimension))
            signature_dimension_dispositions.append(
                {
                    "source_profile_id": profile["profile_id"],
                    "source_book": profile["book_title"],
                    "source_dimension": dimension,
                    "source_status": source["status"],
                    "source_finding_digest": sha256_text(
                        json.dumps(source["findings"], ensure_ascii=False, sort_keys=True)
                    ),
                    "decision": selected["decision"] if selected else "defer",
                    "review_status": (
                        "project_rejected"
                        if selected and selected["decision"] == "reject"
                        else "project_activated"
                        if selected
                        else "protected_deferred"
                    ),
                    "rationale": (
                        selected["rationale"]
                        if selected
                        else (
                            f"{profile['book_title']}在{dimension}维度的受保护结论为"
                            f"{json.dumps(source['findings'][0], ensure_ascii=False, sort_keys=True)[:180]}。"
                            f"{DEFER_REASONS[dimension]}"
                        )
                    ),
                    "canonical_artifacts": (
                        selected["canonical_artifacts"]
                        if selected
                        else dimension_target[dimension]
                    ),
                    "originality_transformation": (
                        selected["originality_transformation"]
                        if selected
                        else (
                            f"该{dimension}结论仅保留为反丢失证据；启用前必须写出"
                            "《百工夜行录》的独立因果、角色代价与地域载体，"
                            "禁止迁移专名、事件链、能力皮肤和文风。"
                        )
                    ),
                    "activation_requirements": [
                        "identify one exact project volume and chapter range",
                        "write a project-specific causal transformation",
                        "prove no conflict with active character, progression, history, and originality contracts",
                        "relock canonical baseline and repeat dual independent review",
                    ],
                }
            )
    write(
        WORKSPACE / "validation/literary_semantic_application.v1.json",
        {
            "version": "1.0",
            "project_id": "hundred-crafts-night-procession",
            "source_signature_profiles_path": str(PROFILE.relative_to(ROOT)),
            "source_signature_profiles_sha256": sha256(PROFILE),
            "source_mechanism_library_path": str(LIBRARY.relative_to(ROOT)),
            "source_mechanism_library_sha256": sha256(LIBRARY),
            "dimension_decisions": [
                {
                    "dimension": dimension,
                    "decision": "transform",
                    "rationale": DIMENSION_POLICIES[dimension][0],
                    "canonical_artifacts": artifacts,
                    "originality_transformation": DIMENSION_POLICIES[dimension][1],
                }
                for dimension, artifacts in dimension_target.items()
            ],
            "signature_decisions": selected_signature_decisions,
            "signature_dimension_dispositions": signature_dimension_dispositions,
            "production_effect": {
                "old_baseline_authorization_valid": False,
                "formal_prose_must_pause": True,
                "required_before_reopen": [
                    "semantic contract validation",
                    "canonical baseline relock",
                    "Codex Sol independent review",
                    "Antigravity independent review",
                    "fresh Owner authorization",
                ],
            },
        },
    )


if __name__ == "__main__":
    build()
