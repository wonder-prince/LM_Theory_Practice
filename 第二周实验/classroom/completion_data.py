"""微型句子补全实验的数据、词表和编码函数。

数据单独放在本文件中，便于课堂查看“模型究竟见过什么”。任务是五分类：输入
四个用空格分开的中文词，从【学习、下雨、健康、阅读、回家】中预测第五个词。
"""

from __future__ import annotations

import torch


CANDIDATES = ["学习", "下雨", "健康", "阅读", "回家"]

# 每个类别 10 条，共 5×10=50 条。把目标词接在四词提示后，可以组成通顺短句。
# 目标词本身不出现在输入中，避免模型只做复制。
TRAINING_SAMPLES = {
    "学习": [
        "学生 每天 认真 地", "我们 一起 努力 地", "他 在 图书馆 安静",
        "她 通过 视频 自主", "大家 利用 周末 集中", "为了 考试 我们 认真",
        "小组 成员 互相 帮助", "我 想 跟着 老师", "新生 开始 适应 线上",
        "他们 使用 电脑 辅助",
    ],
    "下雨": [
        "天空 乌云 密布 快要", "预报 说明 下午 可能", "外面 雷声 阵阵 正在",
        "天色 突然 变暗 开始", "空气 十分 潮湿 即将", "我 看见 乌云 认为会",
        "燕子 低飞 往往 预示", "风 越刮 越大 要", "窗外 云层 很厚 可能",
        "天气预报 提醒 今晚 会",
    ],
    "健康": [
        "均衡 饮食 有助 保持", "规律 运动 能够 促进", "充足 睡眠 有益 身体",
        "少油 少盐 让人 更加", "每天 散步 可以 保持", "良好 心态 有助 身心",
        "定期 体检 保障 身体", "戒烟 限酒 都 有利于", "科学 作息 让人 更",
        "适度 锻炼 使人 保持",
    ],
    "阅读": [
        "我 每天 睡前 坚持", "学生 在 图书馆 安静", "老师 鼓励 大家 广泛",
        "她 喜欢 利用 周末", "孩子 跟随 父母 一起", "为了 开阔 视野 多多",
        "这间 书房 适合 专心", "他 拿起 书本 开始", "课堂 留出 十分钟 自由",
        "我们 通过 电子设备 进行",
    ],
    "回家": [
        "加班 结束 以后 我", "放学 以后 学生 立即", "天色 已经 很晚 该",
        "任务 完成 以后 大家", "下班 后 我 直接", "聚会 结束 朋友们 各自",
        "比赛 结束 队员 准备", "课程 结束 我们 一起", "外面 下雨 他 提前",
        "妈妈 打来 电话 催我",
    ],
}

# 固定示例便于核对。它们属于训练集，因此只验证模型学会封闭任务。
EVALUATION_PROMPTS = [
    ("学生 每天 认真 地", "学习"),
    ("天空 乌云 密布 快要", "下雨"),
    ("均衡 饮食 有助 保持", "健康"),
    ("我 每天 睡前 坚持", "阅读"),
    ("加班 结束 以后 我", "回家"),
]


def build_vocabulary() -> tuple[dict[str, int], list[str]]:
    """把全部训练词按字典序编号，并加入 [UNK] 接收课堂中的未登录词。"""
    words = {"[UNK]"}
    for prompts in TRAINING_SAMPLES.values():
        for prompt in prompts:
            words.update(prompt.split())
    id_to_word = sorted(words)
    return {word: index for index, word in enumerate(id_to_word)}, id_to_word


def encode(prompt: str, word_to_id: dict[str, int]) -> list[int]:
    """把四词提示转换成四个整数 id；新词统一映射为 [UNK]。"""
    words = prompt.strip().split()
    if len(words) != 4:
        raise ValueError("请输入恰好 4 个用空格分隔的词，例如：天空 乌云 密布 将要")
    unknown_id = word_to_id["[UNK]"]
    return [word_to_id.get(word, unknown_id) for word in words]


def make_training_tensors(word_to_id: dict[str, int]) -> tuple[torch.Tensor, torch.Tensor]:
    """生成输入 [50,4] 与类别标签 [50]。"""
    rows, labels = [], []
    for label, candidate in enumerate(CANDIDATES):
        for prompt in TRAINING_SAMPLES[candidate]:
            rows.append(encode(prompt, word_to_id))
            labels.append(label)
    return torch.tensor(rows, dtype=torch.long), torch.tensor(labels, dtype=torch.long)

