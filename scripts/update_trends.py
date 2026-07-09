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
        "accounts": config["accounts"],
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

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceNote": "自动抓取公开 RSS/趋势源生成，适合每日运营快照，关键发布前建议人工复核。",
        "trends": trends,
        "audienceMap": audience_map,
    }
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {DATA_FILE} with {len(trends)} trends")


if __name__ == "__main__":
    main()
