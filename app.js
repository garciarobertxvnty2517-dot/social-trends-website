const DATA_URL = "data/trends.json";

const platformMeta = {
  x: {
    name: "X / Twitter",
    summary: "实时观点、新闻发酵、体育争议、科技圈讨论"
  },
  instagram: {
    name: "Instagram",
    summary: "视觉化热点、Reels、轮播、生活方式与名人内容"
  },
  tiktok: {
    name: "TikTok",
    summary: "短视频挑战、趋势音频、创作者经济、原生口播"
  },
  facebook: {
    name: "Facebook",
    summary: "社区讨论、家庭消费、本地化、Reels 二次分发"
  }
};

let trends = [
  {
    platform: "x",
    title: "美国队 Balogun 红牌禁赛被撤销引发争议",
    topic: "世界杯、VAR、体育争议、政治介入讨论",
    heat: 96,
    sentiment: "mid",
    summary: "2026 世界杯期间，美国前锋 Folarin Balogun 的红牌停赛被 FIFA 撤销，围绕 VAR、纪律规则和政治影响的讨论迅速升温。",
    operation: "X 上适合做事实线梳理和观点帖：先列时间线，再给出“规则争议在哪里”，避免用阴谋论口吻下结论。",
    sources: [
      { label: "The Guardian", url: "https://www.theguardian.com/football/2026/jul/06/folarin-balogun-red-card-reversal-trump-calls-fifa-explainer" },
      { label: "Axios", url: "https://www.axios.com/2026/07/05/folarin-balogun-cleared-usmnt-belgium-fifa-red-card" }
    ],
    accounts: [
      { name: "@FabrizioRomano", why: "足球新闻快讯节奏" },
      { name: "@MenInBlazers", why: "体育梗和球迷语气" },
      { name: "@tombogert", why: "美国足球信息源" }
    ]
  },
  {
    platform: "x",
    title: "Haaland 带挪威击败巴西后的社媒玩笑帖",
    topic: "世界杯爆冷、球星表达、meme、体育情绪",
    heat: 91,
    sentiment: "high",
    summary: "挪威击败巴西后，Haaland 的社媒庆祝内容放大了“爆冷”和“28 年等待”的情绪，体育内容号快速跟进。",
    operation: "适合 X 快反：借“爆冷/反转/等待终于值得”这类情绪，不攻击球队或球迷。品牌可用一句短梗带出产品场景。",
    sources: [
      { label: "The Sun", url: "https://www.thesun.ie/sport/17242396/erling-haaland-goat-instagram-world-cup-brazil/" },
      { label: "Times of India", url: "https://timesofindia.indiatimes.com/sports/football/fifa-world-cup/erling-haaland-mocks-brazil-with-laughing-post-after-ending-selecaos-world-cup-dream/articleshow/132204943.cms" }
    ],
    accounts: [
      { name: "@FabrizioRomano", why: "一句话快讯 + 情绪符号" },
      { name: "@TrollFootball", why: "体育 meme 反应速度" },
      { name: "@utdreport", why: "球迷号标题写法" }
    ]
  },
  {
    platform: "x",
    title: "Meta AI 与云服务野心引发科技圈讨论",
    topic: "Meta、AI 模型、云服务、科技股",
    heat: 84,
    sentiment: "mid",
    summary: "Meta 被报道探索云服务和 AI 模型访问，同时高管称内部模型能力追上头部模型，引发科技、投资和 AI 从业者讨论。",
    operation: "X 适合做观点 thread：第一条给判断“Meta 正从社交平台变成 AI 基建玩家”，后续拆业务、广告、开发者生态影响。",
    sources: [
      { label: "Axios", url: "https://www.axios.com/2026/07/01/meta-cloud-mark-zuckerberg" },
      { label: "Business Insider", url: "https://www.businessinsider.com/meta-ai-model-catches-up-openai-gpt-5-says-2026-7" }
    ],
    accounts: [
      { name: "@benedictevans", why: "科技趋势大图景" },
      { name: "@stratechery", why: "商业模式拆解" },
      { name: "@swyx", why: "AI 开发者视角" }
    ]
  },
  {
    platform: "x",
    title: "AI 广告泡沫与创作者价值再讨论",
    topic: "AI 广告、Creator Economy、营销效率、内容信任",
    heat: 80,
    sentiment: "mid",
    summary: "广告行业围绕 AI 是否能替代创意、创作者是否会被过度商业化继续争论，适合做营销观点内容。",
    operation: "用“AI 能提效，但不能替代创作者信任”做观点帖，附 3 个品牌应避免的错误：过度模板化、无授权复刻、忽视评论反馈。",
    sources: [
      { label: "The Verge", url: "https://www.theverge.com/podcast/959792/digitas-ceo-amy-lanzi-cannes-ad-industry-marketing-ai-creators" },
      { label: "Business Insider", url: "https://www.businessinsider.com/social-giants-build-ai-future-creators-less-power-2026-3" }
    ],
    accounts: [
      { name: "@MarketingBrew", why: "营销新闻角度" },
      { name: "@gregisenberg", why: "创业和内容商业化观点" },
      { name: "@KatelynBourgoin", why: "消费者心理拆解" }
    ]
  },
  {
    platform: "instagram",
    title: "Wimbledon 草莓奶油份量争议",
    topic: "Wimbledon、shrinkflation、现场体验、体育生活方式",
    heat: 78,
    sentiment: "mid",
    summary: "温网经典草莓奶油被观众质疑份量不足，话题从赛事小吃延伸到 shrinkflation 和消费体验。",
    operation: "Instagram 适合做轮播：“一个甜品为什么能引发讨论”。品牌可借势做价格透明、份量对比、用户投票。",
    sources: [
      { label: "Times of India", url: "https://timesofindia.indiatimes.com/sports/international-sports/not-enough-strawberries-wimbledon-fans-question-famous-dessert-as-complaints-mount/articleshow/132204794.cms" }
    ],
    accounts: [
      { name: "@eatlikeagirl", why: "食物故事和旅行语境" },
      { name: "@londonfoodbabes", why: "伦敦本地美食热点" },
      { name: "@halfbakedharvest", why: "美食视觉和配方包装" }
    ]
  },
  {
    platform: "instagram",
    title: "“2026 is the new 2016” 复古滤镜与老照片回潮",
    topic: "怀旧、老照片、滤镜、明星旧照",
    heat: 88,
    sentiment: "high",
    summary: "用户和名人重发 2016 年照片，复刻 Snapchat 滤镜、亮色自拍、早期 Instagram 审美，适合视觉平台扩散。",
    operation: "Instagram 可做“品牌 2016 回忆杀”轮播：旧视觉、旧产品、旧广告语和现在对比，最后一页引导用户评论自己的 2016。",
    sources: [
      { label: "Trend background", url: "https://en.wikipedia.org/wiki/2026_is_the_new_2016" },
      { label: "The Sun", url: "https://www.the-sun.com/tech/15779870/2026-2016-tiktok-instagram-social-media-nostalgia/" }
    ],
    accounts: [
      { name: "@matildadjerf", why: "复古生活方式审美" },
      { name: "@devonleecarlson", why: "个人风格和怀旧视觉" },
      { name: "@oldloserinbrooklyn", why: "潮流趋势解释" }
    ]
  },
  {
    platform: "instagram",
    title: "Haaland 赢球庆祝内容带动体育明星图像传播",
    topic: "世界杯、球星社媒、庆祝帖、粉丝互动",
    heat: 86,
    sentiment: "high",
    summary: "Haaland 凭借世界杯进球和庆祝帖获得大量社媒讨论，Instagram 上的图像化庆祝、评论互动和二创空间很强。",
    operation: "品牌可模仿“胜利瞬间 + 短句 caption + 评论区互动”结构，做用户成就、挑战完成或新品达成类内容。",
    sources: [
      { label: "The Sun", url: "https://www.thesun.ie/sport/17242396/erling-haaland-goat-instagram-world-cup-brazil/" }
    ],
    accounts: [
      { name: "@fabriziorom", why: "体育新闻图文快发" },
      { name: "@footballersfits", why: "球星生活方式二创" },
      { name: "@433skills", why: "足球短视频剪辑感" }
    ]
  },
  {
    platform: "instagram",
    title: "Wimbledon AI fan experience 让传统赛事变成打卡内容",
    topic: "AI 体验、赛事现场、打卡、粉丝互动",
    heat: 73,
    sentiment: "mid",
    summary: "温网现场加入 AI 互动体验，引发“传统体育如何拥抱科技”的讨论，也给 Reels 和 Story 提供打卡素材。",
    operation: "适合做 Story 问答和 Reels：展示体验入口、用户表情、结果画面，再引导“你愿意把脸交给 AI 生成吗？”",
    sources: [
      { label: "The Guardian", url: "https://www.theguardian.com/sport/2026/jun/29/wimbledon-2026-diary-football-world-cup-home-nation-heartbreaks-tennis" }
    ],
    accounts: [
      { name: "@thetennisletter", why: "网球热点快讯" },
      { name: "@rachelstenquist", why: "体育现场生活方式表达" },
      { name: "@caseymcquillen", why: "赛事体验短视频" }
    ]
  },
  {
    platform: "tiktok",
    title: "“2026 is the new 2016” 复古挑战与旧音频",
    topic: "怀旧、2016 音乐、老挑战、复古穿搭",
    heat: 92,
    sentiment: "high",
    summary: "TikTok 用户复刻 2016 年音乐、挑战、滤镜和流行文化，形成跨平台怀旧内容潮。",
    operation: "TikTok 可做“品牌或产品回到 2016 会长什么样”。使用老照片、低像素滤镜、经典音频和前后对比，植入品牌记忆点。",
    sources: [
      { label: "Trend background", url: "https://en.wikipedia.org/wiki/2026_is_the_new_2016" },
      { label: "The Sun", url: "https://www.the-sun.com/tech/15779870/2026-2016-tiktok-instagram-social-media-nostalgia/" }
    ],
    accounts: [
      { name: "@zachking", why: "高完成度视觉反转" },
      { name: "@charlidamelio", why: "舞蹈和流行文化节奏" },
      { name: "@wisdm8", why: "趋势解析与青年文化" }
    ]
  },
  {
    platform: "tiktok",
    title: "MrBeast 招聘 Head of TikTok 显示短视频运营工业化",
    topic: "创作者公司、TikTok 增长、内容团队、岗位化",
    heat: 87,
    sentiment: "high",
    summary: "MrBeast 团队招聘 TikTok 负责人，说明头部创作者正在把平台增长拆成专门岗位和流程。",
    operation: "适合做运营拆解视频：用“一个 TikTok 岗位到底管什么”作为 hook，拆选题、剪辑、测试、复盘和账号矩阵。",
    sources: [
      { label: "Business Insider", url: "https://www.businessinsider.com/mrbeast-is-hiring-a-head-of-tiktok-job-description-2026-2" }
    ],
    accounts: [
      { name: "@ryantrahan", why: "系列化叙事和挑战" },
      { name: "@airrack", why: "大型挑战和快节奏剪辑" },
      { name: "@colinandsamir", why: "创作者经济分析" }
    ]
  },
  {
    platform: "tiktok",
    title: "AI 与创作者关系紧张：平台工具替代焦虑",
    topic: "AI 头像、创作者经济、授权、商业化",
    heat: 86,
    sentiment: "low",
    summary: "社媒平台加速 AI 工具布局，创作者担心自己的内容、形象和商业机会被平台 AI 产品稀释。",
    operation: "TikTok 适合用真人口播解释“AI 工具能帮创作者什么、不能替代什么”。品牌应强调授权、分成和透明度。",
    sources: [
      { label: "Business Insider", url: "https://www.businessinsider.com/social-giants-build-ai-future-creators-less-power-2026-3" },
      { label: "The Verge", url: "https://www.theverge.com/podcast/959792/digitas-ceo-amy-lanzi-cannes-ad-industry-marketing-ai-creators" }
    ],
    accounts: [
      { name: "@alisa_earle", why: "生活方式商业化" },
      { name: "@alanchikinchow", why: "短剧和系列化叙事" },
      { name: "@marketingexamined", why: "营销拆解型内容" }
    ]
  },
  {
    platform: "tiktok",
    title: "Wimbledon 草莓争议适合做“现场体验吐槽”短视频",
    topic: "赛事美食、吐槽、价格体验、旅行现场",
    heat: 76,
    sentiment: "mid",
    summary: "草莓份量争议在短视频语境中容易被包装成“我花了多少钱，得到什么”的现场体验内容。",
    operation: "用 POV 结构：先展示账单或排队场景，再给实物特写，最后给一句反差评价。评论区引导用户晒其他现场消费坑。",
    sources: [
      { label: "Times of India", url: "https://timesofindia.indiatimes.com/sports/international-sports/not-enough-strawberries-wimbledon-fans-question-famous-dessert-as-complaints-mount/articleshow/132204794.cms" }
    ],
    accounts: [
      { name: "@jordan_the_stallion8", why: "食品和文化梗讲述" },
      { name: "@keith_lee125", why: "真实试吃和评分结构" },
      { name: "@eitan", why: "美食短视频节奏" }
    ]
  },
  {
    platform: "tiktok",
    title: "体育爆冷被剪成反应视频与二创模板",
    topic: "世界杯、反应视频、球迷情绪、二创",
    heat: 82,
    sentiment: "high",
    summary: "世界杯爆冷、球星庆祝和球迷反应天然适合被剪成短视频模板，带动 reaction、duet、stitch 内容。",
    operation: "品牌可用“没人想到会这样”作为 hook，接自己的产品反转或用户故事。注意避免使用未授权比赛画面。",
    sources: [
      { label: "The Sun", url: "https://www.thesun.ie/sport/17242396/erling-haaland-goat-instagram-world-cup-brazil/" }
    ],
    accounts: [
      { name: "@ishowspeed", why: "体育反应情绪强" },
      { name: "@thef2", why: "足球技巧和二创" },
      { name: "@footballdaily", why: "短视频体育新闻口吻" }
    ]
  },
  {
    platform: "facebook",
    title: "未成年人社媒年龄限制接近政策拐点",
    topic: "社媒监管、青少年安全、家庭讨论、平台信任",
    heat: 82,
    sentiment: "low",
    summary: "多国推进或讨论 16 岁以下社媒访问限制，Facebook 上更容易形成家长、学校、社区之间的长讨论。",
    operation: "Facebook 适合做社区型讨论：以“家长如何平衡安全与数字能力”开题，品牌站在教育和工具支持角度，避免硬广。",
    sources: [
      { label: "The Guardian", url: "https://www.theguardian.com/world/2026/jun/28/tech-firms-are-losing-the-public-social-media-age-bans-near-tipping-point" },
      { label: "Guardian smartphone ban study", url: "https://www.theguardian.com/politics/2026/jun/30/school-smartphone-ban-seen-as-punitive-by-young-people-report" }
    ],
    accounts: [
      { name: "Common Sense Media", why: "家庭科技教育内容" },
      { name: "Dr. Becky at Good Inside", why: "家长心理和教育表达" },
      { name: "Scary Mommy", why: "父母社群讨论语气" }
    ]
  },
  {
    platform: "facebook",
    title: "Meta AI、云服务和数据中心投入成为社区讨论素材",
    topic: "Meta、AI 基建、云服务、科技商业",
    heat: 79,
    sentiment: "mid",
    summary: "Meta 被报道探索云服务与 AI 模型访问，Facebook 上更适合转化为“AI 会如何影响普通用户和商家”的讨论。",
    operation: "适合长帖：用普通商家视角讲 AI 工具、广告投放、客服自动化和数据隐私，结尾提问引导评论。",
    sources: [
      { label: "Axios", url: "https://www.axios.com/2026/07/01/meta-cloud-mark-zuckerberg" },
      { label: "Business Insider", url: "https://www.businessinsider.com/meta-ai-model-catches-up-openai-gpt-5-says-2026-7" }
    ],
    accounts: [
      { name: "Neil Patel", why: "中小企业营销教育" },
      { name: "Mari Smith", why: "Facebook 营销教学" },
      { name: "Jon Loomer", why: "Meta 广告实操拆解" }
    ]
  },
  {
    platform: "facebook",
    title: "Facebook Reels 与创作者变现继续适合社区复用",
    topic: "Reels、短视频、创作者变现、社群分发",
    heat: 74,
    sentiment: "high",
    summary: "Facebook Reels 仍是 Meta 短视频生态的一部分，适合把 TikTok/Instagram 的高表现短内容改写成本地社区版本。",
    operation: "运营上先用 Reels 做短引子，再把评论区高频问题整理成长帖或群组讨论。适合本地服务、教育、家庭消费品牌。",
    sources: [
      { label: "Facebook Reels background", url: "https://en.wikipedia.org/wiki/Facebook_Reels" }
    ],
    accounts: [
      { name: "Nas Daily", why: "短视频故事化" },
      { name: "Dhar Mann", why: "强情绪短剧" },
      { name: "Jay Shetty", why: "观点型短内容" }
    ]
  },
  {
    platform: "facebook",
    title: "2016 怀旧潮适合 Facebook 老照片与社群回忆帖",
    topic: "怀旧、老照片、社群互动、用户回忆",
    heat: 72,
    sentiment: "high",
    summary: "“2026 is the new 2016” 不只在 TikTok 和 Instagram 传播，也适合 Facebook 的老照片、同城群组和校友社群互动。",
    operation: "发布“晒出你 2016 年的一张照片”或“2016 年你最怀念什么”的帖子，配合品牌老包装/老活动图做互动。",
    sources: [
      { label: "Trend background", url: "https://en.wikipedia.org/wiki/2026_is_the_new_2016" }
    ],
    accounts: [
      { name: "Humans of New York", why: "回忆和人物故事" },
      { name: "The Holderness Family", why: "家庭场景和怀旧幽默" },
      { name: "Laura Clery", why: "生活化喜剧表达" }
    ]
  }
];

let audienceMap = {
  "美国队 Balogun 红牌禁赛被撤销引发争议": {
    audience: "美国足球迷、世界杯观众、体育评论账号、关注规则公平性的泛体育用户。",
    motivation: "这类受众关心的不只是球员本身，而是“规则是否公平”“主队是否被针对”“权力是否影响体育”。争议越清晰，评论和转发越容易被点燃。",
    mode: "运营上用事实时间线降低争议风险，再用开放式问题引导讨论，例如“这次判罚撤销合理吗？”适合新闻快评、体育装备、观赛酒水和体育投注相关品牌谨慎借势。"
  },
  "Haaland 带挪威击败巴西后的社媒玩笑帖": {
    audience: "年轻足球迷、球星粉丝、meme 爱好者、关注爆冷剧情的轻度体育用户。",
    motivation: "他们被“强队翻车”“球星整活”“小国逆袭”吸引，参与方式偏情绪化和娱乐化。",
    mode: "用轻松、短句、反转式文案切入，不要站队攻击。适合做“没人想到会这样”的产品反转、挑战达成和品牌胜利时刻。"
  },
  "Meta AI 与云服务野心引发科技圈讨论": {
    audience: "科技从业者、AI 开发者、投资人、B2B SaaS 运营、数字营销团队。",
    motivation: "他们关注 Meta 是否会改变 AI 基建格局、广告生态和开发者机会，讨论更理性，喜欢数据和商业拆解。",
    mode: "适合长 thread、图解和观点卡片。用“这对开发者/广告主/创作者意味着什么”拆成 3 到 5 点，避免空泛喊 AI 趋势。"
  },
  "AI 广告泡沫与创作者价值再讨论": {
    audience: "营销人、品牌主、创作者、广告代理商、内容创业者。",
    motivation: "他们既期待 AI 降低内容成本，又担心内容失去真实感和创作者议价权下降。",
    mode: "用案例型内容最有效：展示 AI 适合做什么、不适合做什么，再给出授权、透明、分成和品牌安全建议。"
  },
  "Wimbledon 草莓奶油份量争议": {
    audience: "网球观众、英国本地用户、美食内容受众、对 shrinkflation 敏感的消费者。",
    motivation: "传统赛事符号叠加“份量变少/价格不值”的消费情绪，容易引发吐槽和生活化共鸣。",
    mode: "Instagram 做视觉对比，TikTok 做现场 POV，Facebook 做消费讨论。食品、旅行、零售品牌可以借“值不值”做互动投票。"
  },
  "“2026 is the new 2016” 复古滤镜与老照片回潮": {
    audience: "Gen Z、年轻千禧一代、时尚美妆用户、怀旧文化爱好者。",
    motivation: "受众想通过旧滤镜、旧音乐和旧穿搭获得轻松的身份表达，也是在逃离过度精致内容。",
    mode: "运营重点是低门槛参与：旧照对比、品牌旧包装、2016 风格模板、用户投稿。不要做得太精致，否则会失去怀旧感。"
  },
  "Haaland 赢球庆祝内容带动体育明星图像传播": {
    audience: "Instagram 体育粉、球星粉丝、健身和男性时尚受众、视觉二创账号。",
    motivation: "他们喜欢英雄时刻、庆祝姿态、胜利情绪和可二创图片。",
    mode: "用强视觉首图加短 caption，评论区设置站队问题。运动、潮流、饮料和游戏品牌适合借“胜利瞬间”做轻量活动。"
  },
  "Wimbledon AI fan experience 让传统赛事变成打卡内容": {
    audience: "赛事现场观众、科技体验爱好者、旅游打卡用户、品牌活动策划人。",
    motivation: "他们关心新奇体验是否值得排队、是否适合拍照分享、是否有社交货币。",
    mode: "适合做 Reels/Story：入口、体验过程、生成结果、用户表情四步走。运营重点是制造可晒结果和可参与话题。"
  },
  "“2026 is the new 2016” 复古挑战与旧音频": {
    audience: "TikTok 年轻用户、舞蹈挑战参与者、复古穿搭用户、音乐梗内容创作者。",
    motivation: "他们更在意参与感和模板感，想用熟悉音频快速表达自己的变化或反差。",
    mode: "用统一音频和固定动作做模板，品牌只植入一个清晰记忆点。适合服饰、美妆、消费电子和校园品牌。"
  },
  "MrBeast 招聘 Head of TikTok 显示短视频运营工业化": {
    audience: "内容运营、创作者、MCN、短视频剪辑师、想进入 creator economy 的求职者。",
    motivation: "他们关注头部团队如何拆分岗位、如何规模化测试内容，以及普通创作者能学到什么。",
    mode: "用拆解型短视频：岗位职责、增长指标、内容流程、普通团队可复制版本。适合教育、工具、招聘和营销服务品牌。"
  },
  "AI 与创作者关系紧张：平台工具替代焦虑": {
    audience: "创作者、设计师、剪辑师、品牌合作负责人、AI 工具用户。",
    motivation: "他们担心平台用 AI 降低创作者价值，也关注是否能用 AI 提高效率和收入。",
    mode: "不要只讲工具功能，要讲授权、收益和边界。适合做“AI 助手而非替代者”的真人口播和案例复盘。"
  },
  "Wimbledon 草莓争议适合做“现场体验吐槽”短视频": {
    audience: "TikTok 美食用户、旅行用户、现场活动观众、价格敏感消费者。",
    motivation: "他们喜欢真实体验、价格对比和“花钱踩坑/值回票价”的即时判断。",
    mode: "用 POV + 价格 + 实物特写 + 一句话评价。品牌可以引导用户晒自己的现场消费体验，收集 UGC。"
  },
  "体育爆冷被剪成反应视频与二创模板": {
    audience: "体育短视频用户、reaction 内容受众、球迷社群、二创剪辑号。",
    motivation: "他们追求强情绪和即时反应，尤其喜欢“我当时的表情”和“没人想到”的共鸣。",
    mode: "运营上用反应模板和 stitch/duet 思路，但避免未授权赛事画面。品牌可用用户故事或产品场景替代比赛画面。"
  },
  "未成年人社媒年龄限制接近政策拐点": {
    audience: "家长、教育工作者、政策关注者、青少年安全组织、家庭消费用户。",
    motivation: "他们关心孩子安全、屏幕时间、社交能力和平台责任，讨论偏价值观和经验分享。",
    mode: "Facebook 适合长帖和群组问题：“你会支持 16 岁以下限制吗？”品牌应提供工具、清单和教育资源，不要制造恐慌。"
  },
  "Meta AI、云服务和数据中心投入成为社区讨论素材": {
    audience: "中小企业主、广告投放人员、AI 工具用户、Facebook 社群管理员。",
    motivation: "他们更关心 AI 会不会影响获客、广告成本、客服效率和隐私风险。",
    mode: "用普通商家视角写：AI 能帮你省什么、需要注意什么、如何开始测试。结尾用问题引导经验分享。"
  },
  "Facebook Reels 与创作者变现继续适合社区复用": {
    audience: "本地商家、家庭内容创作者、教育博主、Facebook 群组运营者。",
    motivation: "他们希望用短视频拿到更多曝光，但仍依赖 Facebook 的熟人和社区信任转化。",
    mode: "先用 Reels 做短引子，再把评论区问题沉淀成长帖。适合本地服务、课程、家庭消费和社区活动。"
  },
  "2016 怀旧潮适合 Facebook 老照片与社群回忆帖": {
    audience: "千禧一代、家庭用户、校友群、同城社区、老照片分享用户。",
    motivation: "Facebook 的怀旧内容更偏个人记忆和关系链互动，用户愿意晒旧照、讲故事、标记朋友。",
    mode: "用“晒出你 2016 的一张照片”做互动，品牌可放旧包装、旧活动、老用户故事，引导评论和转发。"
  }
};

const insights = {
  all: {
    title: "全平台组合策略",
    body: "当前页面按平台分区展示热点，不强行让数量一致。先判断热点在哪个平台天然适配，再决定内容形态：X 做观点与快讯，Instagram 做视觉化保存，TikTok 做短视频测试，Facebook 做社区讨论和复用。"
  },
  x: {
    title: "X / Twitter 策略",
    body: "核心是速度、态度和参与公共讨论。适合发布观点、数据、行业判断和创始人视角。引用新闻出处后再表达判断，可信度会明显提高。"
  },
  instagram: {
    title: "Instagram 策略",
    body: "核心是视觉统一和可保存价值。热点需要转成轮播、Reels 或 Story 互动，强调审美、教程、清单和生活方式表达。"
  },
  tiktok: {
    title: "TikTok 策略",
    body: "核心是 hook、节奏和原生表达。先跟随趋势形式，再放入品牌信息。参考账号不是照抄内容，而是拆解它们的开头、镜头、节奏和评论引导。"
  },
  facebook: {
    title: "Facebook 策略",
    body: "核心是社区信任和本地化。把热点转成用户能参与的问题、活动或实用清单，适合群组、长帖、直播和评论经营。"
  }
};

const trendList = document.querySelector("#trendList");
const insightBox = document.querySelector("#platformInsight");
const filterButtons = document.querySelectorAll(".filter-button");
const todayLabel = document.querySelector("#todayLabel");
const accountDirectory = document.querySelector("#accountDirectory");
const platformOrder = ["x", "instagram", "tiktok", "facebook"];

if (todayLabel) {
  todayLabel.textContent = new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date());
}

function sentimentText(value) {
  if (value === "high") return "正向";
  if (value === "mid") return "混合";
  return "谨慎";
}

function renderSources(sources) {
  return sources.map((source) => `
    <a class="source-link" href="${source.url}" target="_blank" rel="noopener noreferrer">出处：${source.label}</a>
  `).join("");
}

function renderAccounts(accounts) {
  return accounts.map((account) => `
    <span class="account-chip" title="${account.why}">
      ${account.name}${account.followers ? ` · ${account.followers}` : " · <10万粉丝需复核"} - ${account.why}
    </span>
  `).join("");
}

function renderTrendCard(trend) {
  const meta = platformMeta[trend.platform];
  const audience = audienceMap[trend.title] || {
    audience: "该平台核心兴趣用户和相关垂直内容受众。",
    motivation: "用户关注热点背后的情绪、利益变化和可参与讨论点。",
    mode: trend.operation
  };
  const translatedTitle = trend.titleZh && trend.titleZh !== trend.title ? `
    <div class="translation-box">
      <strong>中文标题：</strong>${trend.titleZh}
    </div>
  ` : "";
  const translatedSummary = trend.summaryZh ? `
    <p class="translation-summary"><strong>中文摘要：</strong>${trend.summaryZh.replace(/^中文翻译：/, "")}</p>
  ` : "";

  return `
    <article class="trend-card">
      <div>
        <div class="meta-row">
          <span class="pill">${meta.name}</span>
          <span class="pill">热度 ${trend.heat}</span>
          <span class="pill">${trend.topic}</span>
        </div>
        <h3>${trend.title}</h3>
        ${translatedTitle}
        <p>${trend.summary}</p>
        ${translatedSummary}
        <div class="audience-box">
          <p><strong>背后受众：</strong>${audience.audience}</p>
          <p><strong>关注动机：</strong>${audience.motivation}</p>
          <p><strong>运营方式：</strong>${audience.mode}</p>
        </div>
        <p><strong>运营建议：</strong>${trend.operation}</p>
        <div class="source-row">${renderSources(trend.sources)}</div>
        <div class="account-row">${renderAccounts(trend.accounts)}</div>
      </div>
      <div class="sentiment ${trend.sentiment}">
        ${sentimentText(trend.sentiment)}
      </div>
    </article>
  `;
}

function renderPlatformSection(platform) {
  const meta = platformMeta[platform];
  const platformTrends = trends.filter((trend) => trend.platform === platform);
  return `
    <section class="platform-section" data-section="${platform}">
      <div class="platform-heading">
        <div>
          <p class="eyebrow">${meta.name}</p>
          <h3>${meta.summary}</h3>
        </div>
        <span>${platformTrends.length} 条热点</span>
      </div>
      <div class="platform-cards">
        ${platformTrends.map(renderTrendCard).join("")}
      </div>
    </section>
  `;
}

function renderAccountDirectory() {
  accountDirectory.innerHTML = platformOrder.map((platform) => {
    const meta = platformMeta[platform];
    const platformTrends = trends.filter((trend) => trend.platform === platform);

    return `
      <article class="directory-card">
        <h3>${meta.name}</h3>
        ${platformTrends.map((trend) => `
          <div class="directory-item">
            <strong>${trend.titleZh || trend.title}</strong>
            ${trend.titleZh ? `<p class="directory-original">${trend.title}</p>` : ""}
            <div class="account-row">${renderAccounts(trend.accounts)}</div>
          </div>
        `).join("")}
      </article>
    `;
  }).join("");
}

function renderTrends(platform = "all") {
  const sections = platform === "all" ? platformOrder : [platform];
  trendList.innerHTML = sections.map(renderPlatformSection).join("");
}

function renderInsight(platform = "all") {
  const item = insights[platform];
  insightBox.innerHTML = `
    <h3>${item.title}</h3>
    <p>${item.body}</p>
  `;
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const platform = button.dataset.platform;
    renderTrends(platform);
    renderInsight(platform);
  });
});

async function loadDailyData() {
  const dataUpdatedAt = document.querySelector("#dataUpdatedAt");

  try {
    const response = await fetch(DATA_URL, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    if (Array.isArray(data.trends) && data.trends.length > 0) {
      trends = data.trends;
    }
    if (data.audienceMap && typeof data.audienceMap === "object") {
      audienceMap = { ...audienceMap, ...data.audienceMap };
    }
    if (data.generatedAt && dataUpdatedAt) {
      const updated = new Date(data.generatedAt);
      dataUpdatedAt.textContent = `数据源：公开热点源每日自动更新，更新时间 ${updated.toLocaleString("zh-CN")}`;
    }
  } catch (error) {
    if (dataUpdatedAt) {
      dataUpdatedAt.textContent = "数据源：当前显示内置样例；自动更新数据暂不可用";
    }
    console.warn("Daily trend data unavailable:", error);
  }
}

async function initApp() {
  await loadDailyData();
  renderTrends();
  renderInsight();
  renderAccountDirectory();
}

initApp();
