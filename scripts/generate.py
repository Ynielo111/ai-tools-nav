"""
AI ToolNav 静态页面生成器
从数据定义生成所有工具详情页和分类页
"""
import os
import json
import html as html_mod

# 输出目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
CATS_DIR = os.path.join(BASE_DIR, 'categories')
DOMAIN = "https://www.aitnav.com"

ADSENSE_SNIPPET = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6233913596766498" crossorigin="anonymous"></script>'
ANALYTICS_SNIPPET = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-NQTV1YBBLK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-NQTV1YBBLK');
</script>'''
GOOGLE_SITE_VERIFICATION = '<meta name="google-site-verification" content="VpHmBjp4J_z2x-rAtb7swV1jeCyoCpOuCQbC9Yfrkgw" />'

def common_head_snippets(include_ads=False):
    parts = [GOOGLE_SITE_VERIFICATION]
    if include_ads:
        parts.append(ADSENSE_SNIPPET)
    parts.append(ANALYTICS_SNIPPET)
    return "\n".join(parts)

def robots_for_tool(tool):
    return "noindex, follow"

os.makedirs(TOOLS_DIR, exist_ok=True)
os.makedirs(CATS_DIR, exist_ok=True)

# ===== 数据定义 =====
CATEGORIES = [
    {"id":"llm","name":"大语言模型","icon":"🤖","kw":"AI大模型 ChatGPT替代品 Claude对比","desc":"收录最好用的大语言模型和AI对话工具，包括ChatGPT、Claude、Gemini、DeepSeek等主流AI助手。提供真实使用评分与横向对比，帮你选择最适合的AI对话工具。"},
    {"id":"image","name":"AI 绘画","icon":"🎨","kw":"AI绘画工具 Midjourney Stable Diffusion AI生成图片","desc":"精选最热门的AI绘画与图像生成工具，从Midjourney到DALL·E 3，覆盖艺术创作、电商设计、游戏资产等场景的AI绘图工具推荐。"},
    {"id":"code","name":"AI 编程","icon":"💻","kw":"AI编程工具 GitHub Copilot Cursor AI写代码","desc":"程序员必备的AI编程助手与代码生成工具集合，包括GitHub Copilot、Cursor、Windsurf等，大幅提升开发效率的AI代码工具。"},
    {"id":"video","name":"AI 视频","icon":"🎬","kw":"AI视频生成 Sora Runway AI视频编辑","desc":"最新AI视频生成与编辑工具推荐，涵盖文生视频、数字人播报、AI剪辑等功能，帮您找到最适合的AI视频创作工具。"},
    {"id":"writing","name":"AI 写作","icon":"📝","kw":"AI写作工具 Jasper Grammarly AI文案生成","desc":"实用的AI写作与内容创作工具合集，包括AI文案、语法纠错、论文润色、SEO写作等功能，提升写作效率和质量。"},
    {"id":"audio","name":"AI 音频","icon":"🎵","kw":"AI音乐生成 Suno ElevenLabs AI配音","desc":"AI音频生成与处理工具排行榜，包含AI音乐创作、语音合成、声音克隆、配音旁白等功能的最热门AI音频工具。"},
    {"id":"office","name":"AI 办公","icon":"📊","kw":"AI办公工具 Gamma AI PPT Notion AI","desc":"提升办公效率的AI工具推荐，包括AI演示文稿、智能文档、会议纪要、知识管理等场景的最佳AI办公助手。"},
    {"id":"platform","name":"开发平台","icon":"🔧","kw":"AI开发平台 HuggingFace Dify AI模型部署","desc":"AI开发者必备的平台和工具集，涵盖模型托管、向量数据库、AI应用搭建、Bot开发等场景的顶级AI开发平台。"}
]

TOOLS = [
    # LLM
    {"name":"ChatGPT","desc":"OpenAI旗舰对话助手，支持GPT-4o多模态交互，全球用户量最大的AI工具","url":"https://chat.openai.com","category":"llm","icon":"🤖","tags":["对话","写作","编程","推理"],"rating":5,"review":"综合能力最强的AI助手，生态最完善","audience":"所有人","pricing":"免费增值","function":5,"price":3,"ease":4,"ecosystem":5,"pros":["综合能力最强的AI助手","插件生态极其丰富","GPT-4o多模态能力强","社区活跃、教程海量"],"cons":["高峰期使用时需要排队","Plus订阅费用较高","中文能力弱于国产模型","部分地区需要特殊网络"]},
    {"name":"Claude","desc":"Anthropic出品，安全优先的智能助手，超长上下文和代码理解能力突出","url":"https://claude.ai","category":"llm","icon":"💬","tags":["推理","编程","长文本","安全"],"rating":5,"review":"编程和长文档分析能力一流，Artifacts功能实用","audience":"专业人士","pricing":"免费增值","function":5,"price":3,"ease":4,"ecosystem":4,"pros":["编程和代码理解能力极强","超长上下文窗口","Artifacts 功能实用","安全性和对齐优秀"],"cons":["免费版有每日限额","多模态能力不如GPT-4o","中文支持尚可但非最优","知名度低于ChatGPT"]},
    {"name":"Gemini","desc":"Google多模态大模型，深度整合Google搜索、Gmail、地图等生态","url":"https://gemini.google.com","category":"llm","icon":"🧠","tags":["多模态","搜索","翻译","Google"],"rating":4,"review":"Google生态整合是独特优势，多模态能力出色","audience":"所有人","pricing":"免费增值","function":4,"price":4,"ease":4,"ecosystem":4,"pros":["Google 生态深度整合","多模态能力出色","免费版功能较慷慨","翻译能力顶级"],"cons":["中文回答质量不稳定","推理深度不如Claude","部分功能有地区限制","UI体验不如ChatGPT"]},
    {"name":"DeepSeek","desc":"国产高性能开源大模型，推理能力接近GPT-4，API价格仅为OpenAI的1/10","url":"https://chat.deepseek.com","category":"llm","icon":"🐋","tags":["开源","编程","推理","性价比"],"rating":5,"review":"性价比之王，编程和推理能力接近国际一线","audience":"所有人","pricing":"免费增值","function":5,"price":5,"ease":4,"ecosystem":3,"pros":["性价比极高","推理和编程能力强","开源可商用","中文理解优秀"],"cons":["多模态尚未完善","生态不如OpenAI","知名度还在增长中","企业服务有待完善"]},
    {"name":"Kimi","desc":"月之暗面出品，支持200万字超长上下文，适合论文阅读和长文档分析","url":"https://kimi.moonshot.cn","category":"llm","icon":"🌙","tags":["长文本","阅读","总结","中文"],"rating":4,"review":"长文本处理能力业界最强，论文党的好帮手","audience":"专业人士","pricing":"免费增值","function":4,"price":4,"ease":4,"ecosystem":3,"pros":["200万字超长上下文","论文和报告分析能力极强","中文处理能力出众","界面清爽易用"],"cons":["创意写作能力一般","编程能力不如DeepSeek","海外知名度低","不支持多模态"]},
    {"name":"通义千问","desc":"阿里云自研大模型，电商运营与中文办公场景表现突出","url":"https://tongyi.aliyun.com","category":"llm","icon":"☁️","tags":["中文","办公","阿里生态","免费"],"rating":4,"review":"国内免费大模型中功能最全面的选择","audience":"所有人","pricing":"免费","function":4,"price":5,"ease":3,"ecosystem":4,"pros":["免费使用","中文办公场景出色","阿里云生态集成","功能持续更新"],"cons":["推理深度一般","界面略复杂","创意能力中规中矩","API文档有待完善"]},

    # Image
    {"name":"Midjourney","desc":"顶级AI图像生成工具，艺术风格最丰富，设计社区活跃","url":"https://www.midjourney.com","category":"image","icon":"🎨","tags":["艺术","设计","高质感","创意"],"rating":5,"review":"出图质量天花板，艺术风格无人能及","audience":"专业人士","pricing":"付费","function":5,"price":2,"ease":3,"ecosystem":4,"pros":["出图质量业界最高","艺术风格极其丰富","创意自由度极高","社区活跃灵感多"],"cons":["需要订阅付费","操作需要学习Discord","没有免费试用额度","出图速度有时较慢"]},
    {"name":"DALL·E 3","desc":"OpenAI图像生成，与ChatGPT原生集成，文字理解准确度高","url":"https://openai.com/dall-e-3","category":"image","icon":"🖼️","tags":["对话生成","写实","易用","ChatGPT"],"rating":4,"review":"与ChatGPT联动是最大亮点，提示词理解最准","audience":"所有人","pricing":"付费","function":4,"price":3,"ease":5,"ecosystem":4,"pros":["提示词语义理解极准","与ChatGPT无缝联动","操作极其简单","文字渲染能力提升"],"cons":["需ChatGPT Plus订阅","风格多样性不如Midjourney","价格偏高","不支持本地部署"]},
    {"name":"Stable Diffusion","desc":"开源AI绘画模型，支持本地部署和自定义模型训练","url":"https://stability.ai","category":"image","icon":"🌄","tags":["开源","本地部署","可定制","免费"],"rating":4,"review":"自由度最高，技术党首选，社区模型生态丰富","audience":"专业人士","pricing":"免费","function":4,"price":5,"ease":2,"ecosystem":5,"pros":["完全免费开源","支持本地部署","可自定义模型训练","社区模型生态极丰富"],"cons":["需要较高技术门槛","需要好显卡","基础模型质量不如付费","缺少统一易用界面"]},
    {"name":"Leonardo.AI","desc":"专注游戏资产的AI图像生成，预设风格模板丰富","url":"https://leonardo.ai","category":"image","icon":"🎮","tags":["游戏","资产","风格","批量"],"rating":4,"review":"游戏和影视概念设计的最佳选择","audience":"专业人士","pricing":"免费增值","function":4,"price":4,"ease":4,"ecosystem":3,"pros":["游戏资产生成最佳","预设风格模板丰富","支持批量生成","每天免费额度大方"],"cons":["真实照片不如Midjourney","社区功能有限","API价格偏高","中文提示词支持弱"]},
    {"name":"Canva AI","desc":"Canva内置AI设计套件，模板海量，零设计基础也能用","url":"https://www.canva.com","category":"image","icon":"🎯","tags":["设计","模板","营销","易用"],"rating":4,"review":"非设计师最友好的AI设计工具，模板即用","audience":"初学者","pricing":"免费增值","function":4,"price":4,"ease":5,"ecosystem":5,"pros":["海量模板开箱即用","零设计基础友好","功能全面一站式","团队协作体验好"],"cons":["AI生成质量不及专业工具","免费版有水印","高级功能需付费","品牌定制能力弱"]},
    {"name":"Remove.bg","desc":"AI一键抠图去背景，速度快精度高，支持批量处理","url":"https://www.remove.bg","category":"image","icon":"✂️","tags":["抠图","背景","电商","快速"],"rating":4,"review":"抠图领域的事实标准，又快又准","audience":"所有人","pricing":"免费增值","function":4,"price":4,"ease":5,"ecosystem":3,"pros":["抠图速度极快","精度业界最高","支持批量处理","API集成方便"],"cons":["免费版下载分辨率低","高分辨率需付费","仅做抠图功能单一","批量处理限量"]},

    # Code
    {"name":"GitHub Copilot","desc":"GitHub出品，深度集成VS Code和JetBrains，代码补全的行业标杆","url":"https://github.com/features/copilot","category":"code","icon":"🐙","tags":["补全","IDE","微软","企业"],"rating":5,"review":"IDE集成的天花板，代码补全准确率最高","audience":"专业人士","pricing":"付费","function":5,"price":3,"ease":5,"ecosystem":5,"pros":["代码补全准确率极高","IDE集成无缝","支持所有主流语言","企业级安全性"],"cons":["需要付费订阅","多文件重构能力弱","不支持对话式编程","免费版功能有限"]},
    {"name":"Cursor","desc":"AI原生代码编辑器，基于VS Code但加入了对话式编程体验","url":"https://cursor.sh","category":"code","icon":"🖱️","tags":["编辑器","对话","重构","全文件"],"rating":5,"review":"目前最好用的AI IDE，多文件编辑能力一骑绝尘","audience":"专业人士","pricing":"免费增值","function":5,"price":4,"ease":5,"ecosystem":4,"pros":["多文件编辑能力最强","对话式编程体验好","免费版功能较慷慨","VS Code生态兼容"],"cons":["免费版有调用次数限制","依赖网络连接","稳定性偶有问题","企业版价格偏高"]},
    {"name":"Windsurf","desc":"Codeium出品的免费AI IDE，支持多文件编辑和Agent模式","url":"https://codeium.com/windsurf","category":"code","icon":"🌊","tags":["免费","多文件","Agent","快速"],"rating":4,"review":"免费替代Cursor的最佳选择，功能接近","audience":"所有人","pricing":"免费","function":4,"price":5,"ease":4,"ecosystem":3,"pros":["完全免费","功能接近Cursor","响应速度快","Agent模式实用"],"cons":["补全准确率略低于Copilot","生态尚在发展","团队协作功能弱","插件较少"]},
    {"name":"Claude Code","desc":"Anthropic终端AI编程代理，命令行直接操控整个代码库","url":"https://claude.ai/code","category":"code","icon":"⌨️","tags":["终端","Agent","自动化","CLI"],"rating":5,"review":"终端编程Agent最强选手，复杂重构一把好手","audience":"专业人士","pricing":"付费","function":5,"price":2,"ease":3,"ecosystem":3,"pros":["全代码库操作能力","复杂重构效率极高","命令行原生体验","支持自定义Agent"],"cons":["需要付费且价格较高","需要终端操作经验","无图形界面","门槛较高"]},
    {"name":"v0.dev","desc":"Vercel出品AI前端生成工具，截图/描述即可生成React组件","url":"https://v0.dev","category":"code","icon":"🔼","tags":["前端","UI","React","快速"],"rating":4,"review":"前端原型速度最快的工具，截图转代码很实用","audience":"所有人","pricing":"免费增值","function":4,"price":4,"ease":5,"ecosystem":4,"pros":["截图转代码功能实用","生成速度极快","适合快速原型","React/Tailwind天然支持"],"cons":["仅限前端UI","复杂逻辑无法生成","免费版限制较多","定制化能力有限"]},
    {"name":"Bolt.new","desc":"浏览器内全栈AI开发，写描述即可生成完整Web应用并一键部署","url":"https://bolt.new","category":"code","icon":"⚡","tags":["全栈","即时","Web","零配置"],"rating":4,"review":"产品原型验证的最佳工具，全栈开发零门槛","audience":"初学者","pricing":"免费增值","function":4,"price":4,"ease":5,"ecosystem":3,"pros":["零配置即刻开始","全栈应用一键生成","部署极其简单","适合快速验证想法"],"cons":["生成质量不够稳定","不适合大型项目","免费额度较少","定制灵活性受限"]},

    # Video
    {"name":"Sora","desc":"OpenAI文本/图片转视频模型，画质和物理一致性领先","url":"https://openai.com/sora","category":"video","icon":"🎬","tags":["文生视频","高画质","创意"],"rating":5,"review":"视频生成的技术天花板，物理世界理解最强","audience":"专业人士","pricing":"付费","function":5,"price":2,"ease":3,"ecosystem":3,"pros":["画质业界最高","物理一致性最好","多镜头切换流畅","运动轨迹自然"],"cons":["需要付费","目前仅限部分地区","生成速度较慢","可控性不够精细"]},
    {"name":"Runway","desc":"专业级AI视频编辑与生成平台，影视行业广泛使用","url":"https://runwayml.com","category":"video","icon":"🎥","tags":["编辑","特效","专业","影视"],"rating":4,"review":"影视专业人士的AI工具箱，功能最全面","audience":"专业人士","pricing":"付费","function":4,"price":2,"ease":3,"ecosystem":4,"pros":["功能最全面的AI视频平台","影视行业认可度高","工具链完整","教育版有优惠"],"cons":["价格偏高","学习曲线陡峭","生成质量有时不稳定","免费版功能极少"]},
    {"name":"Pika","desc":"轻量AI视频生成工具，界面简洁操作容易上手","url":"https://pika.art","category":"video","icon":"🦊","tags":["简单","快速","创意","入门"],"rating":4,"review":"最易上手的AI视频工具，适合快速创意验证","audience":"初学者","pricing":"免费增值","function":3,"price":4,"ease":5,"ecosystem":2,"pros":["操作最简单","上手极快","适合创意验证","界面友好"],"cons":["功能相对有限","高级效果不如Runway","视频长度有限制","免费版有水印"]},
    {"name":"HeyGen","desc":"AI数字人视频生成平台，口型同步自然，支持多语言","url":"https://www.heygen.com","category":"video","icon":"👤","tags":["数字人","口播","营销","多语言"],"rating":4,"review":"数字人播报效果最自然的平台","audience":"企业","pricing":"付费","function":4,"price":3,"ease":4,"ecosystem":3,"pros":["数字人口型最自然","多语言支持好","口播视频效率高","模板丰富"],"cons":["价格偏高","自定义程度有限","需要付费才能下载高清","免费版限制多"]},
    {"name":"CapCut","desc":"字节跳动旗下AI视频剪辑工具，AI字幕和模板功能强大","url":"https://www.capcut.com","category":"video","icon":"✂️","tags":["剪辑","字幕","模板","免费"],"rating":4,"review":"短视频创作者必备，AI字幕准确率极高","audience":"所有人","pricing":"免费","function":4,"price":5,"ease":5,"ecosystem":4,"pros":["完全免费","AI字幕准确率极高","模板海量","上手简单"],"cons":["有字节跳动品牌顾虑","高级调色功能弱","桌面版功能不如移动端","部分模板需付费"]},
    {"name":"Synthesia","desc":"企业级AI虚拟主播视频平台，支持140+语言和头像定制","url":"https://www.synthesia.io","category":"video","icon":"🎙️","tags":["虚拟人","企业","多语言","培训"],"rating":4,"review":"企业培训视频的最佳方案，省去拍摄成本","audience":"企业","pricing":"付费","function":4,"price":2,"ease":4,"ecosystem":3,"pros":["140+语言支持","企业培训场景最佳","省去拍摄成本","定制头像可用"],"cons":["企业级订阅价格高","免费功能几乎为零","头像自然度不如HeyGen","缺少创意功能"]},

    # Writing
    {"name":"Jasper","desc":"老牌AI营销文案平台，品牌声音定制和SEO优化功能成熟","url":"https://www.jasper.ai","category":"writing","icon":"✍️","tags":["营销","文案","品牌","SEO"],"rating":4,"review":"营销团队的AI写作主力，品牌调性保持最好","audience":"企业","pricing":"付费","function":4,"price":3,"ease":4,"ecosystem":3,"pros":["品牌声音定制出色","SEO优化功能成熟","团队协作功能好","模板丰富"],"cons":["价格偏高不适合个人","中文支持弱","免费试用期短","定位偏营销单一"]},
    {"name":"Notion AI","desc":"Notion内置AI写作助手，与知识库深度整合","url":"https://www.notion.so/product/ai","category":"writing","icon":"📋","tags":["笔记","知识库","协作","全能"],"rating":4,"review":"笔记+AI的完美结合，工作流最自然","audience":"所有人","pricing":"付费","function":4,"price":3,"ease":5,"ecosystem":5,"pros":["与Notion无缝集成","工作流最自然","知识库+AI完美结合","团队协作极佳"],"cons":["需付费使用","独立写作能力一般","中文质量中规中矩","不能独立使用"]},
    {"name":"Grammarly","desc":"全球最流行的AI英语语法纠正与润色工具，浏览器/桌面全覆盖","url":"https://www.grammarly.com","category":"writing","icon":"✅","tags":["语法","润色","英语","全平台"],"rating":5,"review":"英语写作刚需工具，几乎没有替代品","audience":"所有人","pricing":"免费增值","function":5,"price":4,"ease":5,"ecosystem":5,"pros":["语法纠正极其准确","全平台覆盖","润色建议质量高","免费版功能已够用"],"cons":["仅支持英语","高级功能需付费","不适合长篇创作","隐私方面有争议"]},
    {"name":"Perplexity","desc":"AI搜索引擎+写作助手，自动引用来源适合学术和研究","url":"https://www.perplexity.ai","category":"writing","icon":"🔎","tags":["搜索","引用","研究","实时"],"rating":4,"review":"AI搜索+写作的混合体，研究利器","audience":"专业人士","pricing":"免费增值","function":4,"price":4,"ease":4,"ecosystem":3,"pros":["自动引用来源","实时信息整合","适合学术研究","免费版已不错"],"cons":["长文撰写能力有限","中文资料搜索弱","Pro订阅偏贵","不支持离线使用"]},
    {"name":"QuillBot","desc":"专业AI改写润色工具，支持多种改写模式和摘要生成","url":"https://quillbot.com","category":"writing","icon":"🔄","tags":["改写","摘要","学术","多模式"],"rating":4,"review":"学术论文改写的最佳工具，降重效果好","audience":"专业人士","pricing":"免费增值","function":4,"price":4,"ease":5,"ecosystem":3,"pros":["论文降重效果极佳","多种改写模式","摘要生成好用","操作简单"],"cons":["免费版有字数限制","仅限英语","长文处理能力弱","改写质量有波动"]},
    {"name":"腾讯混元写作","desc":"腾讯AI写作助手，中文场景优化，办公文档和翻译出色","url":"https://hunyuan.tencent.com","category":"writing","icon":"🐧","tags":["中文","办公","翻译","免费"],"rating":3,"review":"国内免费中文写作工具的稳健选择","audience":"所有人","pricing":"免费","function":3,"price":5,"ease":3,"ecosystem":3,"pros":["免费使用","中文场景优化好","办公文档支持","腾讯生态集成"],"cons":["功能相对基础","创意写作能力弱","界面不够现代","知名度低"]},

    # Audio
    {"name":"Suno","desc":"AI音乐生成器，输入歌词和风格即可一键生成完整歌曲","url":"https://suno.ai","category":"audio","icon":"🎵","tags":["音乐","作曲","歌词","创作"],"rating":5,"review":"AI音乐生成的现象级产品，作曲质量惊人","audience":"所有人","pricing":"免费增值","function":5,"price":4,"ease":5,"ecosystem":4,"pros":["作曲质量惊人","上手极其简单","风格覆盖广","每日免费额度"],"cons":["高级功能需付费","歌词质量不稳定","无法精细控制编曲","版权归属尚不明确"]},
    {"name":"ElevenLabs","desc":"顶级AI语音合成与声音克隆平台，29种语言支持","url":"https://elevenlabs.io","category":"audio","icon":"🗣️","tags":["语音","克隆","多语言","自然"],"rating":5,"review":"语音合成的天花板，声音克隆效果以假乱真","audience":"专业人士","pricing":"免费增值","function":5,"price":4,"ease":4,"ecosystem":4,"pros":["语音合成业界最佳","声音克隆效果惊人","29种语言支持","API集成方便"],"cons":["免费版有字符限制","中文语音不够自然","高级克隆需付费","道德使用需要关注"]},
    {"name":"Murf","desc":"专业AI配音旁白工具，适合课程录制和有声内容制作","url":"https://murf.ai","category":"audio","icon":"🎤","tags":["配音","旁白","课程","专业"],"rating":4,"review":"课程和视频配音的专业工具，音色库丰富","audience":"专业人士","pricing":"付费","function":4,"price":3,"ease":4,"ecosystem":3,"pros":["音色库丰富","专业配音场景优化","支持背景音乐","时间轴编辑方便"],"cons":["免费版功能极少","价格不低","中文音色偏少","社区相对较小"]},
    {"name":"Descript","desc":"像编辑文档一样编辑音频/视频，AI转录和去口癖功能实用","url":"https://www.descript.com","category":"audio","icon":"📝","tags":["编辑","转录","播客","AI"],"rating":4,"review":"播客创作者的秘密武器，编辑效率提升10倍","audience":"专业人士","pricing":"付费","function":4,"price":3,"ease":5,"ecosystem":3,"pros":["编辑体验革命性","AI去口癖功能实用","转录准确率高","播客工作流最佳"],"cons":["价格偏高","对中文支持有限","需要一定学习","免费版限制多"]},
    {"name":"Audiobox","desc":"Meta出品的AI音效与语音生成研究项目，音效生成能力强","url":"https://audiobox.metademolab.com","category":"audio","icon":"📻","tags":["音效","语音","Meta","免费"],"rating":3,"review":"音效生成的免费好工具，Meta出品质量有保证","audience":"所有人","pricing":"免费","function":3,"price":5,"ease":3,"ecosystem":2,"pros":["完全免费","音效生成有特色","Meta出品有保障","研究项目持续更新"],"cons":["功能有限","尚在研究阶段","生成质量不够稳定","缺少商业支持"]},
    {"name":"剪映音频","desc":"字节跳动AI配音与音频编辑，中文配音效果自然","url":"https://www.capcut.com","category":"audio","icon":"🎧","tags":["配音","剪辑","中文","免费"],"rating":4,"review":"国内短视频创作者最常用的配音工具","audience":"所有人","pricing":"免费","function":4,"price":5,"ease":5,"ecosystem":4,"pros":["免费使用","中文配音最自然","与剪映无缝集成","操作简单"],"cons":["国际版功能不同","音色数量有限","高级音频编辑弱","字节品牌顾虑"]},

    # Office
    {"name":"Gamma","desc":"AI演示文稿与文档一键生成，设计感强，效率远超PPT","url":"https://gamma.app","category":"office","icon":"📊","tags":["PPT","文档","演示","设计"],"rating":5,"review":"做演示文稿效率最高的AI工具，设计无需手动调整","audience":"所有人","pricing":"免费增值","function":5,"price":4,"ease":5,"ecosystem":3,"pros":["演示文稿效率最高","设计审美在线","支持多种格式","实时协作"],"cons":["免费版有限制","不支持PPT导入","自定义空间小","离线无法使用"]},
    {"name":"Microsoft Copilot","desc":"Office全家桶内置AI助手，Word/Excel/PPT/Outlook全覆盖","url":"https://copilot.microsoft.com","category":"office","icon":"🪟","tags":["Office","办公","集成","企业"],"rating":4,"review":"Office用户的最佳选择，无缝集成生态","audience":"企业","pricing":"付费","function":4,"price":2,"ease":4,"ecosystem":5,"pros":["Office深度集成","企业级安全保障","Excel数据AI分析强","Teams协同好"],"cons":["价格偏高需订阅","个人版功能弱","部分功能还在完善","需要Office 365"]},
    {"name":"Notion","desc":"AI增强的知识管理与团队协作平台，灵活度极高","url":"https://www.notion.so","category":"office","icon":"📋","tags":["协作","知识库","AI","灵活"],"rating":5,"review":"知识管理领域无可争议的第一名","audience":"所有人","pricing":"免费增值","function":5,"price":4,"ease":4,"ecosystem":5,"pros":["知识管理最强","灵活度极高","模板社区活跃","免费版已够用"],"cons":["学习曲线存在","离线功能弱","AI功能需额外付费","中文搜索有提升空间"]},
    {"name":"Beautiful.ai","desc":"AI智能排版演示文稿，自动调整设计布局","url":"https://www.beautiful.ai","category":"office","icon":"✨","tags":["排版","智能","企业","设计"],"rating":4,"review":"追求设计感的商业PPT首选，排版自动优化","audience":"企业","pricing":"付费","function":4,"price":3,"ease":5,"ecosystem":2,"pros":["自动排版极智能","设计审美出色","品牌统一管理","导出格式多"],"cons":["免费功能极其有限","模板数量不如Gamma","价格偏高","协作功能弱"]},
    {"name":"Tome","desc":"AI驱动叙事型演示文稿，适合讲故事和产品演示","url":"https://tome.app","category":"office","icon":"📖","tags":["故事","演示","产品","交互"],"rating":4,"review":"产品演示和故事讲述的最佳PPT替代品","audience":"所有人","pricing":"免费增值","function":4,"price":4,"ease":5,"ecosystem":3,"pros":["叙事引导设计独特","交互体验极佳","产品演示场景最佳","上手快"],"cons":["适合场景偏窄","不如Gamma通用","免费版限制多","导出格式少"]},
    {"name":"飞书智能伙伴","desc":"飞书内置AI办公助手，覆盖会议纪要、文档协作、数据分析","url":"https://www.feishu.cn","category":"office","icon":"🐦","tags":["协作","会议","文档","中文"],"rating":4,"review":"国内团队协作AI功能的集大成者","audience":"企业","pricing":"免费增值","function":4,"price":4,"ease":4,"ecosystem":4,"pros":["团队协作AI集大成","会议纪要自动化好","中文体验最优","飞书生态深度集成"],"cons":["仅限飞书平台","非飞书用户无法使用","国际化弱","数据在字节跳动平台"]},

    # Platform
    {"name":"Hugging Face","desc":"全球最大AI模型社区，数十万开源模型和数据集","url":"https://huggingface.co","category":"platform","icon":"🤗","tags":["模型","开源","社区","数据"],"rating":5,"review":"AI开发者的GitHub，模型和数据集的首选平台","audience":"专业人士","pricing":"免费增值","function":5,"price":5,"ease":3,"ecosystem":5,"pros":["全球最大模型社区","开源模型极其丰富","免费托管使用","社区活跃文档齐全"],"cons":["需要编程基础","界面体验一般","服务器响应有时慢","企业版价格高"]},
    {"name":"Replicate","desc":"云端AI模型托管与API服务，一键部署开源模型","url":"https://replicate.com","category":"platform","icon":"🔄","tags":["API","部署","模型","云端"],"rating":4,"review":"开源模型部署到云的最快方式","audience":"专业人士","pricing":"付费","function":4,"price":3,"ease":4,"ecosystem":3,"pros":["一键部署开源模型","按量付费灵活","支持的模型多","API简单易用"],"cons":["使用成本可能高","冷启动较慢","免费额度少","依赖网络"]},
    {"name":"Dify","desc":"开源LLMOps平台，可视化搭建AI应用，支持RAG和Agent","url":"https://dify.ai","category":"platform","icon":"🔧","tags":["开源","编排","可视化","RAG"],"rating":5,"review":"搭建AI应用最友好的开源平台，功能全面","audience":"专业人士","pricing":"免费增值","function":5,"price":4,"ease":4,"ecosystem":4,"pros":["可视化编排友好","开源可自部署","RAG支持出色","社区版本功能齐全"],"cons":["企业版价格较高","文档有待完善","部署需要技术","海外知名度待提升"]},
    {"name":"Coze","desc":"字节跳动AI Bot搭建平台，零代码创建智能机器人","url":"https://www.coze.com","category":"platform","icon":"🤖","tags":["零代码","Bot","插件","字节"],"rating":4,"review":"零基础搭建AI Bot的最佳选择，插件生态丰富","audience":"初学者","pricing":"免费","function":4,"price":5,"ease":5,"ecosystem":4,"pros":["零代码零门槛","插件生态丰富","免费使用","多平台发布"],"cons":["高级功能有限","数据在字节跳动平台","定制化能力弱","仅限简单Bot"]},
    {"name":"LangChain","desc":"最流行的LLM应用开发框架，链式调用和Agent开发标准","url":"https://www.langchain.com","category":"platform","icon":"🦜","tags":["框架","开发","链式","标准"],"rating":4,"review":"LLM开发的事实标准框架，生态最成熟","audience":"专业人士","pricing":"免费","function":5,"price":5,"ease":2,"ecosystem":5,"pros":["LLM开发事实标准","生态最成熟","文档丰富","社区极其活跃"],"cons":["学习曲线陡峭","版本更新快不稳定","抽象层次多","简单场景可能过重"]},
    {"name":"Pinecone","desc":"企业级AI向量数据库，为RAG应用提供高性能向量检索","url":"https://www.pinecone.io","category":"platform","icon":"🌲","tags":["向量","检索","RAG","企业"],"rating":4,"review":"向量数据库的行业标杆，性能和稳定性最佳","audience":"企业","pricing":"付费","function":4,"price":2,"ease":4,"ecosystem":3,"pros":["性能和稳定性业界标杆","运维零负担","扩展性好","企业级支持"],"cons":["价格较高","免费版限制多","替代品越来越多","供应商锁定风险"]},
]

# Pricing class mapping
PRICING_CLASS = {"免费":"tag-free","付费":"tag-paid","免费增值":"tag-freemium"}

# Article data for cross-linking
ARTICLES = [
    {"id":"chatgpt-vs-claude-vs-gemini","title":"ChatGPT vs Claude vs Gemini 2026全面对比：三大AI助手谁更强","type":"comparison"},
    {"id":"deepseek-vs-chatgpt","title":"DeepSeek vs ChatGPT：国产大模型能替代吗？2026深度对比","type":"comparison"},
    {"id":"kimi-vs-tongyi","title":"Kimi vs 通义千问：国产长文本大模型对决 2026","type":"comparison"},
    {"id":"midjourney-vs-dalle-vs-sd","title":"Midjourney vs DALLE 3 vs Stable Diffusion：AI绘画工具横评 2026","type":"comparison"},
    {"id":"github-copilot-vs-cursor-vs-windsurf","title":"GitHub Copilot vs Cursor vs Windsurf：AI编程工具选哪个 2026","type":"comparison"},
    {"id":"sora-vs-runway-vs-pika","title":"Sora vs Runway vs Pika：AI视频生成哪家强 2026","type":"comparison"},
    {"id":"suno-vs-elevenlabs","title":"Suno vs ElevenLabs：AI音频创作工具对比 2026","type":"comparison"},
    {"id":"gamma-vs-beautiful-vs-tome","title":"Gamma vs Beautiful.ai vs Tome：AI PPT工具横评 2026","type":"comparison"},
    {"id":"claude-code-vs-cursor","title":"Claude Code vs Cursor vs Copilot：开发者AI助手深度对比 2026","type":"comparison"},
    {"id":"perplexity-vs-chatgpt-search","title":"Perplexity vs ChatGPT Search：AI搜索引擎对比 2026","type":"comparison"},
    {"id":"leonardo-vs-midjourney","title":"Leonardo.AI vs Midjourney：游戏设计AI工具对比 2026","type":"comparison"},
    {"id":"heygen-vs-synthesia","title":"HeyGen vs Synthesia：AI数字人平台对比 2026","type":"comparison"},
    {"id":"best-ai-coding-tools","title":"程序员必备的10款AI编程工具 2026：从代码补全到全栈开发","type":"recommendation"},
    {"id":"best-ai-image-tools","title":"设计师必备AI绘画工具Top 10 2026：从专业创作到一键出图","type":"recommendation"},
    {"id":"student-ai-tools-free","title":"学生党免费AI工具推荐 2026：覆盖学习和生活的AI工具箱","type":"recommendation"},
    {"id":"ai-side-hustle-tools","title":"如何用AI工具做副业赚钱？2026年普通人也能上手的6条路径","type":"recommendation"},
    {"id":"deepseek-complete-guide","title":"DeepSeek完全使用指南 2026：从注册到高级技巧","type":"recommendation"},
    {"id":"chatgpt-prompt-guide","title":"ChatGPT提示词技巧大全 2026：普通人也能写出好Prompt","type":"recommendation"},
    {"id":"ai-cli-tools-setup-guide","title":"AI 命令行工具安装指南：Claude Code / Codex / Gemini CLI 上手教程 2026","type":"guide"},
]


def star_html(rating):
    return ''.join('★' if i < rating else '☆' for i in range(5))


def pricing_tag(p):
    cls = PRICING_CLASS.get(p, '')
    return f'<span class="tag {cls}">{p}</span>'


def tool_slug(name):
    """生成工具的文件名slug"""
    import re
    # 中文名到slug的手动映射
    slug_map = {
        '通义千问': 'tongyi',
        '腾讯混元写作': 'hunyuan-writing',
        '剪映音频': 'capcut-audio',
        '飞书智能伙伴': 'feishu',
    }
    if name in slug_map:
        return slug_map[name]

    s = name.lower().strip()
    s = s.replace('·', '-').replace(' ', '-')
    s = re.sub(r'[^a-z0-9-]', '', s)
    s = re.sub(r'-+', '-', s)
    return s


def gen_tool_page(tool, all_tools, cats):
    """生成单个工具详情页"""
    cat = next((c for c in cats if c['id'] == tool['category']), None)
    cat_tools = [t for t in all_tools if t['category'] == tool['category']]
    alt_tools = [t for t in cat_tools if t['name'] != tool['name']][:3]

    # 相关文章（基于分类关键词匹配）
    related_articles = []
    cat_names = {tool['name'].lower(), cat['name'] if cat else ''}
    for a in ARTICLES:
        if len(related_articles) >= 3:
            break
        title_lower = a['title'].lower()
        if tool['name'].lower() in title_lower or (cat and cat['name'] in title_lower):
            related_articles.append(a)

    title = f"{tool['name']} — 评测、评分、优缺点 | AI ToolNav"
    desc = f"{tool['name']}：{tool['review']}。查看{cat['name'] + ' ' if cat else ''}{tool['name']}的功能评分、优缺点、价格对比和替代工具推荐。"

    pros_html = ''.join(f'<li>{p}</li>' for p in tool.get('pros', []))
    cons_html = ''.join(f'<li>{c}</li>' for c in tool.get('cons', []))
    tags_html = pricing_tag(tool['pricing']) + ''.join(f'<span class="tag">{tg}</span>' for tg in tool['tags'])
    stars = star_html(tool['rating'])

    alt_html = ''
    for alt in alt_tools:
        slug = tool_slug(alt['name'])
        alt_html += f'<a href="/tools/{slug}.html" class="alt-card"><div class="alt-name">{alt["icon"]} {alt["name"]}</div><div class="alt-desc">{alt["desc"][:50]}...</div></a>'

    rel_art_html = ''
    for a in related_articles:
        rel_art_html += f'<li style="margin-bottom:6px;"><a href="/articles/{a["id"]}.html" style="color:var(--accent-start);font-size:13px;text-decoration:none;">{a["title"]}</a></li>'

    func, prc, ease, eco = tool.get('function', 4), tool.get('price', 3), tool.get('ease', 4), tool.get('ecosystem', 3)
    robots = robots_for_tool(tool)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{common_head_snippets()}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{tool['name']},{cat['kw'] if cat else ''}">
<link rel="stylesheet" href="/css/style.css">
<link rel="canonical" href="{DOMAIN}/tools/{tool_slug(tool['name'])}.html">
<meta name="robots" content="{robots}">
</head>
<body class="no-splash">
<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">AI ToolNav</a>
    <nav class="nav">
      <a href="/">首页</a>
      <a href="/categories/llm.html">大模型</a>
      <a href="/categories/image.html">AI绘画</a>
      <a href="/categories/code.html">AI编程</a>
      <a href="/articles/">文章</a>
      <a href="/tools/">在线工具</a>
    </nav>
  </div>
</header>

<main class="main">
  <a href="/categories/{tool['category']}.html" class="back-btn">← {cat['name'] if cat else '返回'}分类</a>

  <div class="detail-header animate-fade-in">
    <div class="detail-icon">{tool['icon']}</div>
    <div class="detail-info">
      <h1>{tool['name']} <span style="color:var(--star-color);font-size:18px;">{stars}</span></h1>
      <div class="detail-desc">{tool['desc']}</div>
      <div class="detail-review">💬 {tool['review']}</div>
      <div class="rank-tags" style="margin-bottom:12px;">{tags_html}</div>
      <a href="{tool['url']}" target="_blank" rel="noopener" class="detail-cta">访问官网 →</a>
      <button class="collect-btn" onclick="toggleCollect('{tool['name']}')" id="collectBtn">☆ 收藏</button>
    </div>
  </div>

  <!-- 四维评分 -->
  <section class="glass-card" style="padding:24px;margin-bottom:24px;">
    <h4 style="margin-bottom:16px;font-size:15px;">📊 四维评分</h4>
    <div class="rating-bars">
      <div class="rating-bar-item">
        <div class="rating-bar-label"><span>功能性</span><span>{func}/5</span></div>
        <div class="rating-bar-track"><div class="rating-bar-fill" style="width:{func*20}%"></div></div>
      </div>
      <div class="rating-bar-item">
        <div class="rating-bar-label"><span>价格</span><span>{prc}/5</span></div>
        <div class="rating-bar-track"><div class="rating-bar-fill" style="width:{prc*20}%;background:linear-gradient(to right,#34d399,#10b981)"></div></div>
      </div>
      <div class="rating-bar-item">
        <div class="rating-bar-label"><span>易用性</span><span>{ease}/5</span></div>
        <div class="rating-bar-track"><div class="rating-bar-fill" style="width:{ease*20}%;background:linear-gradient(to right,#fbbf24,#f59e0b)"></div></div>
      </div>
      <div class="rating-bar-item">
        <div class="rating-bar-label"><span>生态</span><span>{eco}/5</span></div>
        <div class="rating-bar-track"><div class="rating-bar-fill" style="width:{eco*20}%;background:linear-gradient(to right,#a78bfa,#818cf8)"></div></div>
      </div>
    </div>
  </section>

  <!-- 优缺点 -->
  <div class="pros-cons">
    <div class="pros"><h4>👍 优点</h4><ul>{pros_html}</ul></div>
    <div class="cons"><h4>👎 缺点</h4><ul>{cons_html}</ul></div>
  </div>

  <!-- 基本信息 -->
  <div class="glass-card" style="padding:20px;margin-bottom:24px;">
    <p style="font-size:13px;color:var(--text-secondary);margin-bottom:6px;">🏷 价格：<strong style="color:var(--text-primary);">{tool['pricing']}</strong></p>
    <p style="font-size:13px;color:var(--text-secondary);margin-bottom:6px;">🎯 适合：<strong style="color:var(--text-primary);">{tool['audience']}</strong></p>
    <p style="font-size:13px;color:var(--text-secondary);">🔗 官网：<a href="{tool['url']}" target="_blank" rel="noopener" style="color:var(--accent-start);">{tool['url']}</a></p>
  </div>

  <!-- 替代工具 -->
  {f'''<section class="section">
    <div class="section-title">🔄 替代工具推荐</div>
    <div class="section-subtitle">同分类的其他优秀选择</div>
    <div class="alt-grid">{alt_html}</div>
  </section>''' if alt_html else ''}

  <!-- 相关文章 -->
  {f'''<section class="section">
    <div class="section-title">📋 相关评测文章</div>
    <ul style="list-style:none;">{rel_art_html}</ul>
  </section>''' if rel_art_html else ''}
</main>

<footer class="footer">
  <p>© 2026 AI ToolNav · <a href="/privacy.html">隐私政策</a> | <a href="/terms.html">服务条款</a> | <a href="/about.html">关于我们</a> · 每日更新</p>
</footer>

<script>
function toggleCollect(name) {{
  var key = 'collected_tools';
  var collected = JSON.parse(localStorage.getItem(key) || '[]');
  var idx = collected.indexOf(name);
  var btn = document.getElementById('collectBtn');
  if (idx === -1) {{
    collected.push(name);
    btn.textContent = '★ 已收藏';
    btn.classList.add('collected');
  }} else {{
    collected.splice(idx, 1);
    btn.textContent = '☆ 收藏';
    btn.classList.remove('collected');
  }}
  localStorage.setItem(key, JSON.stringify(collected));
}}
(function(){{
  var collected = JSON.parse(localStorage.getItem('collected_tools') || '[]');
  if (collected.indexOf('{tool['name']}') !== -1) {{
    var btn = document.getElementById('collectBtn');
    if (btn) {{ btn.textContent = '★ 已收藏'; btn.classList.add('collected'); }}
  }}
}})();
</script>
</body>
</html>'''


def gen_category_page(cat, tools, all_tools):
    """生成分类页"""
    cat_tools = sorted([t for t in tools if t['category'] == cat['id']], key=lambda t: -t['rating'])
    top5 = cat_tools[:5]

    title = f"{cat['name']}工具推荐 | {cat['name']}排行对比 2026 — AI ToolNav"
    desc = f"{cat['desc']}"

    # Ranking list
    ranking = ''
    ranks = ['gold', 'silver', 'bronze', '', '']
    for i, t in enumerate(top5):
        slug = tool_slug(t['name'])
        tags_html = pricing_tag(t['pricing']) + ''.join(f'<span class="tag">{tg}</span>' for tg in t['tags'])
        ranking += f'''<a href="/tools/{slug}.html" class="ranking-item">
          <div class="rank-num {ranks[i] if i < 3 else ''}">{i+1}</div>
          <span class="rank-icon">{t['icon']}</span>
          <div class="rank-info">
            <div class="rank-name">{t['name']}</div>
            <div class="rank-desc">{t['desc']}</div>
            <div class="rank-review">💬 {t['review']}</div>
            <div class="rank-tags">{tags_html}</div>
          </div>
          <div class="rank-stars">{star_html(t['rating'])}</div>
          <div class="rank-audience">适合<br>{t['audience']}</div>
        </a>'''

    # Comparison table
    table = ''
    for t in cat_tools:
        slug = tool_slug(t['name'])
        table += f'''<tr>
          <td class="td-name"><a href="/tools/{slug}.html" style="color:inherit;text-decoration:none;">{t['icon']} {t['name']}</a></td>
          <td>{star_html(t['rating'])}</td>
          <td>{pricing_tag(t['pricing'])}</td>
          <td>{t['audience']}</td>
          <td style="font-size:12px;color:var(--text-secondary);">💬 {t['review']}</td>
        </tr>'''

    # More tools grid
    more_grid = ''
    for t in cat_tools[5:]:
        slug = tool_slug(t['name'])
        tags_html = pricing_tag(t['pricing']) + ''.join(f'<span class="tag">{tg}</span>' for tg in t['tags'])
        more_grid += f'<a href="/tools/{slug}.html" class="tool-card"><span class="icon">{t["icon"]}</span><div class="name">{t["name"]}</div><div class="desc">{t["desc"]}</div><div class="tags">{tags_html}</div></a>'

    # Related articles
    rel_arts = ''
    cat_name_lower = cat['name'].lower()
    for a in ARTICLES:
        if cat_name_lower in a['title'].lower() or any(kw in a['title'].lower() for kw in cat['kw'].split()):
            if len(rel_arts.split('</li>')) < 6:
                rel_arts += f'<li style="margin-bottom:6px;"><a href="/articles/{a["id"]}.html" style="color:var(--accent-start);font-size:13px;text-decoration:none;">{a["title"]}</a></li>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{common_head_snippets()}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{cat['kw']}">
<link rel="stylesheet" href="/css/style.css">
<link rel="canonical" href="{DOMAIN}/categories/{cat['id']}.html">
<meta name="robots" content="noindex, follow">
</head>
<body class="no-splash">
<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">AI ToolNav</a>
    <nav class="nav">
      <a href="/">首页</a>
      <a href="/categories/llm.html">大模型</a>
      <a href="/categories/image.html">AI绘画</a>
      <a href="/categories/code.html">AI编程</a>
      <a href="/articles/">文章</a>
      <a href="/tools/">在线工具</a>
    </nav>
  </div>
</header>

<main class="main">
  <a href="/" class="back-btn">← 返回首页</a>

  <div class="cat-info glass-card" style="padding:24px;margin-bottom:24px;">
    <h2 style="font-size:24px;font-weight:700;margin-bottom:6px;">{cat['icon']} {cat['name']}工具推荐</h2>
    <p style="font-size:13px;color:var(--text-secondary);line-height:1.6;">{desc}</p>
  </div>

  <!-- Top 5 -->
  <section class="section">
    <div class="section-title">🏆 {cat['name']} Top 5 排行榜</div>
    <div class="section-subtitle">评分最高的5款工具，按综合评分排序</div>
    <div class="ranking-list">{ranking}</div>
  </section>

  <!-- Comparison Table -->
  <section class="section">
    <div class="section-title">📊 {cat['name']}横向对比表</div>
    <div class="section-subtitle">一键对比，帮你做出最佳选择</div>
    <div style="overflow-x:auto;">
      <table class="compare-table">
        <thead><tr><th>工具</th><th>评分</th><th>价格</th><th>适合人群</th><th>点评</th></tr></thead>
        <tbody>{table}</tbody>
      </table>
    </div>
  </section>

  <!-- More tools -->
  {f'''<section class="section">
    <div class="section-title">📋 更多{cat['name']}</div>
    <div class="card-grid">{more_grid}</div>
  </section>''' if more_grid else ''}

  <!-- Related articles -->
  {f'''<section class="section">
    <div class="section-title">📝 相关文章</div>
    <ul style="list-style:none;">{rel_arts}</ul>
  </section>''' if rel_arts else ''}
</main>

<footer class="footer">
  <p>© 2026 AI ToolNav · <a href="/privacy.html">隐私政策</a> | <a href="/terms.html">服务条款</a> | <a href="/about.html">关于我们</a> · 每日更新</p>
</footer>
</body>
</html>'''


def gen_tools_index(tools, cats):
    """生成工具列表页 /tools/index.html"""
    ranked = sorted(tools, key=lambda t: -t['rating'])

    ranking = ''
    ranks_cls = ['gold', 'silver', 'bronze']
    for i, t in enumerate(ranked[:20]):
        slug = tool_slug(t['name'])
        tags_html = pricing_tag(t['pricing']) + ''.join(f'<span class="tag">{tg}</span>' for tg in t['tags'])
        rc = ranks_cls[i] if i < 3 else ''
        ranking += f'''<a href="/tools/{slug}.html" class="ranking-item">
          <div class="rank-num {rc}">{i+1}</div>
          <span class="rank-icon">{t['icon']}</span>
          <div class="rank-info">
            <div class="rank-name">{t['name']}</div>
            <div class="rank-desc">{t['desc']}</div>
            <div class="rank-tags">{tags_html}</div>
          </div>
          <div class="rank-stars">{star_html(t['rating'])}</div>
          <div class="rank-audience">适合<br>{t['audience']}</div>
        </a>'''

    # Grid for remaining tools
    grid = ''
    for t in ranked[20:]:
        slug = tool_slug(t['name'])
        tags_html = pricing_tag(t['pricing']) + ''.join(f'<span class="tag">{tg}</span>' for tg in t['tags'])
        grid += f'<a href="/tools/{slug}.html" class="tool-card"><span class="icon">{t["icon"]}</span><div class="name">{t["name"]} {star_html(t["rating"])}</div><div class="desc">{t["desc"]}</div><div class="tags">{tags_html}</div></a>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{common_head_snippets()}
<title>AI工具排行榜 | 完整评分与对比 — AI ToolNav</title>
<meta name="description" content="完整AI工具排行榜，收录48款精选AI工具，包含评分、价格、适用人群和详细点评。支持按分类筛选和横向对比。">
<meta name="keywords" content="AI工具排行榜,AI工具排名,AI工具评分,最好用的AI工具">
<link rel="stylesheet" href="/css/style.css">
<link rel="canonical" href="{DOMAIN}/tools/">
<meta name="robots" content="noindex, follow">
</head>
<body class="no-splash">
<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">AI ToolNav</a>
    <nav class="nav">
      <a href="/">首页</a>
      <a href="/categories/llm.html">大模型</a>
      <a href="/categories/image.html">AI绘画</a>
      <a href="/categories/code.html">AI编程</a>
      <a href="/articles/">文章</a>
      <a href="/tools/">在线工具</a>
    </nav>
  </div>
</header>

<main class="main">
  <a href="/" class="back-btn">← 返回首页</a>
  <div class="hero-headline">
    <h2 class="gradient-heading">完整 AI 工具排行榜</h2>
    <p>48 款精选工具，综合评分排序</p>
  </div>

  <section class="section">
    <div class="section-title">🏆 综合排名</div>
    <div class="ranking-list">{ranking}</div>
  </section>

  {f'''<section class="section">
    <div class="section-title">📋 更多工具</div>
    <div class="card-grid">{grid}</div>
  </section>''' if grid else ''}
</main>

<footer class="footer">
  <p>© 2026 AI ToolNav · <a href="/privacy.html">隐私政策</a> | <a href="/terms.html">服务条款</a> | <a href="/about.html">关于我们</a> · 每日更新</p>
</footer>
</body>
</html>'''


# ===== 主流程 =====
if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    count = 0

    # 生成工具详情页
    for tool in TOOLS:
        slug = tool_slug(tool['name'])
        html = gen_tool_page(tool, TOOLS, CATEGORIES)
        path = os.path.join(TOOLS_DIR, f'{slug}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f'  ✅ {slug}.html')

    print(f'\n📦 已生成 {count} 个工具详情页')

    # 生成分类页
    cc = 0
    for cat in CATEGORIES:
        html = gen_category_page(cat, TOOLS, TOOLS)
        path = os.path.join(CATS_DIR, f'{cat["id"]}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        cc += 1
        print(f'  ✅ categories/{cat["id"]}.html')

    print(f'\n📁 已生成 {cc} 个分类页')

    # 生成工具列表页
    html = gen_tools_index(TOOLS, CATEGORIES)
    with open(os.path.join(TOOLS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ tools/index.html')

    print(f'\n🎉 全部完成！共生成 {count + cc + 1} 个页面')
