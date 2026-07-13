import email.utils
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "trends.json"

FEEDS = [
    ("Google Trends US", "https://trends.google.com/trending/rss?geo=US"),
    ("NYTimes Technology", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"),
    ("Guardian Technology", "https://www.theguardian.com/technology/rss"),
    ("Guardian Football", "https://www.theguardian.com/football/rss"),
    ("Guardian Sport", "https://www.theguardian.com/sport/rss"),
]

TRANSLATION_CACHE = {}

PLATFORM_CONFIG = {
    "x": {
        "name": "X / Twitter",
        "count": 5,
        "topic": "实时讨论、新闻发酵、观点交锋",
        "accounts": [
            {"name": "@FabrizioRomano", "why": "快讯式标题和高频更新"},
            {"name": "@benedictevans", "why": "科技趋势大图景"},
            {"name": "@MarketingBrew", "why": "营销新闻角度"},
        ],
        "audience": "新闻敏感用户、行业从业者、体育/科技评论者、喜欢参与即时讨论的人群。",
        "motivation": "他们想第一时间知道发生了什么，并通过转发、评论、站队表达自己的判断。",
        "operation": "用事实来源 + 一句话判断 + 开放式问题发布。适合 thread、快评、数据截图和创始人视角。"
    },
    "instagram": {
        "name": "Instagram",
        "count": 4,
        "topic": "视觉化热点、Reels、轮播、生活方式",
        "accounts": [
            {"name": "@oldloserinbrooklyn", "why": "潮流趋势解释"},
            {"name": "@devonleecarlson", "why": "生活方式和怀旧视觉"},
            {"name": "@thetennisletter", "why": "体育热点图文快发"},
        ],
        "audience": "视觉审美用户、生活方式关注者、体育/娱乐粉丝、喜欢保存清单和轮播的人群。",
        "motivation": "他们需要好看、可保存、可转发的内容，也喜欢把热点变成个人风格表达。",
        "operation": "把热点拆成 5 页轮播或 15 秒 Reels：背景、原因、影响、可模仿动作、互动问题。"
    },
    "tiktok": {
        "name": "TikTok",
        "count": 5,
        "topic": "短视频挑战、趋势音频、反应视频、创作者经济",
        "accounts": [
            {"name": "@zachking", "why": "高完成度视觉反转"},
            {"name": "@colinandsamir", "why": "创作者经济拆解"},
            {"name": "@marketingexamined", "why": "营销案例短内容"},
        ],
        "audience": "年轻用户、短视频创作者、meme 参与者、喜欢快速模仿和二创的人群。",
        "motivation": "他们追求参与感、反差、情绪释放和容易复制的模板。",
        "operation": "用 3 秒 hook + 可复制模板 + 评论区任务。优先测试多个开头，再保留完播率最高版本。"
    },
    "facebook": {
        "name": "Facebook",
        "count": 4,
        "topic": "社区讨论、家庭消费、本地化、长帖解释",
        "accounts": [
            {"name": "Mari Smith", "why": "Facebook 营销教学"},
            {"name": "Jon Loomer", "why": "Meta 广告实操拆解"},
            {"name": "Scary Mommy", "why": "父母社群讨论语气"},
        ],
        "audience": "家长、本地社区用户、中小企业主、社群管理员和实用信息消费者。",
        "motivation": "他们更关心热点对家庭、社区、工作和日常消费有什么实际影响。",
        "operation": "把热点改写成社区问题、经验征集或实用清单。适合长帖、群组讨论和 Reels 二次分发。"
    },
}

ACCOUNT_POOLS = {
    "football": [
        {"name": "@FabrizioRomano", "why": "足球快讯标题和转会/赛事节奏"},
        {"name": "@MenInBlazers", "why": "足球文化梗和球迷口吻"},
        {"name": "@TrollFootball", "why": "体育 meme 反应速度"},
        {"name": "@thefootballarena", "why": "足球数据和观点图文"},
        {"name": "@brfootball", "why": "足球二创视觉和短梗"},
        {"name": "@TheEuropeanLad", "why": "球迷视角和争议讨论"},
    ],
    "ai_tech": [
        {"name": "@swyx", "why": "AI 开发者视角"},
        {"name": "@benedictevans", "why": "科技趋势大图景"},
        {"name": "@alliekmiller", "why": "AI 应用和商业化表达"},
        {"name": "@rowancheung", "why": "AI 新闻快讯和工具拆解"},
        {"name": "@mckaywrigley", "why": "AI 产品演示与观点"},
        {"name": "@stratechery", "why": "科技商业模式拆解"},
    ],
    "marketing_creator": [
        {"name": "@MarketingBrew", "why": "营销新闻角度"},
        {"name": "@marketingexamined", "why": "营销案例短内容"},
        {"name": "@KatelynBourgoin", "why": "消费者心理拆解"},
        {"name": "@gregisenberg", "why": "创业和内容商业化观点"},
        {"name": "@colinandsamir", "why": "创作者经济分析"},
        {"name": "@mattnavarra", "why": "社媒平台更新快讯"},
    ],
    "fashion_lifestyle": [
        {"name": "@oldloserinbrooklyn", "why": "潮流趋势解释"},
        {"name": "@devonleecarlson", "why": "个人风格和怀旧视觉"},
        {"name": "@matildadjerf", "why": "复古生活方式审美"},
        {"name": "@wisdm8", "why": "青年文化和趋势拆解"},
        {"name": "@best.dressed", "why": "穿搭叙事和视觉表达"},
        {"name": "@theannaedit", "why": "生活方式清单化表达"},
    ],
    "food_travel": [
        {"name": "@keith_lee125", "why": "真实试吃和评分结构"},
        {"name": "@jordan_the_stallion8", "why": "食品和文化梗讲述"},
        {"name": "@eatlikeagirl", "why": "食物故事和旅行语境"},
        {"name": "@londonfoodbabes", "why": "本地美食热点"},
        {"name": "@eitan", "why": "美食短视频节奏"},
        {"name": "@food52", "why": "食物生活方式包装"},
    ],
    "parenting_safety": [
        {"name": "Common Sense Media", "why": "家庭科技教育内容"},
        {"name": "Dr. Becky at Good Inside", "why": "家长心理和教育表达"},
        {"name": "Scary Mommy", "why": "父母社群讨论语气"},
        {"name": "The Holderness Family", "why": "家庭场景和幽默表达"},
        {"name": "Laura Clery", "why": "生活化喜剧表达"},
        {"name": "Raising Good Humans", "why": "亲子议题播客式拆解"},
    ],
    "facebook_marketing": [
        {"name": "Mari Smith", "why": "Facebook 营销教学"},
        {"name": "Jon Loomer", "why": "Meta 广告实操拆解"},
        {"name": "Neil Patel", "why": "中小企业营销教育"},
        {"name": "Social Media Examiner", "why": "平台更新解释"},
        {"name": "HubSpot", "why": "B2B 内容营销模板"},
        {"name": "Amy Porterfield", "why": "课程和社群转化内容"},
    ],
    "video_reaction": [
        {"name": "@zachking", "why": "高完成度视觉反转"},
        {"name": "@ryantrahan", "why": "系列化叙事和挑战"},
        {"name": "@airrack", "why": "大型挑战和快节奏剪辑"},
        {"name": "@ishowspeed", "why": "强情绪反应内容"},
        {"name": "@alanchikinchow", "why": "短剧和系列化叙事"},
        {"name": "@khaby.lame", "why": "极简反应式表达"},
    ],
    "news_analysis": [
        {"name": "@MorningBrew", "why": "新闻摘要包装"},
        {"name": "@axios", "why": "短句新闻解释结构"},
        {"name": "@semafor", "why": "国际新闻背景化表达"},
        {"name": "@mattnavarra", "why": "社媒新闻快讯"},
        {"name": "@TaylorLorenz", "why": "互联网文化报道视角"},
        {"name": "@CaseyNewton", "why": "平台政策和科技新闻分析"},
    ],
}

USED_ACCOUNT_COMBOS = {key: set() for key in PLATFORM_CONFIG}

# Override the broad creator pools above with micro-creator candidates.
# These are intentionally not official accounts or mega creators. Follower
# counts change, so the UI labels them as estimates and recommends a final
# check before outreach or paid collaboration.
ACCOUNT_POOLS = {
    "football": [
        {"name": "@Alwys_ChsngFPL", "followers": "<10万，FPL 小号", "why": "Fantasy football 数据和差异化选题"},
        {"name": "@elliottvenis", "followers": "约5万", "why": "足球/体育预测类内容节奏"},
        {"name": "@goalflexo", "followers": "约2万", "why": "足球短视频和球星热点二创"},
        {"name": "@marfawe", "followers": "约2万", "why": "世界杯图文梗和球迷口吻"},
        {"name": "@igoeLFC", "followers": "<10万需复核", "why": "垂直球迷号标题和情绪表达"},
        {"name": "@TacticsJournal", "followers": "<10万需复核", "why": "战术拆解和长图文表达"},
    ],
    "ai_tech": [
        {"name": "@ImKushanK", "followers": "约5万", "why": "AI 自动化教学和工具演示"},
        {"name": "@Bennettxai", "followers": "<10万需复核", "why": "AI 自动化实操内容"},
        {"name": "@marcinteodoru", "followers": "约4.1万", "why": "AI 视觉内容和教程表达"},
        {"name": "@Ivy_Dinma", "followers": "约1.2万-5万", "why": "AI 营销和业务运营内容"},
        {"name": "@lifeof_scoop", "followers": "<10万需复核", "why": "本地 newsletter 和 AI 小生意拆解"},
        {"name": "@exploraX_", "followers": "<10万需复核", "why": "AI 自动化和增长观点"},
    ],
    "marketing_creator": [
        {"name": "@ChelseaUGC", "followers": "约4万", "why": "UGC 创作者变现和家居内容"},
        {"name": "@patrickcolpron", "followers": "约4万", "why": "餐厅/本地营销和创作者增长"},
        {"name": "@SocialJesi", "followers": "<10万需复核", "why": "社媒营销技巧和轻量教学"},
        {"name": "@lifeof_scoop", "followers": "<10万需复核", "why": "newsletter 增长案例"},
        {"name": "@Ivy_Dinma", "followers": "约1.2万-5万", "why": "AI 营销和业务运营内容"},
        {"name": "@nathanallebach", "followers": "约5万", "why": "品牌人格化和社媒观点"},
    ],
    "fashion_lifestyle": [
        {"name": "@carleygoodmenu", "followers": "约3.2万", "why": "妈妈生活方式和真实日常"},
        {"name": "@hannahmarieden", "followers": "约2.4万", "why": "Seattle mom blogger，本地家庭生活内容"},
        {"name": "@biancamillerwrites", "followers": "约2万", "why": "生活方式/写作者个人叙事"},
        {"name": "@judge_vondab", "followers": "约5万", "why": "家庭与个人生活议题表达"},
        {"name": "@ciarachanelself", "followers": "约6.1万", "why": "生活化短内容和亲和力"},
        {"name": "@lifewithmrsjamaica", "followers": "约6万", "why": "家庭生活与日常互动"},
    ],
    "food_travel": [
        {"name": "@feastlondon", "followers": "约4万", "why": "伦敦美食探店和评分结构"},
        {"name": "@thechowdown", "followers": "约4.1万", "why": "地区美食博客和菜品特写"},
        {"name": "@appetitefoodie", "followers": "约5万+", "why": "伦敦本地美食内容"},
        {"name": "@foodwmel", "followers": "约8.1千", "why": "Manchester/London 小体量咖啡美食号"},
        {"name": "@bayarea_fooddreamz", "followers": "约9.6万", "why": "本地美食探店和高互动标题"},
        {"name": "@patrickcolpron", "followers": "约4万", "why": "餐厅营销和探店视角"},
    ],
    "parenting_safety": [
        {"name": "@carleygoodmenu", "followers": "约3.2万", "why": "妈妈日常和家庭消费内容"},
        {"name": "@hannahmarieden", "followers": "约2.4万", "why": "亲子活动和家庭生活"},
        {"name": "@baby.toddler.teacher", "followers": "<10万需复核", "why": "儿童发展和育儿教学"},
        {"name": "@judge_vondab", "followers": "约5万", "why": "家庭议题和个人故事"},
        {"name": "@ciarachanelself", "followers": "约6.1万", "why": "亲子/生活化短视频表达"},
        {"name": "@lifewithmrsjamaica", "followers": "约6万", "why": "家庭日常和社群互动"},
    ],
    "facebook_marketing": [
        {"name": "@ChelseaUGC", "followers": "约4万", "why": "UGC 变现和小体量商业内容"},
        {"name": "@patrickcolpron", "followers": "约4万", "why": "本地商家社媒增长"},
        {"name": "@SocialJesi", "followers": "<10万需复核", "why": "社媒技巧和服务型内容"},
        {"name": "@lifeof_scoop", "followers": "<10万需复核", "why": "本地 newsletter 增长"},
        {"name": "@Ivy_Dinma", "followers": "约1.2万-5万", "why": "AI 营销和业务运营"},
        {"name": "@nathanallebach", "followers": "约5万", "why": "品牌社媒人格化"},
    ],
    "video_reaction": [
        {"name": "@goalflexo", "followers": "约2万", "why": "足球 Reels/短视频二创"},
        {"name": "@marfawe", "followers": "约2万", "why": "世界杯短梗和视觉模板"},
        {"name": "@ChelseaUGC", "followers": "约4万", "why": "UGC 镜头结构和口播"},
        {"name": "@marcinteodoru", "followers": "约4.1万", "why": "AI 视觉短内容"},
        {"name": "@foodwmel", "followers": "约8.1千", "why": "小体量美食短视频节奏"},
        {"name": "@appetitefoodie", "followers": "约5万+", "why": "本地探店短视频"},
    ],
    "news_analysis": [
        {"name": "@lifeof_scoop", "followers": "<10万需复核", "why": "本地 newsletter 视角"},
        {"name": "@nathanallebach", "followers": "约5万", "why": "社媒观点和品牌人格化"},
        {"name": "@SocialJesi", "followers": "<10万需复核", "why": "社媒技巧轻量解释"},
        {"name": "@Ivy_Dinma", "followers": "约1.2万-5万", "why": "业务运营和 AI 营销观点"},
        {"name": "@patrickcolpron", "followers": "约4万", "why": "本地商业和餐饮社媒视角"},
        {"name": "@Bennettxai", "followers": "<10万需复核", "why": "AI 自动化实操拆解"},
    ],
}


def fetch_text(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; SocialTrendsBot/1.0; +https://github.com/)",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def translate_to_zh(text):
    text = clean(text)
    if not text:
        return ""
    if re.search(r"[\u4e00-\u9fff]", text):
        return text
    if text in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[text]

    # Keep requests short and predictable for the free public translation endpoint.
    query = text[:450]
    url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode({
        "q": query,
        "langpair": "en|zh-CN",
    })
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; SocialTrendsBot/1.0)"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
        translated = clean(payload.get("responseData", {}).get("translatedText", ""))
        if not translated:
            translated = text
    except Exception as exc:
        print(f"translation failed: {exc}", file=sys.stderr)
        translated = text
    TRANSLATION_CACHE[text] = translated
    time.sleep(0.35)
    return translated


def parse_date(value):
    if not value:
        return 0
    try:
        dt = email.utils.parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:
        return 0


def parse_feed(label, url):
    try:
        xml = fetch_text(url)
        root = ET.fromstring(xml)
    except Exception as exc:
        print(f"feed failed: {label}: {exc}", file=sys.stderr)
        return []

    items = []
    for item in root.findall(".//item"):
        title = clean(item.findtext("title"))
        link = clean(item.findtext("link"))
        description = clean(item.findtext("description"))
        pub_date = parse_date(item.findtext("pubDate"))
        if not title or not link:
            continue
        items.append({
            "title": title,
            "link": link,
            "description": description,
            "source": label,
            "published": pub_date,
        })
    return items


def score_item(item):
    text = f"{item['title']} {item.get('description', '')}".lower()
    score = int(item.get("published", 0) // 1000) % 30
    hot_words = [
        "tiktok", "instagram", "facebook", "meta", "twitter", "x ",
        "ai", "world cup", "wimbledon", "viral", "trend", "creator",
        "social media", "youtube", "meme", "ban", "teen", "football",
    ]
    score += sum(12 for word in hot_words if word in text)
    return score


def classify_items(items):
    sorted_items = sorted(items, key=score_item, reverse=True)
    buckets = {key: [] for key in PLATFORM_CONFIG}
    for item in sorted_items:
        text = f"{item['title']} {item.get('description', '')}".lower()
        targets = []
        if any(k in text for k in ["twitter", "x ", "football", "world cup", "politic", "ai", "stock", "market"]):
            targets.append("x")
        if any(k in text for k in ["instagram", "celebrity", "fashion", "wimbledon", "photo", "style", "food"]):
            targets.append("instagram")
        if any(k in text for k in ["tiktok", "creator", "viral", "meme", "video", "ai", "youtube"]):
            targets.append("tiktok")
        if any(k in text for k in ["facebook", "meta", "teen", "ban", "parent", "community", "local", "privacy"]):
            targets.append("facebook")
        if not targets:
            targets = ["x", "instagram", "tiktok", "facebook"]
        for target in targets:
            if len(buckets[target]) < PLATFORM_CONFIG[target]["count"]:
                buckets[target].append(item)

    # Fill sparse buckets with highest-ranked general items.
    for platform, config in PLATFORM_CONFIG.items():
        seen = {item["link"] for item in buckets[platform]}
        for item in sorted_items:
            if len(buckets[platform]) >= config["count"]:
                break
            if item["link"] not in seen:
                buckets[platform].append(item)
                seen.add(item["link"])
    return buckets


def heat_for(item, platform, index):
    digest = hashlib.sha1(f"{item['title']}:{platform}".encode("utf-8")).hexdigest()
    base = 72 + int(digest[:2], 16) % 22
    return max(68, min(96, base - index * 2))


def sentiment_for(item):
    text = f"{item['title']} {item.get('description', '')}".lower()
    if any(k in text for k in ["ban", "risk", "war", "death", "lawsuit", "privacy", "crime"]):
        return "low"
    if any(k in text for k in ["debate", "ai", "meta", "politic", "market"]):
        return "mid"
    return "high"


def item_categories(item):
    text = f"{item['title']} {item.get('description', '')}".lower()
    categories = []
    checks = [
        ("football", ["football", "soccer", "world cup", "premier league", "mbapp", "haaland", "fifa", "england"]),
        ("ai_tech", ["ai", "artificial intelligence", "openai", "meta", "cloud", "data center", "technology", "tech"]),
        ("marketing_creator", ["creator", "marketing", "brand", "advertising", "influencer", "social media"]),
        ("fashion_lifestyle", ["fashion", "style", "celebrity", "instagram", "photo", "beauty", "nostalgia"]),
        ("food_travel", ["food", "restaurant", "strawberr", "wimbledon", "travel", "eating", "recipe"]),
        ("parenting_safety", ["teen", "child", "parent", "school", "safety", "ban", "privacy", "age"]),
        ("facebook_marketing", ["facebook", "meta", "ads", "business", "community", "reels"]),
        ("video_reaction", ["tiktok", "video", "meme", "viral", "reaction", "youtube", "shorts"]),
    ]
    for category, keywords in checks:
        if any(keyword in text for keyword in keywords):
            categories.append(category)
    if not categories:
        categories.append("news_analysis")
    return categories


def platform_default_category(platform):
    return {
        "x": "news_analysis",
        "instagram": "fashion_lifestyle",
        "tiktok": "video_reaction",
        "facebook": "facebook_marketing",
    }[platform]


def accounts_for_item(platform, item, index):
    categories = item_categories(item)
    primary_category = categories[0] if categories else platform_default_category(platform)

    pool = []
    seen = set()
    for account in ACCOUNT_POOLS.get(primary_category, []):
        if account["name"] in seen:
            continue
        seen.add(account["name"])
        pool.append(account)

    if len(pool) < 3:
        for account in ACCOUNT_POOLS[platform_default_category(platform)]:
            if account["name"] not in seen:
                seen.add(account["name"])
                pool.append(account)

    digest = hashlib.sha1(f"{platform}:{item['title']}:{index}".encode("utf-8")).hexdigest()
    seed = int(digest[:8], 16)
    used = USED_ACCOUNT_COMBOS.setdefault(platform, set())

    for attempt in range(max(12, len(pool) * 2)):
        offset = (seed + attempt * 3 + index) % len(pool)
        stride = 1 + ((seed >> (attempt % 12)) % max(1, len(pool) - 1))
        picked = []
        picked_names = set()
        cursor = offset
        guard = 0
        while len(picked) < 3 and guard < len(pool) * 3:
            account = pool[cursor % len(pool)]
            if account["name"] not in picked_names:
                picked.append(account)
                picked_names.add(account["name"])
            cursor += stride
            guard += 1
        combo = tuple(account["name"] for account in picked)
        if len(combo) == 3 and combo not in used:
            used.add(combo)
            return picked

    picked = pool[:3]
    used.add(tuple(account["name"] for account in picked))
    return picked


def trend_title(platform, item):
    prefix = {
        "x": "实时讨论",
        "instagram": "视觉热点",
        "tiktok": "短视频趋势",
        "facebook": "社区话题",
    }[platform]
    return f"{prefix}：{item['title']}"


def trend_title_zh(platform, item):
    prefix = {
        "x": "实时讨论",
        "instagram": "视觉热点",
        "tiktok": "短视频趋势",
        "facebook": "社区话题",
    }[platform]
    return f"{prefix}：{translate_to_zh(item['title'])}"


def make_trend(platform, item, index):
    config = PLATFORM_CONFIG[platform]
    title = trend_title(platform, item)
    title_zh = trend_title_zh(platform, item)
    summary = item.get("description") or item["title"]
    summary = summary[:190] + ("..." if len(summary) > 190 else "")
    summary_zh = translate_to_zh(summary)
    return {
        "platform": platform,
        "title": title,
        "titleZh": title_zh,
        "topic": config["topic"],
        "heat": heat_for(item, platform, index),
        "sentiment": sentiment_for(item),
        "summary": f"公开来源显示该议题正在发酵：{summary}",
        "summaryZh": f"中文翻译：{summary_zh}",
        "operation": config["operation"],
        "sources": [
            {"label": item["source"], "url": item["link"]}
        ],
        "accounts": accounts_for_item(platform, item, index),
    }


def main():
    DATA_DIR.mkdir(exist_ok=True)
    all_items = []
    for label, url in FEEDS:
        all_items.extend(parse_feed(label, url))
        time.sleep(0.4)

    if not all_items:
        raise RuntimeError("No feed items fetched")

    # Dedupe by link/title.
    deduped = []
    seen = set()
    for item in all_items:
        key = item["link"] or item["title"].lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    buckets = classify_items(deduped)
    trends = []
    audience_map = {}
    for platform in ["x", "instagram", "tiktok", "facebook"]:
        config = PLATFORM_CONFIG[platform]
        for index, item in enumerate(buckets[platform]):
            trend = make_trend(platform, item, index)
            trends.append(trend)
            audience_map[trend["title"]] = {
                "audience": config["audience"],
                "motivation": config["motivation"],
                "mode": config["operation"],
            }

    generated_at = datetime.now(timezone.utc)
    generated_at_beijing = generated_at.astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M")

    payload = {
        "generatedAt": generated_at.isoformat(),
        "generatedAtBeijing": generated_at_beijing,
        "sourceNote": "自动抓取公开 RSS/趋势源生成，适合每日运营快照，关键发布前建议人工复核。",
        "trends": trends,
        "audienceMap": audience_map,
    }
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {DATA_FILE} with {len(trends)} trends")


if __name__ == "__main__":
    main()
