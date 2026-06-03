import tkinter as tk
from tkinter import messagebox
import random

# 苏州版「今天吃什么决定器」
# 说明：
# 1. 不联网，不会自动读取地图；餐厅营业时间、分店位置请出发前再用地图确认。
# 2. 想加餐厅，只需要在 RESTAURANTS 里按同样格式新增一项。
# 3. 想删餐厅，直接删掉对应字典即可。

RESTAURANTS = [
    {
        "name": "松鹤楼",
        "eat": "松鼠鳜鱼 / 清炒虾仁 / 苏帮菜",
        "category": "苏帮菜",
        "area": "观前街/市中心",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["正式一点", "带朋友", "想吃苏州味"],
        "flavor": ["清淡", "甜口", "本地特色"],
        "note": "经典苏帮菜老字号，适合认真吃一顿。",
        "tags": ["老字号", "苏帮菜", "游客友好"]
    },
    {
        "name": "得月楼",
        "eat": "松鼠鳜鱼 / 响油鳝糊 / 苏式船点",
        "category": "苏帮菜",
        "area": "观前街/市中心",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["正式一点", "带朋友", "想吃苏州味"],
        "flavor": ["清淡", "甜口", "本地特色"],
        "note": "老牌苏帮菜，适合想吃传统菜的时候。",
        "tags": ["老字号", "苏帮菜", "观前街"]
    },
    {
        "name": "新聚丰菜馆",
        "eat": "母油船鸭 / 樱桃肉 / 手剥虾仁",
        "category": "苏帮菜",
        "area": "观前街/市中心",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["正式一点", "带朋友", "想吃苏州味"],
        "flavor": ["本地特色", "甜口"],
        "note": "老派苏帮菜，适合多人点几个菜一起吃。",
        "tags": ["苏帮菜", "老饭店"]
    },
    {
        "name": "协和菜馆",
        "eat": "响油鳝糊 / 酱鸭 / 清炒虾仁",
        "category": "苏帮菜",
        "area": "观前街/市中心",
        "budget": "¥¥",
        "time": ["午餐", "晚餐"],
        "scene": ["想吃苏州味", "家常一点"],
        "flavor": ["本地特色", "清淡"],
        "note": "比大馆子更家常，适合想吃苏式小炒。",
        "tags": ["苏帮菜", "家常"]
    },
    {
        "name": "吴门人家",
        "eat": "苏帮菜 / 苏式点心 / 评弹氛围",
        "category": "苏帮菜",
        "area": "平江路/姑苏区",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["带朋友", "想吃苏州味", "有氛围"],
        "flavor": ["本地特色", "清淡"],
        "note": "适合想要一点苏州氛围感的时候。",
        "tags": ["苏帮菜", "氛围"]
    },
    {
        "name": "珍珠饭店",
        "eat": "苏式家常菜 / 河鲜 / 小炒",
        "category": "苏帮菜",
        "area": "姑苏区",
        "budget": "¥¥",
        "time": ["午餐", "晚餐"],
        "scene": ["家常一点", "不想太贵", "带朋友"],
        "flavor": ["本地特色", "清淡"],
        "note": "适合几个人随便点菜吃饭。",
        "tags": ["家常菜", "苏帮菜"]
    },

    {
        "name": "同得兴",
        "eat": "枫镇大肉面 / 白汤面 / 焖肉面",
        "category": "苏式汤面",
        "area": "十全街/姑苏区",
        "budget": "¥¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "想吃苏州味", "不想太撑"],
        "flavor": ["清淡", "本地特色"],
        "note": "想吃苏式白汤面时很适合，早上吃更有感觉。",
        "tags": ["苏式面", "白汤", "枫镇大肉面"]
    },
    {
        "name": "裕兴记",
        "eat": "两面黄 / 三虾面 / 蟹黄面 / 浇头面",
        "category": "苏式汤面",
        "area": "平江路/苏博附近",
        "budget": "¥¥",
        "time": ["早餐", "午餐", "晚餐"],
        "scene": ["一个人", "带朋友", "想吃苏州味"],
        "flavor": ["本地特色", "鲜味"],
        "note": "想吃特色苏式面，尤其是两面黄，可以选它。",
        "tags": ["苏式面", "两面黄", "蟹黄面"]
    },
    {
        "name": "朱鸿兴",
        "eat": "焖肉面 / 爆鱼面 / 苏式浇头面",
        "category": "苏式汤面",
        "area": "观前街/市中心",
        "budget": "¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "不想太贵", "想吃苏州味"],
        "flavor": ["本地特色", "清淡"],
        "note": "老字号面馆，适合快速吃一碗面。",
        "tags": ["老字号", "苏式面", "浇头面"]
    },
    {
        "name": "陆长兴",
        "eat": "苏式汤面 / 焖肉面 / 爆鱼面",
        "category": "苏式汤面",
        "area": "姑苏区/多店",
        "budget": "¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "不想太贵", "家常一点"],
        "flavor": ["本地特色", "清淡"],
        "note": "传统苏式面馆，适合想吃得简单一点。",
        "tags": ["苏式面", "老字号"]
    },
    {
        "name": "伟记奥面馆",
        "eat": "奥灶面 / 爆鱼面 / 焖肉面",
        "category": "苏式汤面",
        "area": "姑苏区",
        "budget": "¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "想吃热乎的", "不想太贵"],
        "flavor": ["本地特色", "鲜味"],
        "note": "想换一碗昆山风格奥灶面，可以试试。",
        "tags": ["奥灶面", "苏式面"]
    },
    {
        "name": "苏祥兴",
        "eat": "苏式汤面 / 浇头面",
        "category": "苏式汤面",
        "area": "十全街/姑苏区",
        "budget": "¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "不想太贵", "想吃苏州味"],
        "flavor": ["本地特色", "清淡"],
        "note": "十全街一带的苏式面选择之一。",
        "tags": ["苏式面", "十全街"]
    },
    {
        "name": "万泰兴",
        "eat": "苏式汤面 / 焖肉面 / 大排面",
        "category": "苏式汤面",
        "area": "十全街/姑苏区",
        "budget": "¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "不想太贵", "家常一点"],
        "flavor": ["本地特色", "清淡"],
        "note": "适合想吃传统苏式汤面的时候。",
        "tags": ["苏式面", "十全街"]
    },

    {
        "name": "哑巴生煎",
        "eat": "生煎 / 泡泡小馄饨",
        "category": "小吃早餐",
        "area": "姑苏区/多店",
        "budget": "¥",
        "time": ["早餐", "午餐", "下午茶"],
        "scene": ["一个人", "不想太贵", "小吃"],
        "flavor": ["本地特色", "甜口", "鲜味"],
        "note": "想吃苏州生煎小吃时很合适。",
        "tags": ["生煎", "小馄饨"]
    },
    {
        "name": "鑫震源",
        "eat": "大虾生煎 / 鲜肉生煎 / 小馄饨",
        "category": "小吃早餐",
        "area": "山塘街/多店",
        "budget": "¥",
        "time": ["早餐", "午餐", "下午茶", "夜宵"],
        "scene": ["一个人", "不想太贵", "小吃"],
        "flavor": ["鲜味", "本地特色"],
        "note": "分店多，适合临时想吃生煎。",
        "tags": ["生煎", "连锁", "方便"]
    },
    {
        "name": "荣阳楼",
        "eat": "油氽团子 / 生煎 / 小馄饨",
        "category": "小吃早餐",
        "area": "山塘街",
        "budget": "¥",
        "time": ["早餐", "午餐", "下午茶"],
        "scene": ["小吃", "逛街顺便吃", "不想太贵"],
        "flavor": ["本地特色", "甜口"],
        "note": "山塘街附近想吃老式小吃可以考虑。",
        "tags": ["油氽团子", "生煎", "山塘街"]
    },
    {
        "name": "矮脚楼馄饨",
        "eat": "泡泡馄饨 / 小馄饨",
        "category": "小吃早餐",
        "area": "姑苏区",
        "budget": "¥",
        "time": ["早餐", "午餐", "夜宵"],
        "scene": ["一个人", "不想太撑", "小吃"],
        "flavor": ["清淡", "本地特色"],
        "note": "不太饿、想吃点热乎汤水时适合。",
        "tags": ["馄饨", "小吃"]
    },
    {
        "name": "马栋佩烧麦",
        "eat": "烧麦 / 蛋黄烧麦 / 香菇肉丁烧麦",
        "category": "小吃早餐",
        "area": "姑苏区",
        "budget": "¥",
        "time": ["早餐", "午餐"],
        "scene": ["一个人", "小吃", "不想太贵"],
        "flavor": ["本地特色", "咸香"],
        "note": "糯米党可以选，适合早餐或午餐。",
        "tags": ["烧麦", "早餐"]
    },
    {
        "name": "赵天禄",
        "eat": "熟食 / 酱肉 / 油汆团子",
        "category": "小吃早餐",
        "area": "观前街/市中心",
        "budget": "¥¥",
        "time": ["午餐", "下午茶", "晚餐"],
        "scene": ["小吃", "买点带走", "想吃苏州味"],
        "flavor": ["本地特色", "甜口"],
        "note": "适合买点苏式熟食或小吃。",
        "tags": ["老字号", "熟食", "小吃"]
    },

    {
        "name": "黄天源",
        "eat": "糕团 / 青团 / 糖年糕 / 定胜糕",
        "category": "甜点糕团",
        "area": "观前街/市中心",
        "budget": "¥",
        "time": ["早餐", "下午茶"],
        "scene": ["小吃", "买点带走", "想吃甜的"],
        "flavor": ["甜口", "本地特色"],
        "note": "苏式糕团老字号，适合想吃甜口点心。",
        "tags": ["糕团", "老字号", "甜点"]
    },
    {
        "name": "长发西饼",
        "eat": "鲜肉月饼 / 蛋糕 / 面包",
        "category": "甜点糕团",
        "area": "观前街/多店",
        "budget": "¥",
        "time": ["下午茶", "买点带走"],
        "scene": ["想吃甜的", "买点带走", "小吃"],
        "flavor": ["甜口", "咸香"],
        "note": "鲜肉月饼很适合趁热吃。",
        "tags": ["鲜肉月饼", "点心"]
    },
    {
        "name": "采芝斋",
        "eat": "苏式糖果 / 粽子糖 / 伴手礼",
        "category": "甜点糕团",
        "area": "观前街/市中心",
        "budget": "¥",
        "time": ["下午茶", "买点带走"],
        "scene": ["买点带走", "想吃甜的"],
        "flavor": ["甜口", "本地特色"],
        "note": "适合买苏式糖果和小零食。",
        "tags": ["老字号", "伴手礼", "糖果"]
    },
    {
        "name": "稻香村",
        "eat": "苏式糕点 / 鲜肉月饼 / 绿豆糕",
        "category": "甜点糕团",
        "area": "多店",
        "budget": "¥",
        "time": ["下午茶", "买点带走"],
        "scene": ["买点带走", "想吃甜的"],
        "flavor": ["甜口", "本地特色"],
        "note": "适合买传统点心或伴手礼。",
        "tags": ["糕点", "伴手礼"]
    },
    {
        "name": "叶受和",
        "eat": "苏式糕点 / 月饼 / 糖果",
        "category": "甜点糕团",
        "area": "观前街/市中心",
        "budget": "¥",
        "time": ["下午茶", "买点带走"],
        "scene": ["买点带走", "想吃甜的"],
        "flavor": ["甜口", "本地特色"],
        "note": "传统苏式糕点选择之一。",
        "tags": ["糕点", "老字号"]
    },
    {
        "name": "赵记传承",
        "eat": "绿豆汤 / 糖水 / 赤豆小圆子",
        "category": "甜点糕团",
        "area": "姑苏区/多店",
        "budget": "¥",
        "time": ["下午茶", "夜宵"],
        "scene": ["想吃甜的", "小吃", "不想太撑"],
        "flavor": ["甜口", "清爽"],
        "note": "想喝点甜汤、夏天解暑可以选。",
        "tags": ["甜品", "糖水"]
    },

    {
        "name": "双塔市集",
        "eat": "小吃 / 咖啡 / 简餐 / 甜品",
        "category": "市集扫街",
        "area": "双塔/姑苏区",
        "budget": "¥¥",
        "time": ["早餐", "午餐", "下午茶"],
        "scene": ["逛街顺便吃", "带朋友", "选择困难"],
        "flavor": ["丰富", "本地特色", "年轻一点"],
        "note": "选择多，适合不知道具体吃什么时边逛边决定。",
        "tags": ["市集", "咖啡", "小吃"]
    },
    {
        "name": "葑门横街",
        "eat": "菜场小吃 / 熟食 / 糕团 / 小面",
        "category": "市集扫街",
        "area": "葑门/姑苏区",
        "budget": "¥",
        "time": ["早餐", "午餐", "下午茶"],
        "scene": ["逛街顺便吃", "小吃", "不想太贵"],
        "flavor": ["本地特色", "烟火气"],
        "note": "烟火气更足，适合随便逛随便吃。",
        "tags": ["菜场", "小吃", "烟火气"]
    },
    {
        "name": "山塘街",
        "eat": "生煎 / 糕团 / 小吃 / 茶饮",
        "category": "市集扫街",
        "area": "山塘街",
        "budget": "¥¥",
        "time": ["午餐", "下午茶", "晚餐", "夜宵"],
        "scene": ["逛街顺便吃", "带朋友", "小吃"],
        "flavor": ["本地特色", "丰富"],
        "note": "适合边走边吃，但热门时段人会多。",
        "tags": ["景区", "小吃", "夜景"]
    },
    {
        "name": "平江路",
        "eat": "苏式小吃 / 咖啡 / 甜品 / 简餐",
        "category": "市集扫街",
        "area": "平江路/姑苏区",
        "budget": "¥¥",
        "time": ["午餐", "下午茶", "晚餐"],
        "scene": ["逛街顺便吃", "带朋友", "有氛围"],
        "flavor": ["丰富", "年轻一点"],
        "note": "适合约着散步，边逛边选。",
        "tags": ["景区", "咖啡", "小吃"]
    },
    {
        "name": "十全街",
        "eat": "苏式面 / 咖啡 / 小馆子",
        "category": "市集扫街",
        "area": "十全街/姑苏区",
        "budget": "¥¥",
        "time": ["早餐", "午餐", "下午茶", "晚餐"],
        "scene": ["逛街顺便吃", "选择困难", "想吃苏州味"],
        "flavor": ["丰富", "本地特色"],
        "note": "面馆和小店比较集中，适合随便逛。",
        "tags": ["苏式面", "街区"]
    },

    {
        "name": "海底捞",
        "eat": "火锅 / 番茄锅 / 牛肉 / 捞派滑牛",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "夜宵", "聚餐"],
        "scene": ["带朋友", "正式一点", "选择困难"],
        "flavor": ["辣", "丰富"],
        "note": "最稳的聚餐选择之一，分店多。",
        "tags": ["火锅", "聚餐", "连锁"]
    },
    {
        "name": "巴奴毛肚火锅",
        "eat": "毛肚 / 菌汤 / 火锅",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["带朋友", "想吃肉", "正式一点"],
        "flavor": ["辣", "鲜味"],
        "note": "想吃火锅但不想太随便时可以选。",
        "tags": ["火锅", "聚餐"]
    },
    {
        "name": "半天妖烤鱼",
        "eat": "青花椒烤鱼 / 蒜香烤鱼",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["带朋友", "不想太贵", "想吃重口"],
        "flavor": ["辣", "咸香"],
        "note": "两三个人吃比较合适。",
        "tags": ["烤鱼", "聚餐"]
    },
    {
        "name": "西塔老太太泥炉烤肉",
        "eat": "韩式烤肉 / 牛肉 / 拌饭",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["带朋友", "想吃肉"],
        "flavor": ["咸香", "丰富"],
        "note": "想吃烤肉时可以选。",
        "tags": ["烤肉", "聚餐"]
    },
    {
        "name": "太二酸菜鱼",
        "eat": "酸菜鱼 / 小吃 / 米饭",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥",
        "time": ["午餐", "晚餐"],
        "scene": ["带朋友", "不想太贵", "想吃重口"],
        "flavor": ["酸辣", "鲜味"],
        "note": "酸辣口，适合两三个人。",
        "tags": ["酸菜鱼", "聚餐"]
    },
    {
        "name": "南京大牌档",
        "eat": "盐水鸭 / 美龄粥 / 赤豆元宵",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥",
        "time": ["午餐", "晚餐"],
        "scene": ["带朋友", "家常一点", "选择困难"],
        "flavor": ["江浙口", "清淡"],
        "note": "不一定是苏州菜，但商场聚餐比较稳。",
        "tags": ["江浙菜", "商场"]
    },
    {
        "name": "桂满陇",
        "eat": "杭帮菜 / 东坡肉 / 西湖醋鱼",
        "category": "商场聚餐",
        "area": "多商圈",
        "budget": "¥¥¥",
        "time": ["午餐", "晚餐", "聚餐"],
        "scene": ["正式一点", "带朋友", "有氛围"],
        "flavor": ["江浙口", "甜口"],
        "note": "想吃江浙菜、环境好一点可以选。",
        "tags": ["杭帮菜", "商场"]
    },

    {
        "name": "兰州牛肉面",
        "eat": "牛肉面 / 炒面片 / 凉拌牛肉",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥",
        "time": ["早餐", "午餐", "晚餐", "夜宵"],
        "scene": ["一个人", "不想太贵", "快点吃完"],
        "flavor": ["咸香", "清淡"],
        "note": "简单、快、不会太纠结。",
        "tags": ["快餐", "面"]
    },
    {
        "name": "麻辣烫",
        "eat": "自选麻辣烫 / 冒菜",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥",
        "time": ["午餐", "晚餐", "夜宵"],
        "scene": ["一个人", "选择困难", "不想太贵"],
        "flavor": ["辣", "丰富"],
        "note": "想吃什么自己夹，适合纠结的时候。",
        "tags": ["快餐", "自选"]
    },
    {
        "name": "黄焖鸡米饭",
        "eat": "黄焖鸡 / 米饭 / 土豆香菇",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥",
        "time": ["午餐", "晚餐"],
        "scene": ["一个人", "快点吃完", "不想太贵"],
        "flavor": ["咸香"],
        "note": "非常标准的工作日选择。",
        "tags": ["快餐", "米饭"]
    },
    {
        "name": "沙县小吃",
        "eat": "拌面 / 蒸饺 / 鸭腿饭 / 馄饨",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥",
        "time": ["早餐", "午餐", "晚餐", "夜宵"],
        "scene": ["一个人", "快点吃完", "不想太贵"],
        "flavor": ["清淡", "咸香"],
        "note": "不讲究但很方便。",
        "tags": ["快餐", "简单"]
    },
    {
        "name": "东北水饺",
        "eat": "水饺 / 锅包肉 / 地三鲜",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥¥",
        "time": ["午餐", "晚餐"],
        "scene": ["一个人", "带朋友", "想吃热乎的"],
        "flavor": ["咸香", "家常"],
        "note": "想吃主食、热乎一点时适合。",
        "tags": ["饺子", "家常"]
    },
    {
        "name": "重庆小面",
        "eat": "小面 / 豌杂面 / 红油抄手",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥",
        "time": ["午餐", "晚餐", "夜宵"],
        "scene": ["一个人", "不想太贵", "想吃重口"],
        "flavor": ["辣", "咸香"],
        "note": "想吃辣但不想吃太多时适合。",
        "tags": ["面", "辣"]
    },
    {
        "name": "煲仔饭",
        "eat": "腊味煲仔饭 / 牛肉煲仔饭",
        "category": "随便吃点",
        "area": "附近就行",
        "budget": "¥¥",
        "time": ["午餐", "晚餐"],
        "scene": ["一个人", "想吃热乎的", "不想太贵"],
        "flavor": ["咸香"],
        "note": "适合想吃米饭又想有点锅气。",
        "tags": ["米饭", "热乎"]
    },

    {
        "name": "霸王茶姬",
        "eat": "伯牙绝弦 / 茉莉雪芽",
        "category": "喝点东西",
        "area": "多商圈",
        "budget": "¥",
        "time": ["下午茶", "晚餐", "夜宵"],
        "scene": ["想喝点", "逛街顺便吃", "买点带走"],
        "flavor": ["清爽", "奶茶"],
        "note": "想喝奶茶但不想太腻。",
        "tags": ["奶茶", "连锁"]
    },
    {
        "name": "喜茶",
        "eat": "多肉葡萄 / 芝芝莓莓 / 果茶",
        "category": "喝点东西",
        "area": "多商圈",
        "budget": "¥¥",
        "time": ["下午茶", "晚餐"],
        "scene": ["想喝点", "逛街顺便吃"],
        "flavor": ["清爽", "甜口"],
        "note": "想喝水果茶时可以选。",
        "tags": ["果茶", "奶茶"]
    },
    {
        "name": "瑞幸咖啡",
        "eat": "生椰拿铁 / 美式 / 拿铁",
        "category": "喝点东西",
        "area": "多商圈",
        "budget": "¥",
        "time": ["早餐", "下午茶"],
        "scene": ["想喝点", "快点吃完", "买点带走"],
        "flavor": ["咖啡", "清爽"],
        "note": "想提神、方便带走。",
        "tags": ["咖啡", "连锁"]
    },
    {
        "name": "Manner Coffee",
        "eat": "拿铁 / 澳白 / 美式",
        "category": "喝点东西",
        "area": "多商圈",
        "budget": "¥¥",
        "time": ["早餐", "下午茶"],
        "scene": ["想喝点", "买点带走"],
        "flavor": ["咖啡"],
        "note": "想喝咖啡时可以选。",
        "tags": ["咖啡"]
    },
    {
        "name": "7分甜",
        "eat": "杨枝甘露 / 芒果西米露",
        "category": "喝点东西",
        "area": "多商圈",
        "budget": "¥",
        "time": ["下午茶", "晚餐", "夜宵"],
        "scene": ["想喝点", "想吃甜的"],
        "flavor": ["甜口", "清爽"],
        "note": "想喝甜品饮料可以选。",
        "tags": ["甜品", "饮品"]
    },
]

BUDGET_OPTIONS = ["不限", "¥", "¥¥", "¥¥¥"]
CATEGORY_OPTIONS = ["不限"] + sorted(set(item["category"] for item in RESTAURANTS))
AREA_OPTIONS = ["不限"] + sorted(set(item["area"] for item in RESTAURANTS))
TIME_OPTIONS = ["不限", "早餐", "午餐", "下午茶", "晚餐", "夜宵", "聚餐"]
SCENE_OPTIONS = ["不限", "一个人", "带朋友", "正式一点", "不想太贵", "想吃苏州味", "小吃", "逛街顺便吃", "选择困难", "快点吃完", "想吃甜的", "想喝点", "想吃重口", "买点带走"]
FLAVOR_OPTIONS = ["不限", "清淡", "甜口", "辣", "鲜味", "咸香", "本地特色", "丰富", "咖啡", "奶茶", "清爽"]

COMMENTS = [
    "就这个，别纠结了。",
    "今天吃这个很合理。",
    "命运已经替你点好了。",
    "可以，出发。",
    "这个选择不亏。",
    "再想下去就饿过头了。",
    "要不今天就试试这个？",
    "这个结果有点靠谱。",
]


def match_item(item, category, area, budget, time_choice, scene, flavor, keyword):
    if category != "不限" and item["category"] != category:
        return False

    if area != "不限" and item["area"] != area:
        return False

    if budget != "不限" and item["budget"] != budget:
        return False

    if time_choice != "不限" and time_choice not in item["time"]:
        return False

    if scene != "不限" and scene not in item["scene"]:
        return False

    if flavor != "不限" and flavor not in item["flavor"]:
        return False

    keyword = keyword.strip().lower()
    if keyword:
        text = " ".join([
            item["name"], item["eat"], item["category"], item["area"], item["note"],
            " ".join(item["tags"]), " ".join(item["scene"]), " ".join(item["flavor"])
        ]).lower()
        if keyword not in text:
            return False

    return True


class SuzhouFoodPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("苏州今天吃什么")
        self.root.geometry("760x720")
        self.root.minsize(760, 720)
        self.root.configure(bg="#fff8f0")

        self.history = []
        self.current_result = None

        self.category_var = tk.StringVar(value="不限")
        self.area_var = tk.StringVar(value="不限")
        self.budget_var = tk.StringVar(value="不限")
        self.time_var = tk.StringVar(value="不限")
        self.scene_var = tk.StringVar(value="不限")
        self.flavor_var = tk.StringVar(value="不限")
        self.keyword_var = tk.StringVar(value="")

        self.build_ui()
        self.update_count()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="苏州今天吃什么？",
            font=("Microsoft YaHei", 26, "bold"),
            bg="#fff8f0",
            fg="#2f2f2f"
        )
        title.pack(pady=(18, 4))

        subtitle = tk.Label(
            self.root,
            text="筛一下，再摇一下。实在不想筛，就直接摇。",
            font=("Microsoft YaHei", 11),
            bg="#fff8f0",
            fg="#777"
        )
        subtitle.pack()

        filter_box = tk.LabelFrame(
            self.root,
            text="筛选条件",
            font=("Microsoft YaHei", 11, "bold"),
            bg="#fff8f0",
            fg="#555",
            padx=12,
            pady=10
        )
        filter_box.pack(fill="x", padx=22, pady=(16, 10))

        self.add_option(filter_box, "类型", self.category_var, CATEGORY_OPTIONS, 0, 0)
        self.add_option(filter_box, "区域", self.area_var, AREA_OPTIONS, 0, 2)
        self.add_option(filter_box, "预算", self.budget_var, BUDGET_OPTIONS, 0, 4)
        self.add_option(filter_box, "时间", self.time_var, TIME_OPTIONS, 1, 0)
        self.add_option(filter_box, "场景", self.scene_var, SCENE_OPTIONS, 1, 2)
        self.add_option(filter_box, "口味", self.flavor_var, FLAVOR_OPTIONS, 1, 4)

        tk.Label(filter_box, text="关键词", bg="#fff8f0", fg="#555", font=("Microsoft YaHei", 10)).grid(row=2, column=0, sticky="e", padx=4, pady=7)
        keyword_entry = tk.Entry(filter_box, textvariable=self.keyword_var, font=("Microsoft YaHei", 10), width=22)
        keyword_entry.grid(row=2, column=1, sticky="w", padx=4, pady=7)
        keyword_entry.bind("<KeyRelease>", lambda event: self.update_count())

        reset_btn = tk.Button(
            filter_box,
            text="清空筛选",
            font=("Microsoft YaHei", 10),
            relief="flat",
            bg="#ffe3c4",
            activebackground="#ffd29b",
            command=self.reset_filters
        )
        reset_btn.grid(row=2, column=2, padx=4, pady=7, sticky="w")

        self.count_label = tk.Label(
            filter_box,
            text="",
            bg="#fff8f0",
            fg="#999",
            font=("Microsoft YaHei", 10)
        )
        self.count_label.grid(row=2, column=3, columnspan=3, sticky="w", padx=4, pady=7)

        card = tk.Frame(self.root, bg="white", highlightbackground="#f0d7bf", highlightthickness=1)
        card.pack(fill="x", padx=22, pady=10)

        self.name_label = tk.Label(
            card,
            text="点「帮我决定」开始",
            font=("Microsoft YaHei", 25, "bold"),
            bg="white",
            fg="#222",
            wraplength=690,
            justify="center"
        )
        self.name_label.pack(pady=(24, 8))

        self.eat_label = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 15),
            bg="white",
            fg="#555",
            wraplength=690,
            justify="center"
        )
        self.eat_label.pack(pady=4)

        self.meta_label = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            bg="white",
            fg="#777",
            wraplength=690,
            justify="center"
        )
        self.meta_label.pack(pady=4)

        self.note_label = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            bg="white",
            fg="#888",
            wraplength=690,
            justify="center"
        )
        self.note_label.pack(pady=(4, 22))

        button_box = tk.Frame(self.root, bg="#fff8f0")
        button_box.pack(pady=(10, 8))

        self.pick_button = tk.Button(
            button_box,
            text="帮我决定",
            font=("Microsoft YaHei", 15, "bold"),
            width=14,
            height=2,
            relief="flat",
            bg="#ff9f68",
            fg="white",
            activebackground="#ff8a48",
            activeforeground="white",
            command=self.start_pick
        )
        self.pick_button.grid(row=0, column=0, padx=8)

        self.again_button = tk.Button(
            button_box,
            text="换一个",
            font=("Microsoft YaHei", 13),
            width=11,
            height=2,
            relief="flat",
            bg="#ffd6a8",
            activebackground="#ffc17a",
            command=self.start_pick
        )
        self.again_button.grid(row=0, column=1, padx=8)

        self.copy_button = tk.Button(
            button_box,
            text="复制结果",
            font=("Microsoft YaHei", 13),
            width=11,
            height=2,
            relief="flat",
            bg="#ffe3c4",
            activebackground="#ffd29b",
            command=self.copy_result
        )
        self.copy_button.grid(row=0, column=2, padx=8)

        lower_box = tk.Frame(self.root, bg="#fff8f0")
        lower_box.pack(fill="both", expand=True, padx=22, pady=(10, 16))

        alt_box = tk.LabelFrame(
            lower_box,
            text="备选项",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#fff8f0",
            fg="#555"
        )
        alt_box.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.alt_text = tk.Text(
            alt_box,
            height=8,
            font=("Microsoft YaHei", 10),
            bg="white",
            fg="#555",
            relief="flat",
            wrap="word"
        )
        self.alt_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.alt_text.insert("1.0", "摇一次之后，这里会显示几个备选。")
        self.alt_text.config(state="disabled")

        history_box = tk.LabelFrame(
            lower_box,
            text="最近摇到",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#fff8f0",
            fg="#555"
        )
        history_box.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.history_text = tk.Text(
            history_box,
            height=8,
            font=("Microsoft YaHei", 10),
            bg="white",
            fg="#555",
            relief="flat",
            wrap="word"
        )
        self.history_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.history_text.insert("1.0", "还没有记录。")
        self.history_text.config(state="disabled")

        tip = tk.Label(
            self.root,
            text="提示：本软件不联网；餐厅是否营业、排队情况、最近分店位置，请出发前再用地图确认。",
            font=("Microsoft YaHei", 9),
            bg="#fff8f0",
            fg="#aaa"
        )
        tip.pack(pady=(0, 10))

    def add_option(self, parent, label, variable, options, row, col):
        tk.Label(parent, text=label, bg="#fff8f0", fg="#555", font=("Microsoft YaHei", 10)).grid(row=row, column=col, sticky="e", padx=4, pady=7)
        menu = tk.OptionMenu(parent, variable, *options, command=lambda value: self.update_count())
        menu.config(font=("Microsoft YaHei", 10), width=12, relief="flat", bg="white", activebackground="#ffe3c4")
        menu.grid(row=row, column=col + 1, sticky="w", padx=4, pady=7)

    def reset_filters(self):
        self.category_var.set("不限")
        self.area_var.set("不限")
        self.budget_var.set("不限")
        self.time_var.set("不限")
        self.scene_var.set("不限")
        self.flavor_var.set("不限")
        self.keyword_var.set("")
        self.update_count()

    def get_filtered_items(self):
        return [
            item for item in RESTAURANTS
            if match_item(
                item,
                self.category_var.get(),
                self.area_var.get(),
                self.budget_var.get(),
                self.time_var.get(),
                self.scene_var.get(),
                self.flavor_var.get(),
                self.keyword_var.get()
            )
        ]

    def update_count(self):
        count = len(self.get_filtered_items())
        self.count_label.config(text=f"当前可选：{count} 个")

    def start_pick(self):
        items = self.get_filtered_items()
        if not items:
            messagebox.showinfo("没有结果", "当前筛选条件太严格了，放宽一点再试试。")
            return

        self.pick_button.config(state="disabled")
        self.again_button.config(state="disabled")
        self.copy_button.config(state="disabled")
        self.animate(0, items)

    def animate(self, count, items):
        item = random.choice(items)
        self.display_item(item, thinking=True)

        if count < 22:
            delay = 30 + count * 8
            self.root.after(delay, lambda: self.animate(count + 1, items))
        else:
            final = random.choice(items)
            self.current_result = final
            self.display_item(final, thinking=False)
            self.update_alternatives(items, final)
            self.update_history(final)
            self.pick_button.config(state="normal")
            self.again_button.config(state="normal")
            self.copy_button.config(state="normal")

    def display_item(self, item, thinking=False):
        self.name_label.config(text=item["name"])
        self.eat_label.config(text=item["eat"])
        self.meta_label.config(text=f'{item["category"]}｜{item["area"]}｜{item["budget"]}')

        if thinking:
            self.note_label.config(text="正在认真纠结中……")
        else:
            tag_text = " / ".join(item["tags"])
            self.note_label.config(text=f'{item["note"]}\n{random.choice(COMMENTS)}\n标签：{tag_text}')

    def update_alternatives(self, items, chosen):
        pool = [item for item in items if item is not chosen]
        random.shuffle(pool)
        alternatives = pool[:5]

        self.alt_text.config(state="normal")
        self.alt_text.delete("1.0", "end")

        if not alternatives:
            self.alt_text.insert("1.0", "当前筛选范围内没有更多备选。")
        else:
            lines = []
            for i, item in enumerate(alternatives, start=1):
                lines.append(f'{i}. {item["name"]}｜{item["eat"]}\n   {item["area"]}｜{item["budget"]}｜{item["note"]}')
            self.alt_text.insert("1.0", "\n\n".join(lines))

        self.alt_text.config(state="disabled")

    def update_history(self, item):
        text = f'{item["name"]}｜{item["eat"]}'
        if text not in self.history:
            self.history.insert(0, text)
        self.history = self.history[:8]

        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.insert("1.0", "\n".join(f"{i + 1}. {x}" for i, x in enumerate(self.history)))
        self.history_text.config(state="disabled")

    def copy_result(self):
        if not self.current_result:
            return

        item = self.current_result
        text = (
            f'今天吃：{item["name"]}\n'
            f'推荐：{item["eat"]}\n'
            f'区域：{item["area"]}\n'
            f'预算：{item["budget"]}\n'
            f'理由：{item["note"]}'
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("已复制", "结果已经复制，可以直接发给朋友。")


if __name__ == "__main__":
    root = tk.Tk()
    app = SuzhouFoodPicker(root)
    root.mainloop()
