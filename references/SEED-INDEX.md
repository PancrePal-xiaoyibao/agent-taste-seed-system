# 🗂️ 种子全景索引（等距平铺 · 全员同等可见）· 审美种子大脑

> **这是什么**：全库种子的**等距平铺目录**——每粒一行、同等曝光、没有「首选 / 备选」的层级差。
> **为什么不用旧的「按需查询」**：人工索引表只有 10~12 行，结构性地让 95% 的种子永远没入口。
> **怎么用**：机器选 → `python3 scripts/seed_brain.py match "<任务描述>"`（IDF 加权 top-K）；
> 人/LLM 通读 → 本文件全文，按信号词自行判断归属。
> **排序**：按层、层内按 ID 字典序——**刻意不按重要性**，杜绝任何隐含优先级。
> **规模**：374 粒 ｜ 风格章档 352 ｜ 代码基因卡 12 ｜ 情绪档 10
> **🌱 增量区**：带 🌱 的条目来自 `references/seed-additions.jsonl`（agent 运行时用 `seed_brain.py add` 写入）。
> 它们与源库种子**同权参与匹配**，不因「新」而优先，也不因「未回填源文件」而低一等。

---

## 情绪档（10 粒）

目录：[`moods/`](moods/)

| id | 名称 | 一句话 |
|---|---|---|
| `md-01-科技酷感` | 科技酷感 | 科技产品长图、发布会 KV、赛博题材插画、数据可视化暗色版、技术类 PPT、开发者工具官网。 |
| `md-02-梦幻治愈` | 梦幻治愈 | 生活类长图、公益/心理健康内容、儿童与亲子、治愈系游戏 UI、欢迎页、贺卡。 |
| `md-03-热血冲击` | 热血冲击 | 赛事/活动 KV、招新海报、战斗类游戏宣传、口号型长图、动员页。 |
| `md-04-庄重典雅` | ️ 庄重典雅 | 周年庆/纪念内容、官方年报封面、机构介绍、婚礼与典礼、历史文化题材、高端品牌页。 |
| `md-05-甜美容爱` | 甜美容爱 | 婚恋/交友产品、甜品与花店、少女向游戏、节日贺卡、宠物内容、母婴。 |
| `md-06-孤独诗意` | ️ 孤独诗意 | 文艺长文配图、音乐/诗歌内容、深夜电台、独立产品官网、告别与纪念。 |
| `md-07-荒诞幽默` | 🃏 荒诞幽默 | 社交传播图、愚人节/整活内容、播客封面、亚文化品牌、吐槽长图。 |
| `md-08-暗黑崇高` | 暗黑崇高 | 史诗题材、恐怖游戏宣传、重金属/暗黑音乐、历史创伤叙事、万圣节企划。 |
| `md-09-清晰理性` | 清晰理性 | 数据报告、SaaS 官网、B 端产品、技术文档配图、仪表盘、信息长图。 |
| `md-10-东方古韵` | 东方古韵 | 国风游戏、茶/酒/中药材品牌、传统节日企划、汉服与文创、诗词内容。 |

## 代码基因卡（12 粒）

目录：[`code-genes/`](code-genes/)

| id | 名称 | 一句话 |
|---|---|---|
| `cg-01-瑞士平面` | 瑞士平面 / 包豪斯 | 报告长图、SaaS 官网、B 端 dashboard、技术文档、信息图表 |
| `cg-02-赛博霓虹` | 赛博霓虹 | 暗色 dashboard、科技产品长图、开发者工具官网、游戏 HUD |
| `cg-03-中国画留白` | 中国画留白（绢色·气口·印章） | 文化内容长图、茶叶/酒/中药材页、诗词内容、国风品牌官网 |
| `cg-04-极简主义` | 极简主义（留白即豪华） | 高端产品页、作品集、发布页 hero、品牌声明页、摄影展示 |
| `cg-05-吉卜力手绘亲和` | 吉卜力手绘亲和 | 亲子/教育产品、公益内容、生活方式长图、儿童活动页、疗愈系工具 |
| `cg-06-浮世绘扁平` | 浮世绘扁平（木版画 UI） | 文化活动页、日料/和风品牌、创意海报式长图、专题封面 |
| `cg-07-巴洛克聚光` | 巴洛克聚光（Tenebrism 暗底 hero） | 发布会/大片感 hero 区、人物故事页、纪录片风格长图、奢侈品页 |
| `cg-08-洛可可粉彩` | 洛可可粉彩 | 婚庆/婚恋页、甜品花店、少女向活动、节日礼盒页、母婴 |
| `cg-09-波普拼贴` | 波普拼贴 | 潮流品牌页、活动宣传、社交传播图、音乐/娱乐内容、整活企划 |
| `cg-10-构成主义海报` | 构成主义海报 | 活动 KV、招聘/招募页、宣言式长图、运动赛事、社会议题传播 |
| `cg-11-赛璐璐动漫ui` | 赛璐璐动漫 UI | 二次元产品/游戏 UI、角色主站长图、虚拟主播页、动漫社区 |
| `cg-12-哥特暗黑` | 哥特暗黑 | 恐怖/悬疑游戏页、万圣节企划、暗黑音乐内容、史诗叙事长图 |

## 风格章档（352 粒）

目录：[`art-seeds.md`](art-seeds.md)

| id | 名称 | 一句话 |
|---|---|---|
| `ch-001-村上ゆき` | 村上ゆき | 轻盈梦幻、清透用色、温柔眼神 |
| `ch-a-geng` | 阿梗 A Geng | 《踮脚张望》：清新文艺水彩晕染 |
| `ch-agnes-martin` | 马丁 Agnes Martin | 浅底上手绘细线网格几乎不可见，需安静凝视；不冷的、充满精神性 |
| `ch-ai-weiwei` | 艾未未 Ai Weiwei | 一亿颗陶瓷葵花籽、汉白玉鸽子：人权自由体制探讨 |
| `ch-ai-yazawa` | 矢泽爱 Ai Yazawa | 极致时尚：纤细高挑精心搭配（Westwood系），漫画×时尚插画，冷艳 |
| `ch-aivazovsky` | 艾瓦佐夫斯基 Aivazovsky | 史上海景最伟大者之一：暴风巨浪与月光海面，水光空气无伦掌控 |
| `ch-akatsuka` | 赤冢不二夫 Akatsuka | 搞笑漫画开创：《天才傻瓜》节奏与荒唐幽默影响全行业 |
| `ch-albers` | 阿尔伯斯 Albers | 《向正方形致敬》：同一色块在不同背景下看起来完全不同 |
| `ch-albrecht-d` | 丢勒 Albrecht Dürer | 德国文艺复兴巨人，版画线条极精细，自画像深刻心理刻画 |
| `ch-allen-jones` | 艾伦·琼斯 Allen Jones | SM 家具雕塑的强争议强冲击 |
| `ch-anno` | 庵野秀明 Anno | 机甲重点在驾驶员心理创伤；极端个人化、实验抽象 |
| `ch-ansel-adams` | 亚当斯 Ansel Adams | 约塞米蒂黑白大画幅，「区域曝光法」，每细节灰度层次 |
| `ch-araki` | 荒木经惟 Araki | 花、情色捆缚、妻子临终：一切指向生与死 |
| `ch-araki-2` | 荒木飞吕彦 Araki | 独一无二美学：筋肉猛男、JOJO立、时尚设计，画风独特演化 |
| `ch-artemisia-gentileschi` | 真蒂莱斯基 Artemisia Gentileschi | 最著名巴洛克女画家，强烈戏剧性与暴力倾向，力量与勇气 |
| `ch-ask` | ASK | 华丽色彩装饰时尚的和洋融合 |
| `ch-atey-ghailan` | Atey Ghailan | 瑞典概念：细腻光影氛围，速写色彩练习教科书 |
| `ch-august-macke` | 马克 August Macke | 优雅明亮色彩、光敏感处理，同样阵亡于一战 |
| `ch-azuma-aya` | あずまあや Azuma Aya | 温暖治愈手绘质感、布纹肌理 |
| `ch-bacon` | 培根 Bacon | 刷子抹布撕扯：尖叫教皇、瘫软肉体、存在恐惧的封闭空间 |
| `ch-bada-shanren` | 八大山人 Bada Shanren | 明宗室遗民僧：鱼鸟皆翻白眼，倔强孤傲亡国之痛，极简极有力 |
| `ch-baldessari` | 巴尔代萨里 Baldessari | 脸上贴彩点、莫名句子；让你笑，然后让你想 |
| `ch-balla` | 巴拉 Balla | 《拴着皮带的狗》多重交叠的连续运动研究 |
| `ch-basquiat` | 巴斯奎特 Basquiat | 涂鸦文字皇冠骷髅，种族权力历史批判，自由粗暴才华横溢 |
| `ch-beardsley` | 比亚兹莱 Beardsley | 英年早逝的天才插画：极致黑白、诡异意象、情色暗示的不安之美 |
| `ch-benjamin-west` | 韦斯特 Benjamin West | 开创当代服装绘历史画，皇家美院院长 |
| `ch-bernini` | 贝尼尼 Bernini | 大理石有生命：衣能飘动、皮肤有温度、情感瞬间爆发 |
| `ch-beuys` | 博伊斯 Beuys | 毛毡脂肪蜂蜜的「有温度」材料；「人人都是艺术家」 |
| `ch-bill-viola` | 维奥拉 Bill Viola | 溺水挣扎/火焰之人/雨夜告别如文艺复兴祭坛画般庄严 |
| `ch-boccioni` | 薄邱尼 Boccioni | 《空间中连续的独特形式》：城市力量速度运动的动态感，一战阵亡 |
| `ch-bones` | 骨头社 Bones | 热血战斗：《钢炼》《E7》《我的英雄》，流畅战斗+独特运镜 |
| `ch-bonnard` | 博纳尔 Bonnard | 亲密色彩：室内花园沐浴在奇异美丽的色彩中，如打翻的调色盘 |
| `ch-boucher` | 布歇 Boucher | 蓬巴杜夫人最爱：粉红裸体、柔软绸缎、鲜花花园的享乐极致 |
| `ch-braque` | 布拉克 Braque | 与毕加索并肩但更温和：肌理材料实验、静物、 muted 调 |
| `ch-brauner` | 布劳纳 Brauner | 古埃及印第安图腾巫术符号的神秘预言 |
| `ch-bronzino` | 布龙齐诺 Bronzino | 美第奇宫廷，冷峻优雅、疏离表情、大理石般冷感 |
| `ch-buddy` | Buddy 蛤蟆 | 《侍灵演武》：日漫流畅×中国古典韵味 |
| `ch-cai-guo-qiang` | 蔡国强 Cai Guo-Qiang | 火药爆破绘画与烟火装置（2008北京奥运脚印） |
| `ch-caillebotte` | 卡耶博特 Caillebotte | 摄影式视角的现代巴黎，俯视/裁切/透视缩短的大胆构图 |
| `ch-canova` | 卡诺瓦 Canova | 温柔光泽大理石，《丘比特与普塞克》神话爱意凝于温柔瞬间 |
| `ch-caravaggio` | 卡拉瓦乔 Caravaggio | 舞台追光般 Tenebrism，街头模特粗粝真实，人间苦难与热情 |
| `ch-carl-andr` | 安德烈 Carl André | 整齐排列的金属方板让观众踩上去，否定雕塑基座 |
| `ch-carr` | 卡拉 Carrà | 从未来主义转向与基里科共创空寂神秘 |
| `ch-carrington` | 卡林顿 Carrington | 移居墨西哥：凯尔特神话炼金术意象、反复的马，比男性超现实者更温和神秘 |
| `ch-cartier-bresson` | 布列松 Cartier-Bresson | 新闻摄影之父：事件自动构成完美几何的瞬间 |
| `ch-chen-yifei` | 陈逸飞 Chen Yifei | 江南水乡古典仕女：电影镜头般抒情唯美 |
| `ch-cindy-sherman` | 舍曼 Cindy Sherman | 自扮明星/历史/童话/小丑：身份是否只是文化面具？ |
| `ch-clamp` | CLAMP | 全女性团体：极纤细人物、复杂华丽服饰、藤蔓线条 |
| `ch-claude-monet` | 莫奈 Claude Monet | 印象派得名于《日出·印象》；干草堆/鲁昂大教堂/睡莲系列捕捉光线时刻变化，晚年睡莲近乎色彩交响乐 |
| `ch-clyfford-still` | 斯蒂尔 Clyfford Still | 刮刀厚涂、参差裂缝透出下层光的原始崇高 |
| `ch-constable` | 康斯特布尔 Constable | 英格兰乡村：滚动云彩、翠绿田野，云彩研究极深，影响巴比松 |
| `ch-copley` | 科普利 Copley | 独立时期最重要：革命一代的坚毅气质，《沃森与鲨鱼》里程碑 |
| `ch-courbet` | 库尔贝 Courbet | 「没见过天使所以不画」，《画室》《奥尔南葬礼》巨幅描绘普通人世界 |
| `ch-dal` | 达利 Dalí | 照片级精确的不可能场景：融化时钟、拉长大象；「偏执批判法」 |
| `ch-dan-flavin` | 弗莱文 Dan Flavin | 只用市售荧光灯管：光即雕塑，空间被色彩重新定义 |
| `ch-daubigny` | 杜比尼 Daubigny | 奥维尔河畔风景，直接影响莫奈 |
| `ch-daumier` | 杜米埃 Daumier | 「纸上的米开朗基罗」，石版画捕捉19世纪巴黎百态 |
| `ch-de-chirico` | 基里科 de Chirico | 空无一人意大利广场、拉长阴影、火车雕像组合，直接影响超现实主义 |
| `ch-de-kooning` | 德·库宁 de Kooning | 暴力大笔触×具象的撕扯：《女性》既是赞颂也是涂改 |
| `ch-degas` | 德加 Degas | 不在意外光、专注运动形体：芭蕾舞女标志题材，日本版画式意外裁切视角 |
| `ch-delacroix` | 德拉克洛瓦 Delacroix | 浪漫主义灵魂：《自由引导人民》，崇尚色彩、激情运动笔触、深刻色彩理论家 |
| `ch-delaunay` | 德劳内 Delaunay | 彩色圆盘的同时性对比，绘画中的音乐节奏 |
| `ch-delvaux` | 德尔沃 Delvaux | 古典建筑街道上的裸女与远处火车，梦境与死亡之间的静止 |
| `ch-derain` | 德兰 Derain | 纯红蓝橙画风景，完全不考虑自然色，纯粹为表现 |
| `ch-diane-arbus` | 阿勃丝 Diane Arbus | 侏儒巨人双胞胎变装者：不安却无法移开视线 |
| `ch-donald-judd` | 贾德 Donald Judd | 黄铜胶合板有机玻璃盒子等距上墙；「一个盒子就是它自己」 |
| `ch-dorothea-lange` | 兰格 Dorothea Lange | 《移民母亲》：一张脸诉说时代所有苦难 |
| `ch-duchamp` | 杜尚 Duchamp | 小便池签名《泉》、给蒙娜丽莎画胡子，彻底颠覆「什么是艺术」；「艺术就是我在做的事」 |
| `ch-dufy` | 杜菲 Dufy | 赛马海滨音乐厅永远阳光愉悦，介于野兽派与装饰艺术之间 |
| `ch-eakins` | 伊肯斯 Eakins | 痴迷解剖运动研究，《格罗斯诊所》外科手术般科学精确 |
| `ch-ed-ruscha` | 鲁沙 Ed Ruscha | LA 加油站停车场：冷静客观的公路文化 |
| `ch-eggleston` | 埃格尔斯顿 Eggleston | 彩色摄影先驱：饱和色彩让南方平凡变神秘；「世界是有颜色的」 |
| `ch-egon-schiele` | 席勒 Egon Schiele | 克林姆特弟子但更激进：骨瘦扭曲人体、毫不掩饰的欲望与死亡 |
| `ch-el-greco` | 埃尔·格列柯 El Greco | 扭曲拉长人体、阴森蓝绿色调、燃烧天空，无法归类的神秘主义 |
| `ch-el-lissitzky` | 利西茨基 El Lissitzky | 至上主义×设计感：二维三维间动态过渡，海报排版影响极深 |
| `ch-eliasson` | 埃利亚松 Eliasson | 泰特涡轮大厅造太阳、展厅造瀑布彩虹，环保关切 |
| `ch-ellsworth-kelly` | 凯利 Ellsworth Kelly | 鲜明单色简单形状：叶子的曲线、帽子的影子 |
| `ch-ensor` | 恩索尔 Ensor | 骷髅面具狂欢，明亮刺目色彩，直接影响表现主义 |
| `ch-fan-kuan` | 范宽 Fan Kuan | 《溪山行旅图》北宋巅峰：巨山占三分之二，人驮渺小；「对景造意」雨点皴 |
| `ch-fang-lijun` | 方力钧 Fang Lijun | 打哈欠光头水中挣扎：转型期的虚无迷惘 |
| `ch-fra-angelico` | 安杰利科 Fra Angelico | 修士画家，明亮柔和色彩、天堂般光感与宁静的虔诚 |
| `ch-fragonard` | 弗拉戈纳尔 Fragonard | 《秋千》洛可可精神完美代表，快速潇洒笔触、糖果甜美色 |
| `ch-frank-stella` | 斯特拉 Frank Stella | 「你看到什么就是什么」的黑色条纹；后期转色彩斑驳立体画布 |
| `ch-frankenthaler` | 弗兰肯塔勒 Frankenthaler | 发明 Soak-stain：稀释颜料倒入生画布渗透如水彩，影响整个色域派 |
| `ch-frans-hals` | 哈尔斯 Frans Hals | 快速率性笔触捕捉瞬间笑容，技法自由影响印象派 |
| `ch-franz-kline` | 克莱恩 Franz Kline | 巨型毛笔般的黑白笔触建筑震撼空间，如汉字书写 |
| `ch-franz-marc` | 马尔克 Franz Marc | 蓝马黄牛的色彩象征动物画，一战阵亡年仅36 |
| `ch-frida-kahlo` | 弗里达·卡罗 Frida Kahlo | 墨西哥最著名女画家：自画像充满痛苦坚韧与本土文化 |
| `ch-friedrich` | 弗里德里希 Friedrich | 德国浪漫主义标志：人于广袤自然前凝视（雾海漫游者），「崇高」 |
| `ch-fujiko-f-fujio` | 藤子·F·不二雄 Fujiko F. Fujio | 圆润可爱、想象力与温暖，国民级角色 |
| `ch-gainsborough` | 庚斯博罗 Gainsborough | 英国最杰出门类双修：优美风景背景、宽阔流畅笔触，《蓝衣少年》 |
| `ch-gaud` | 高迪 Gaudí | 圣家堂如骨头植物海水堆砌的有机体，色彩来自碎瓷马赛克 Trencadís |
| `ch-gauguin` | 高更 Gauguin | 逃离文明去塔希提：大片平涂色、强烈轮廓线的神秘装饰风格 |
| `ch-ger` | 莱热 Léger | 人物如金属管齿轮圆圈构成，影响后来的波普 |
| `ch-ghibli` | 吉卜力 Ghibli | 手绘极致：每帧背景如画册，自然景观（夏日绿、流水、云）是灵魂 |
| `ch-giorgione` | 乔尔乔内 Giorgione | 诗意风景与神秘主题，首创风景主题独立绘画 |
| `ch-giotto` | 乔托 Giotto | 突破拜占庭平面化，赋予人物立体感与情感表达，朴实叙事性与面部表情著称 |
| `ch-gottlieb` | 戈特利布 Gottlieb | 上方圆形发光体（天）与下方粗糙笔触（地）的对立统一 |
| `ch-goya` | 戈雅 Goya | 从宫廷优雅到最黑暗绘画：《1808年5月3日》战争控诉，「黑画」是表现主义预演 |
| `ch-gu-kaizhi` | 顾恺之 Gu Kaizhi | 最早可靠记载大师：《女史箴图》春蚕吐丝般细腻流畅线条 |
| `ch-guimard` | 吉马尔 Guimard | 翠绿铸铁曲线如植物茎干，新艺术建筑名片 |
| `ch-guo-xi` | 郭熙 Guo Xi | 理论大家：「三远法」（高深远平）；《早春图》云雾泉水春之苏醒 |
| `ch-gursky` | 古尔斯基 Gursky | 巨幅商业景观：交易所/货架/人潮；《莱茵河II》430万美元最贵照片 |
| `ch-gustave-moreau` | 莫罗 Gustave Moreau | 象征主义核心：神秘寓言、宝石色彩珠宝细节（马蒂斯之师） |
| `ch-hagio` | 萩尾望都 Hagio | 复杂叙事心理描写革新：诗意线条哥特氛围 |
| `ch-hamaji-aki` | はまじあき Hamaji Aki | 轻松可爱、简练线条、丰富夸张表情 |
| `ch-hamilton` | 汉密尔顿 Hamilton | 英国波普之父，第一件真正波普作品 |
| `ch-hans-arp` | 阿尔普 Hans Arp | 生物形态般自由流动的抽象形状，自动绘画早期实践者 |
| `ch-hans-hofmann` | 霍夫曼 Hans Hofmann | 连接欧洲现代主义与美国抽表：色彩空间张力的「推拉」 |
| `ch-hans-holbein` | 荷尔拜因 Hans Holbein | 亨利八世宫廷画家，冷静克制、细节精确，服装珠宝揭示身份心理 |
| `ch-harunobu` | 铃木春信 Harunobu | 发明多色印刷「锦绘」：纤细清秀美人的市井诗意 |
| `ch-hasegawa` | 长谷川町子 Hasegawa | 《海螺小姐》日本最长寿：温暖日常、战后家庭记录 |
| `ch-heckel` | 黑克尔 Heckel | 尖锐线条不安构图，后期转抒情 |
| `ch-hieronymus-bosch` | 博斯 Hieronymus Bosch | 500年前超现实：怪异生物、地狱折磨、荒诞混合体 |
| `ch-hiroshige` | 广重 Hiroshige | 《东海道五十三次》：雨雪月夜樱花的四季诗情，最擅长天气氛围 |
| `ch-hirst` | 赫斯特 Hirst | 福尔马林鲨鱼、钻石骷髅：把死亡推到观众面前 |
| `ch-hiten` | Hiten | 高度商业化高质量：柔美少女、细腻光影、通透色彩 |
| `ch-hockney` | 霍克尼 Hockney | 加州泳池：明快饱和、平面化空间、清澈水面，享乐主义赞歌；摄影拼贴+iPad画 |
| `ch-hogarth` | 贺加斯 Hogarth | 「道德漫画」组画《浪子生涯》《时髦婚姻》，辛辣讽刺18世纪英国 |
| `ch-hojo` | 北条司 Hojo | 精准写实：人物比例准确、服装枪械精细 |
| `ch-hokusai` | 北斋 Hokusai | 全球最著名日本艺术家：《神奈川冲浪里》人类文化史最知名图像之一；90岁仍求进步 |
| `ch-hosoda` | 细田守 Hosoda | 数码世界×家庭关系，表情细腻丰富 |
| `ch-hua-yecai` | 花噎菜 Hua Yecai | 质感极强赛璐璐：大胆用色、强光影对比 |
| `ch-huang-binhong` | 黄宾虹 Huang Binhong | 集大成者：反复积染「积墨法」，黑不可测却黑中透光 |
| `ch-huang-gongwang` | 黄公望 Huang Gongwang | 《富春山居图》最著名长卷之一：书法用笔入画，披麻皴江南温润 |
| `ch-ikeda` | 池田理代子 Ikeda | 法国大革命史诗：古典欧洲华丽×少女柔美 |
| `ch-ikuhara` | 几原邦彦 Ikuhara | 反复视觉符号（玫瑰剑钥匙）+舞台剧感：性别革命成长 |
| `ch-ingres` | 安格尔 Ingres | 线条绝对主义、瓷器般人体曲线，《大宫女》人为加长的脊柱成经典 |
| `ch-inoue` | 井上雄彦 Inoue | 少年漫与艺术漫自由穿梭：后期毛笔作画气韵生动 |
| `ch-ishinomori` | 石之森章太郎 Ishinomori | 最多产：《假面骑士》《009》，题材极广 |
| `ch-j-m-w-turner` | 透纳 J.M.W. Turner | 「光的画家」，后期几乎抽象：迷雾船只、燃烧议院，色彩光线溶解形体 |
| `ch-jacques-louis-david` | 大卫 Jacques-Louis David | 旗手+拿破仑首席：《贺拉斯兄弟的誓言》理性高于情感 |
| `ch-jacques-villon` | 维永 Jacques Villon | 精确分析立体主义+铜版/石版应用（杜尚之兄） |
| `ch-james-jean` | James Jean | 台湾裔：中世纪版画×浮世绘×工笔×当代，密纹样层叠花卉梦幻人物 |
| `ch-jan-steen` | 扬·斯蒂恩 Jan Steen | 混乱欢乐家庭场景，幽默与道德寓意 |
| `ch-jan-van-eyck` | 凡·艾克 Jan van Eyck | 细节精细到每根毛发、镜面般光影反射，《阿尔诺芬尼夫妇像》 |
| `ch-jasper-johns` | 琼斯 Jasper Johns | 画「已知图像」：国旗数字地图，从日常意义剥离重审绘画 |
| `ch-jeff-wall` | 杰夫·沃尔 Jeff Wall | 精心「导演」的场景如电影剧照：绘画构图×当代瞬间 |
| `ch-jeremy-mann` | Jeremy Mann | 加州：大幅雨夜城市，湿街霓虹倒影，刮刀抹布融合抽象具象 |
| `ch-juan-gris` | 格里斯 Juan Gris | 第三核心：理性数学化、建筑师般严格建构 |
| `ch-kandinsky` | 康定斯基 Kandinsky | 公认第一位抽象画家：色彩形状直接触动灵魂如音乐 |
| `ch-kaori-yuki` | 由贵香织里 Kaori Yuki | 天使禁猎区：华丽堕落天使、逆十字、羽毛翅膀，繁复阴郁 |
| `ch-kapoor` | 卡普尔 Kapoor | 芝加哥「豆子」；物质色彩（买断Vantablack）、负空间与无限 |
| `ch-kara-walker` | 沃克 Kara Walker | 优雅黑白剪影讲奴隶制残酷：形式与内容的反差之力 |
| `ch-kees-van-dongen` | 凡·东根 Kees van Dongen | 漫画般大眼猩红嘴唇的巴黎时尚女性 |
| `ch-keith-haring` | 哈林 Keith Haring | 地铁起步：空心轮廓婴儿/跳舞人/吠狗，简单而充满能量 |
| `ch-khnopff` | 赫诺普夫 Khnopff | 神秘疏离、冰冷的斯芬克斯之美 |
| `ch-kiefer` | 基弗 Kiefer | 德国战后最震撼：废墟稻草铅灰烬，每幅画都是文明遗址 |
| `ch-kim-hyung-tae` | 金亨泰 Kim Hyung-tae | 「油腻师姐」：夸张身材+极精细盔甲服装纹理 |
| `ch-kirchner` | 基希纳 Kirchner | 尖锐角度、不自然色彩、神经质线条的柏林街头 |
| `ch-kishida` | 岸田メル Kishida | 《蓝海少女》《炼金工房》：淡雅蓝白色调、懒洋洋的可爱 |
| `ch-kishimoto` | 岸本齐史 Kishimoto | 流畅凌厉：精彩战斗分镜，忍者文化×现代审美 |
| `ch-klimt` | 克林姆特 Klimt | 金箔装饰+情色主题：《吻》融合拜占庭马赛克、日本版画、新艺术 |
| `ch-koons` | 昆斯 Koons | 不锈钢打磨如镜面气球：气球狗兔子，可爱到极致也空洞到极致 |
| `ch-kosuth` | 科苏斯 Kosuth | 真椅子+照片+字典定义并置：艺术是其中哪个？ |
| `ch-kruger` | 克鲁格 Kruger | 黑白照片+红底白字标语：「你的凝视击中了我的脸」 |
| `ch-kunichika` | 国周 Kunichika | 色彩浓烈构图大胆，浮世绘黄昏最后辉煌 |
| `ch-kuniyoshi` | 国芳 Kuniyoshi | 武士妖怪猫：动态夸张近漫画，影响日本动漫 |
| `ch-kurumada` | 车田正美 Kurumada | 华丽铠甲设计+动态对战 |
| `ch-kusama` | 草间弥生 Kusama | 波点+无限镜屋：把强迫症转化为创造源泉 |
| `ch-kyoani` | 京阿尼 KyoAni | 极致稳定：自然动作、柔和光影、日常细节偏执 |
| `ch-leonardo-da-vinci` | 达·芬奇 Leonardo da Vinci | Sfumato 雾状透视让色彩轮廓如烟雾融合，《蒙娜丽莎》《最后的晚餐》；解剖、光影、空气透视全通 |
| `ch-li-sixun` | 李思训 Li Sixun | 金碧辉煌青绿山水：精细浓艳，唐代宫廷审美 |
| `ch-li-tang` | 李唐 Li Tang | 全景转边角转折人物：苍劲「斧劈皴」，《万壑松风图》 |
| `ch-lichtenstein` | 利希滕斯坦 Lichtenstein | 本戴点放大+大胆黑线轮廓，既是漫画放大也是解构 |
| `ch-lin-fengmian` | 林风眠 Lin Fengmian | 现代艺术先驱：中国画线条×马蒂斯莫迪利亚尼造型，含蓄优美 |
| `ch-liu-ye` | 刘野 Liu Ye | 卡通人物×蒙德里安几何背景：童话与寂寞之间 |
| `ch-loish` | Loish | 荷兰：流畅线条舞蹈般动感、鲜艳和谐、自然健康女体 |
| `ch-loundraw` | Loundraw | 「最会用光影的新生代」：极致透明感，《夏日幽灵》导演 |
| `ch-lu-mingshan` | 鹿溟山 Lu Mingshan | 山海经古风：古典×奇幻、艳丽色彩丰富细节 |
| `ch-lucian-freud` | 弗洛伊德 Lucian Freud | 厚油堆叠皮肤每寸纹理重量，不美化任何人 |
| `ch-luo-zhongli` | 罗中立 Luo Zhongli | 巨幅陕北老农肖像，中国当代艺术史最重要作品之一 |
| `ch-ma-yuan` | 马远 Ma Yuan | 「一角半边」构图：只画角落山水，大片留白遐想 |
| `ch-madhouse` | MADHOUSE | 《死亡笔记》《一拳超人》《寄生兽》：风格跨度极大但水准高超 |
| `ch-magritte` | 马格利特 Magritte | 安静得不安：圆顶礼帽人、遮脸苹果、「这不是一只烟斗」；图像文字能否代表真实？ |
| `ch-malevich` | 马列维奇 Malevich | 《黑方块》：白底黑方，一切艺术最纯粹的本质 |
| `ch-man-ray` | 曼·雷 Man Ray | 发明「雷摄影」Rayograph：无相机物影曝光，如梦似幻 |
| `ch-manet` | 马奈 Manet | 现实主义→印象派：《奥林匹亚》平坦色块、简化阴影引发争议 |
| `ch-mappa` | MAPPA | 增长最快：《巨人最终季》《咒术回战》《电锯人》，高质量高速快节奏 |
| `ch-mary-cassatt` | 卡萨特 Mary Cassatt | 旅法美国女画家：母与子亲密，日本风装饰版画 |
| `ch-masaccio` | 马萨乔 Masaccio | 首次系统运用线性透视，强烈立体感与现实主义倾向 |
| `ch-masson` | 马松 Masson | 笔无意识游走，潜意识图像浮现后赋形 |
| `ch-matisse` | 马蒂斯 Matisse | 20世纪最伟大色彩大师：纯色平涂、极简轮廓，「平衡纯净宁静」如安乐椅，剪纸是晚年巅峰 |
| `ch-max-ernst` | 恩斯特 Max Ernst | 发明 Frottage 摩拓法：拓印纹理中寻找图像，最多产实验者 |
| `ch-mi-er` | 米二 Mi Er | 道家民俗×热血少年：从粗糙到精细，分镜想象力 |
| `ch-michelangelo` | 米开朗基罗 Michelangelo | 西斯廷天顶画巅峰，戏剧性扭动姿态、惊人肌肉解剖，《大卫》完美人体 |
| `ch-millet` | 米勒 Millet | 《拾穗者》《晚祷》：贫穷却纪念碑般尊严，土地的赞歌 |
| `ch-mir` | 米罗 Miró | 像儿童涂鸦的黑点线彩色几何，但每笔高度提炼 |
| `ch-miuchi` | 美内铃惠 Miuchi | 细腻心理+舞台剧表现 |
| `ch-miyazaki` | 宫崎骏 Miyazaki | 飞翔天空、茂密森林、勇敢少女、复杂反派；细腻手绘+壮观飞行+自然细节+美食作画 |
| `ch-mizuki` | 水木茂 Mizuki | 《鬼太郎》：失左臂画出妖怪百科全书，朴拙亲切 |
| `ch-mo-fei` | 墨飞 Mo Fei | 硬朗画风、强节奏战斗、神怪×现代 |
| `ch-moholy-nagy` | 莫霍利-纳吉 Moholy-Nagy | 包豪斯核心：光空间调节器动态雕塑、物影照片 |
| `ch-mondrian` | 蒙德里安 Mondrian | 自然简化为黑网格线+红黄蓝+白灰，极端简化的惊人平衡 |
| `ch-morisot` | 莫里索 Morisot | 核心圈最重要女画家：梳妆少女、摇篮母亲的私密瞬间，笔触极轻盈 |
| `ch-moriyama` | 森山大道 Moriyama | 「粗粒·晃动·失焦」：东京最黑暗角落，城市是粗粝体验 |
| `ch-moronobu` | 菱川师宣 Moronobu | 确立浮世绘基本形式：黑轮廓+手绘填色 |
| `ch-morris-louis` | 莫里斯·路易斯 Morris Louis | 「面纱画」：倾斜倾倒丙烯的透明色彩瀑布 |
| `ch-motherwell` | 马瑟韦尔 Motherwell | 最具文学气质：《西班牙共和国挽歌》黑椭圆与直线的深沉悼念 |
| `ch-mucha` | 穆夏 Mucha | 辨识度最高：高贵女性+流动秀发+花卉藤蔓+圆形光环 |
| `ch-munch` | 蒙克 Munch | 《呐喊》20世纪标志图像，现代存在焦虑；生命死亡爱嫉妒的基本经验 |
| `ch-murakami` | 村上隆 Murakami | Superflat 理论：浮世绘平面×动漫语言，微笑太阳花、Mr.DOB |
| `ch-nam-june-paik` | 白南准 Nam June Paik | 电视机器人、TV Buddha、电视墙：电视从消费品变艺术媒介 |
| `ch-nan-goldin` | 戈尔丁 Nan Goldin | 快照记录亲友的吸毒恋爱暴力艾滋：《性依赖的叙事曲》私摄影圣经 |
| `ch-naoko-yamada` | 山田尚子 Naoko Yamada | 脚的动作、手指颤动、背景光线传情绪 |
| `ch-nara` | 奈良美智 Nara | 可爱但眼神带匕首的叛逆小孩，简洁有力全球共鸣 |
| `ch-nauman` | 瑙曼 Nauman | 霓虹文字、录像、全息、声音装置、行为：探索身体语言空间边界 |
| `ch-neco` | neco | 机械军武少女：柔美×硬核军事细节 |
| `ch-newman` | 纽曼 Newman | 只剩一种元素：大面积单色中的垂直细线（ZIP），《拜异教者》色域巅峰 |
| `ch-ni-zan` | 倪瓒 Ni Zan | 最「淡」的画家：枯树空亭远山，最少笔墨最多孤独清高 |
| `ch-noland` | 诺兰 Noland | 靶心系列与 V 字形：简单几何探索色彩相互作用 |
| `ch-nolde` | 诺尔德 Nolde | 最狂野色彩：燃烧般花卉水景、原始力量宗教画 |
| `ch-oda` | 尾田荣一郎 Oda | 恣意豪放：夸张表情、无约束线条、窒息密分镜 |
| `ch-odore-rousseau` | 卢梭 Théodore Rousseau | 枫丹白露森林写生，自然真实感受 |
| `ch-ofili` | 奥菲利 Ofili | 树脂画+圆点+大象粪便：非洲传统×西方艺术史 |
| `ch-old` | old先 Xian Old | 条漫领军：简洁时尚、帅气人物、温暖日常 |
| `ch-oldenburg` | 奥登伯格 Oldenburg | 超大日常物软雕塑：巨大汉堡、软塌厕所，熟悉变陌生幽默可爱 |
| `ch-on-kawara` | 河原温 On Kawara | 半世纪《今天系列》：每天画当天日期，未完成即销毁；时间存在的终极观念 |
| `ch-oshii` | 押井守 Oshii | 阴暗哲学化、慢节奏高思想密度，影响《黑客帝国》 |
| `ch-otomo` | 大友克洋 Otomo | 定义80年代视觉密度：精细到变态的机械城市、厚重阴影、写实破坏 |
| `ch-pan-tianshou` | 潘天寿 Pan Tianshou | 指墨画：构图极有张力，巨石老松秃鹫霸悍 |
| `ch-paolo-uccello` | 乌切洛 Paolo Uccello | 痴迷透视数学之美，《圣罗马诺之战》极致透视缩短 |
| `ch-paperblue` | PAPERBLUE | 蓝紫调空灵治愈 |
| `ch-parmigianino` | 帕尔米贾尼诺 Parmigianino | 《长颈圣母》：拉长颈部、超大手指、不合理空间，奇异而优雅 |
| `ch-paul-klee` | 保罗·克利 Paul Klee | 最富童心的画家：儿童画×原始符号×音乐手稿；「使不可见成为可见」 |
| `ch-peter-blake` | 布莱克 Peter Blake | 披头士《佩珀军士》专辑封面：名人纸偶拼贴 |
| `ch-picabia` | 毕卡比亚 Picabia | 机器肖像画与透明重叠绘画 |
| `ch-picasso` | 毕加索 Picasso | 《亚威农少女》开启立体主义；分析→综合立体主义，多变风格贯穿整个世纪 |
| `ch-pieter-bruegel` | 勃鲁盖尔 Pieter Bruegel | 农民生活与自然景观，寓言意味、宏大场景、百科全书式细节 |
| `ch-pissarro` | 毕沙罗 Pissarro | 最年长、唯一全勤8次展览，朴实温暖风景+蒙马特大道都市系列 |
| `ch-pistachio` | ピスタチオ Pistachio | 粉嫩可爱甜品色 |
| `ch-pollock` | 波洛克 Pollock | 画布铺地、倾倒颜料：空前复杂的全覆盖构图，捕捉宇宙能量 |
| `ch-popova` | 波波娃 Popova | 女性先锋：从立体主义到纯抽象构成，后转向纺织舞台设计 |
| `ch-production-i-g` | Production I.G | 高质量作画+战斗：《攻壳SAC》《排球少年》，流畅写实分镜严谨 |
| `ch-puvis-de-chavannes` | 沙瓦纳 Puvis de Chavannes | 粉笔般苍白柔和、古典静止感的梦幻仪式 |
| `ch-qi-baishi` | 齐白石 Qi Baishi | 木匠转画家：虾蟹小鸡牵牛花勃勃生机；「妙在似与不似之间」 |
| `ch-qiu-ying` | 仇英 Qiu Ying | 唯一非文人职业画家：青绿山水精细无比、华丽不俗 |
| `ch-raphael` | 拉斐尔 Raphael | 完美和谐，《雅典学院》透视构图杰作，圣母温柔优美 |
| `ch-rauschenberg` | 劳森伯格 Rauschenberg | 「Combine」打破绘画雕塑界限：轮胎山羊标本报纸上画布，当代艺术催化剂 |
| `ch-redon` | 雷东 Redon | 早期黑白炭笔梦境生物，后期神秘花卉，视觉化潜意识 |
| `ch-rei` | 老累 REI | 珠宝质感的厚涂少女：高饱和璀璨通透 |
| `ch-rella` | Rella | 透明感、柔和光影、梦幻配色，初音视觉图 |
| `ch-rembrandt` | 伦勃朗 Rembrandt | 用光穿透灵魂，金色黑暗中捕捉人性；自画像是史上最坦诚的自我记录 |
| `ch-renoir` | 雷诺阿 Renoir | 画「快乐」：年轻女性、孩子、阳光下人群，羽毛般笔触、阳光般色彩，《煎饼磨坊的舞会》 |
| `ch-repin` | 列宾 Repin | 俄国最伟大现实主义：《伏尔加河上的纤夫》，宏大场面+深刻内心 |
| `ch-ricault` | 热里科 Géricault | 《美杜莎之筏》真实海难、巨幅扭曲人体传达绝境抗争，开启浪漫主义 |
| `ch-richard-prince` | 普林斯 Richard Prince | 再摄影牛仔广告封面女郎：质疑原创与商品崇拜 |
| `ch-richter` | 里希特 Richter | 「当代毕加索」：照片模糊绘画×刮刀抽象×色表，拒绝任何标签 |
| `ch-robert-capa` | 卡帕 Robert Capa | 「照片不够好是靠得不够近」：西班牙内战、诺曼底 |
| `ch-robert-frank` | 弗兰克 Robert Frank | 《美国人》：随意不完美构图里的疏离孤独，改写纪实美学 |
| `ch-robert-morris` | 罗伯特·莫里斯 Robert Morris | 灰色胶合板几何体：抛弃个人触感的物理空间关系 |
| `ch-rodchenko` | 罗德琴科 Rodchenko | 画家转摄影：激进俯视斜角、蒙太奇海报至今充满力量 |
| `ch-rosenquist` | 罗森奎斯特 Rosenquist | 广告牌油漆工出身：跑车面条人脸的超现实拼接 |
| `ch-ross-tran` | Ross Tran | 好莱坞式强逆光高对比闪耀，饱和强气场 |
| `ch-rothko` | 罗斯科 Rothko | 模糊边界悬浮矩形色块；不让你「看懂」而让你「感受」，巨幅前的色彩包裹 |
| `ch-rozanova` | 罗扎诺娃 Rozanova | 明亮色彩自主形式的「色彩至上主义」 |
| `ch-rubens` | 鲁本斯 Rubens | 华丽极致：动感人群、丰腴裸体、饱满色彩、奢华装饰，产量惊人 |
| `ch-ruisdael` | 雷斯达尔 Ruisdael | 荷兰黄金时代风景最伟大者：低垂云层、崇高戏剧感、人生短暂之叹 |
| `ch-russolo` | 鲁索洛 Russolo | 发明噪音机器、《噪音的艺术》预言电子音乐 |
| `ch-sai` | 晓斋 Kyōsai | 酒后笔走龙蛇：讽刺妖怪极富动感幽默 |
| `ch-sakimi-chan` | Sakimi Chan | 加拿大：日式美少女×美式写实渲染的超精细 |
| `ch-sandro-botticelli` | 波提切利 Sandro Botticelli | 神话主题《春》《维纳斯的诞生》，优雅忧郁、线条流畅飘逸、柔和唯美 |
| `ch-satoshi-kon` | 今敏 Satoshi Kon | 梦境/现实无缝转换+惊人剪辑：《千年女优》《红辣椒》 |
| `ch-schwitters` | 施维特斯 Schwitters | 街头垃圾废票报纸的「Merz」拼贴，影响装置艺术 |
| `ch-seurat` | 修拉 Seurat | 科学点彩：纯色小点按光学原理混合，《大碗岛的星期天下午》 |
| `ch-severini` | 塞韦里尼 Severini | 未来派中最敏感色彩：《塔巴林舞女》闪烁夜总会灯光 |
| `ch-shaft` | SHAFT | 45度歪头、极简背景、文字飞过、非现实色彩，辨识度极高 |
| `ch-shan-ze` | 杉泽 Shan Ze | 《观山海》：精细线条+古典色彩重演山海经 |
| `ch-sharaku` | 写乐 Sharaku | 仅活跃10个月消失：极度夸张变形的役者肖像如现代漫画 |
| `ch-shen-zhou` | 沈周 Shen Zhou | 宽厚温润，诗文书画俱佳的文人典范 |
| `ch-shi-tao` | 石涛 Shi Tao | 「法自我立」反泥古：一笔成画的革命理论 |
| `ch-shima` | 大岛弓子 Ōshima | 梦幻纤细柔美 |
| `ch-shinkai` | 新海诚 Shinkai | 每帧壁纸：云光雨城市夜景新干线；推动数字超写实背景美学 |
| `ch-shunsh` | 胜川春章 Shunshō | 歌舞伎演员的动态瞬间与个性表情 |
| `ch-sisley` | 西斯莱 Sisley | 最纯粹印象风景：四季河流、桥梁、雪景 |
| `ch-sol-lewitt` | 勒维特 Sol LeWitt | 文字说明规定画什么由助手执行；「概念比成品更重要」 |
| `ch-stephen-shore` | 肖尔 Stephen Shore | 大画幅记录汽车旅馆加油站快餐：普通街景的画作庄严 |
| `ch-sugimoto` | 杉本博司 Sugimoto | 《海景》极简海平面永恒冥想；《剧院》整部长曝把银幕变发光体 |
| `ch-takahashi` | 高桥留美子 Takahashi | 最成功女漫画家：温馨搞笑→战国奇幻，妖怪浪漫 |
| `ch-takahata` | 高畑勋 Takahata | 《萤火虫》战争控诉；《辉夜姬》水墨简笔；写实、日常质感 |
| `ch-takaya` | 高屋奈月 Takaya | 清爽温暖：柔和线条生动表情，治愈不回避伤痛 |
| `ch-takei` | 武井宏之 Takei | 神道教泛灵论×时尚漫画 |
| `ch-takemiya` | 竹宫惠子 Takemiya | 《奔向地球》：科幻成长性别议题入少女漫 |
| `ch-takeoka` | 竹冈美穗 Takeoka | 《文学少女》：文艺怀旧水彩淡彩 |
| `ch-takeuchi` | 武内直子 Takeuchi | 魔法少女融合战斗：高缇耶式时装设计、宝石色彩，定义90年代少女漫视觉 |
| `ch-tan-jiu` | 坛九 Tan Jiu | 高质量黑白+优秀分镜，线条流畅表情生动 |
| `ch-tanemura` | 种村有菜 Tanemura | 闪亮大眼、繁复花边、华丽特效 |
| `ch-tang-yin` | 唐寅 Tang Yin | 卖画为生：仕女山水皆潇洒超脱 |
| `ch-tanguy` | 唐吉 Tanguy | 荒凉空旷沙地上的骨状有机体、遥远地平线长影 |
| `ch-tatlin` | 塔特林 Tatlin | 《第三国际纪念塔》螺旋钢铁革命象征；艺术为社会服务 |
| `ch-tetsuo-hara` | 原哲夫 Tetsuo Hara | 钢筋般人体、力与暴力的美感 |
| `ch-tezuka` | 手冢治虫 Tezuka | 「电影式漫画」：分镜变焦特写让漫画动起来；圆润大眼（迪士尼系）、夸张表情、流畅动作 |
| `ch-thiebaud` | 第伯 Thiebaud | 蛋糕馅饼圣代：柔和绚烂色彩、厚涂如真实奶油 |
| `ch-tiepolo` | 提埃波罗 Tiepolo | 洛可可最伟大天顶画家：浩瀚蓝天、人物漂浮的透视错觉 |
| `ch-tintoretto` | 丁托列托 Tintoretto | 巨幅+戏剧明暗，对角线构图、电影感角度，预示巴洛克 |
| `ch-tite-kubo` | 久保带人 Tite Kubo | 「时髦值」：泼墨跨页、空灵诗意台词、潇洒构图 |
| `ch-titian` | 提香 Titian | 威尼斯灵魂，「色彩之王」，深刻肖像，晚年自由笔触影响巴洛克与印象派 |
| `ch-toei` | 东映动画 Toei | 最老牌：龙珠海贼王美少女，「省钱但好看」的长跑技巧 |
| `ch-toriyama` | 鸟山明 Toriyama | 干净利落线条：衣褶肌肉简化到极致却充满力量，战斗分镜天才 |
| `ch-toulouse-lautrec` | 劳特累克 Toulouse-Lautrec | 红磨坊夜生活：尖锐线条大胆色彩，海报极具现代感 |
| `ch-tracey-emin` | 艾敏 Tracey Emin | 《我的床》：混乱私生活直接搬进画廊 |
| `ch-trigger` | Trigger | 脑洞工作室：撞色、夸张变形透视、闪亮钻头、大声呐喊 |
| `ch-troyon` | 特鲁瓦永 Troyon | 动物画：牛羊田园 |
| `ch-tsunako` | つなこ Tsunako | 《海王星》人设：明亮色彩华丽服装 |
| `ch-turrell` | 特瑞尔 Turrell | 改造火山口为光天文台；Ganzfeld 让人沉浸色彩失去方向 |
| `ch-ufotable` | ufotable | 摄影后期特效：CG×传统达到电影效果，水光火光惊叹 |
| `ch-umezu` | 楳图一雄 Umezu | 《漂流教室》：扭曲表情+密集线条的心理压迫 |
| `ch-umino` | 羽海野千花 Umino | 水彩般柔和：表情微妙真实的青春 |
| `ch-utamaro` | 歌麿 Utamaro | 「大首绘」特写：微妙表情内心世界，线条纤细优雅 |
| `ch-uzaki` | 宇崎拓也 Uzaki | 动感肌肉少女格斗：解剖动态极扎实 |
| `ch-van-doesburg` | 杜斯堡 Van Doesburg | 风格派理论家：引入对角线动感，推动现代建筑与设计 |
| `ch-van-gogh` | 梵高 Van Gogh | 粗犷旋转笔触+极端饱和色，每一笔在燃烧；《星月夜》是他灵魂的X光 |
| `ch-vel` | 委拉斯凯兹 Velázquez | 西班牙巅峰，《宫娥》史上最神秘；笔触自由精准、银灰调优雅 |
| `ch-vermeer` | 维米尔 Vermeer | 左侧窗光的静谧室内、暂停的永恒瞬间，或用暗箱 |
| `ch-victo-ngai` | Victo Ngai 倪传婧 | 香港裔：皮影年画水墨的现代主义演绎，客户苹果/纽约客 |
| `ch-vlaminck` | 弗拉曼克 Vlaminck | 直接挤纯色用刀涂抹，「用心灵作画而非眼睛」 |
| `ch-vuillard` | 维亚尔 Vuillard | 室内装饰：繁复图案柔和色彩将人融入背景，壁毯般华丽 |
| `ch-walker-evans` | 埃文斯 Walker Evans | FSA 南方农民：冷静直接如事实本身 |
| `ch-wang-meng` | 王蒙 Wang Meng | 元四家最繁密：牛毛皴解索皴的细密深山 |
| `ch-warhol` | 沃霍尔 Warhol | 波普之神：丝网印刷金宝汤/梦露/可乐瓶，赞美也暴露机械化空洞；「未来人人成名15分钟」 |
| `ch-watanabe` | 渡边信一郎 Watanabe | 星际牛仔：爵士+黑色电影+港片+动画的干净利落电影感 |
| `ch-watteau` | 华托 Watteau | 洛可可开创者：梦幻花园中的贵族谈情，「华托的忧伤」 |
| `ch-wen-zhengming` | 文徵明 Wen Zhengming | 精细秀美，90岁仍作画，山水兰竹文人气质 |
| `ch-wenqing-yan` | Wenqing Yan | 东方水墨×西方哥特暗黑 |
| `ch-william-blake` | 布莱克 William Blake | 诗人画家，内心宗教幻想，水彩线条如音乐、超脱尘世 |
| `ch-winslow-homer` | 温斯洛·霍默 Winslow Homer | 人与自然对峙：惊险《生命线》与平静加勒比 |
| `ch-wlop` | wlop | 江苏自学成才：《鬼刀》厚涂奇幻少女，光感强烈色彩厚重 |
| `ch-wu-daozi` | 吴道子 Wu Daozi | 「吴带当风」：宗教壁画衣带如风，线条戏剧性动感 |
| `ch-wu-guanzhong` | 吴冠中 Wu Guanzhong | 水墨×现代抽象：「风筝不断线」，江南水墨点线跳跃 |
| `ch-xia-da` | 夏达 Xia Da | 《子不语》《长歌行》：精致优雅、诗词意境飘逸线条 |
| `ch-xia-gui` | 夏圭 Xia Gui | 半边构图：《长江万里图》浩渺壮阔 |
| `ch-xu-beihong` | 徐悲鸿 Xu Beihong | 美术教育奠基：法派素描解剖入水墨，奔马是中国现代标志 |
| `ch-xu-bing` | 徐冰 Xu Bing | 《天书》四千个伪汉字；《地书》只用图标写完整叙事 |
| `ch-xu-xianzhe` | 許先哲 Xu Xianzhe | 「国漫之光」：毛笔般粗线的大漠江湖粗粝史诗 |
| `ch-yan-liben` | 阎立本 Yan Liben | 《步辇图》《历代帝王图》早期宫廷人物巅峰 |
| `ch-yasushi` | 八至 yasushi | 柔和自然色调、氛围感极强的治愈少女 |
| `ch-yi-bu` | 伊吹五月 Yi Bu | 古风少女军娘：细腻华丽、工笔水墨结合、铠甲红绸 |
| `ch-yoneyama` | 米山舞 Yoneyama | 原 Trigger：时尚杂志造型感×动画师动态，冷艳色彩精妙光影 |
| `ch-yoshitoshi` | 芳年 Yoshitoshi | 浮世绘最后伟大者：鬼怪杀戮美丽恐怖结合，残忍梦幻难忘 |
| `ch-yuasa` | 汤浅政明 Yuasa | 最疯狂实验者：变形线条、扭曲透视、自由色彩、无限制 |
| `ch-yue-minjun` | 岳敏君 Yue Minjun | 反复大笑的自我的荒唐空洞不安 |
| `ch-zanne` | 塞尚 Cézanne | 教会世界用几何理解自然：圆柱球锥简化、微妙笔触色彩过渡 |
| `ch-zeng-fanzhi` | 曾梵志 Zeng Fanzhi | 白面具人物的异化焦虑→外科素描般精细的「乱笔」 |
| `ch-zhan-ziqian` | 展子虔 Zhan Ziqian | 《游春图》现存最早山水画 |
| `ch-zhang-daqian` | 张大千 Zhang Daqian | 最多才多艺：早摹古乱真，失明后创「泼墨泼彩」抽象壮丽 |
| `ch-zhang-xiaogang` | 张晓刚 Zhang Xiaogang | 灰调家族旧照风格：头大眼小、血缘线，集体记忆 |
| `ch-zhao-jia` | 赵佳 Zhao Jia | 《黑血》：粗犷有力、强视觉冲击 |
| `ch-zheng-banqiao` | 郑板桥 Zheng Banqiao | 书法入画竹兰石：枝干挺拔叶片疏朗，「六分半书」乱石铺街 |
| `ch-zhou-chunya` | 周春芽 Zhou Chunya | 绿色德牧符号与奔放桃花：野性生命力 |
| `ch-zhou-fang` | 周昉 Zhou Fang | 丰腴贵妇：《簪花仕女图》盛唐贵族奢华审美 |
| `ch-zhu-gengfu` | 祝耕夫 Zhu Gengfu | 《人类进化论》：写实阴郁的环境心理恐怖 |
| `ch-zurbar` | 苏尔巴兰 Zurbarán | 修道院庄重：柠檬陶罐在黑暗中发光，物品如受注视 |

