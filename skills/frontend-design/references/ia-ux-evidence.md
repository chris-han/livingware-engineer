# IA / UX evidence — 原始依据与综合边界

阅读日期：2026-10-12。用途：支持 [IA/UX 原则](ia-ux-principles.md) 与 [检查清单](ia-ux-checklist.md) 的设计推理，并补齐现有 `docs/ia-before-ui.md` 的证据来源。该证据参考是文献前提的唯一持久所有者；工作流只链接它，不复制文献综述或创建新的研究台账。

## 目录

- [本次问题与证据范围](#本次问题与证据范围)
- [S1–S6 来源](#s1s6-来源)
- [综合与采用边界](#综合与采用边界)
- [可验证的设计假设](#可验证的设计假设)

## 本次问题与证据范围

**设计目标：**为已存在的 IA-before-UI 与 frontend-design 补充可靠的认知解释和可执行检查，使任务上下文、材料、依据和结果的层级可评审。**当前不确定性：**自动确定工作区是否同时免除显示上位上下文，以及哪些卸载机制值得采用而不会遮蔽必要判断。**现有依据：**Livingware main `b95f75d7cabd49c7fdf434e2b3d6a5a7be979de2` 已有 JTBD、认知工作分配、Fast-to-Aha、语义所有者、状态恢复与设计源映射。沿用这些所有者；新增的是溯源、条件原则与验收问题。

**证据方法：**阅读下列原始论文的论证/方法/限制、Norman 的已取得章节和作者资料，区分来源前提、项目综合与采用规则；以正常、冲突、过期、恢复和辅助访问场景检查推论是否过度。此任务是理论综合与规范维护，无保护测试集、统计改善结果或新产品实验。原文 PDF/扫描/OCR 只用于阅读，不打包进 MIT 技能，也不把参考文献中的未直接阅读论文当作本次直接证据。

**阅读边界：**Norman 取得第 2 章原文（印刷页 37–73）及作者目录/概念说明，未取得第 3/4 章或全书全文，不声称整书精读。Nielsen 1994 阅读正文、方法、结论与相关附录；Kirsh 阅读作者提供的全文及其版本说明；Risko/Gilbert 阅读发表版本正文、图 1–3、Box 1–3 与限制；Hollan 等阅读作者扫描版的理论、研究框架与数字工作材料设计论证，OCR 用于定位且不作为逐字引文来源。以下摘要刻意简短，产品规则不冒充原文结论。

## S1–S6 来源

### S1 — Nielsen 的启发式与证据限制

Jakob Nielsen (1994). *Enhancing the Explanatory Power of Usability Heuristics*. CHI '94, pp. 152–158. DOI: [10.1145/191666.191729](https://doi.org/10.1145/191666.191729)。[本次阅读副本](https://static.aminer.org/pdf/PDF/000/089/679/enhancing_the_explanatory_power_of_usability_heuristics.pdf)。另读作者维护的 [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/)。

**支持的前提：**1994 研究比较 101 项启发式对 11 个项目中 249 个既有问题的解释，提出九项候选；作者现行清单包含帮助与文档，共十项。状态可见与可识别的可选动作是不同问题；一致性、现实概念、控制、预防与恢复共同参与可用性。**限制：**评分含主观性且无额外评分者；作者明确区分解释既有问题与发现新问题。不能把十项清单称为普遍定律、保证完整覆盖，或据它推导某一布局已有效。

### S2 — Norman 的行动循环与可理解交互

Don Norman (2013). *The Design of Everyday Things: Revised and Expanded Edition*. Basic Books. ISBN: 978-0-465-05065-9。[作者书页/目录](https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/)。[本次第 2 章原文](https://magrawala.github.io/cs347-sp24/assets/docs/DesignofEveryDayThingsChapter2.pdf)。辅助概念核对：[Signifiers, not affordances](https://jnd.org/signifiers-not-affordances/)。

**支持的前提：**第 2 章区分执行与评价鸿沟，以目标、行动与结果理解解释交互；前馈帮助选择/实施动作，反馈帮助理解结果。七项原则包括可发现性、反馈、概念模型、可供性、指示线索、映射与约束。行动可反复、由事件触发，不要求完整依次走完七步。**限制：**这是设计解释框架，并非特定页面的对照实验；七步不能直接变成七屏向导。第 3 章外部知识只核对到作者目录，不据未读章节新增实证声明。

### S3 — Kirsh 的空间认知工作

David Kirsh (1995). *The Intelligent Use of Space*. Artificial Intelligence, 73(1–2), pp. 31–68. DOI: [10.1016/0004-3702(94)00017-U](https://doi.org/10.1016/0004-3702(94)00017-U)。[作者全文](https://adrenaline.ucsd.edu/kirsh/Articles/Space/AIJ1.html)注明发表版略有修订；这里采用作者版明确的论证，不能以网页段落假造期刊页码。

**支持的前提：**空间安排可以简化选择、感知与内部计算；分区、排列、标记和及时的环境变化帮助跟踪状态及下一步。论文依据日常活动观察与 Tetris 研究讨论机制，也说明编码同时受技能、任务和时间影响。**限制：**作者讨论计算节约的量化困难；不支持把 Tetris 时间效果迁移成企业 UI 效果，不支持任意布局、固定方向或自动重排都更优。

### S4 — Hollan、Hutchins、Kirsh 的分布式认知

James Hollan, Edwin Hutchins, David Kirsh (2000). *Distributed Cognition: Toward a New Foundation for Human–Computer Interaction Research*. ACM TOCHI, 7(2), pp. 174–196. DOI: [10.1145/353485.353487](https://doi.org/10.1145/353485.353487)。[作者全文扫描](https://interactivity.ucsd.edu/articles/DCog/DCog.pdf)。

**支持的前提：**分析单位由参与过程的功能关系确定，可包括人、工作材料、工具及跨时间的产物；研究框架把理论、观察与实验联系起来，并探索数字工作材料。界面不应只按孤立按钮评价，还要看表征如何在完整活动中协调与传播。**限制：**这不表示每个区域必须同时显示全部信息，不建立多代理系统、数据库或语义权威，也没有直接验证 Semantier 的面板同步实现。

### S5 — Risko、Gilbert 的认知卸载与代价

Evan F. Risko, Sam J. Gilbert (2016). *Cognitive Offloading*. Trends in Cognitive Sciences, 20(9), pp. 676–688. DOI: [10.1016/j.tics.2016.07.002](https://doi.org/10.1016/j.tics.2016.07.002)。[作者提供的发表版本](https://samgilbert.net/pubs/Risko2016TiCS.pdf)。[机构记录/作者稿](https://discovery.ucl.ac.uk/id/eprint/1508770/)。

**支持的前提：**身体与外部工具可改变任务处理需求；是否卸载取决于实际需求和可能失准的元认知评价。综述讨论提醒、外部记忆、收益与代价，Box 1 提供 choice/no-choice 方法，Box 3 涉及自动化偏差/依赖，图 3 是提出的元认知模型。**限制：**愿意卸载不证明有客观收益，实验条件也可能引入策略抑制负担；提出的模型不是已验证的产品因果模型。不能据其宣称 LLM 自动决策安全或长期能力改善。

### S6 — Nielsen 的渐进披露实践

Jakob Nielsen (2006-12-03). *Progressive Disclosure*. [作者文章](https://www.nngroup.com/articles/progressive-disclosure/)。

**支持的前提：**将主要内容与不常用/高级选项分层，使初始界面聚焦；文章也区分依任务顺序推进的 staged disclosure。**限制：**它是实践指导，不是本次人类对照实验；不意味着把关键上下文、风险、证据缺口或可纠正入口隐藏，也不规定一定采用向导。

## 综合与采用边界

| 层级 | 本次结论 | 所有者与非声明 |
| --- | --- | --- |
| 来源前提 | 表征与工具参与任务；可用性涉及行动、状态理解、记忆、控制与恢复 | S1–S6；不能外推确定的本地收益 |
| 设计综合 | 上位上下文先可识别；信息顺序跟随依赖；空间帮助比较；动态披露保留稳定锚点 | 原则 P01–P16；属于推论与工程综合 |
| 明确采用 | 通过现有 frontend-design 条件加载原则与清单，沿用 IA-before-UI gate 与项目权威 | 用户本次明确要求；不是自动学习授权 |
| Semantier 应用 | 工作台 header 唯一工作区切换；任务、材料、Inspector 与 chat 保持真实绑定 | 条件应用示例；本次未实施产品代码 |
| 经验声明 | 局部路径正确、设计一致性、人类任务收益分别报告 | 必须各有对应证据；当前无新增人类测量 |

这些来源没有证明“header 永远最佳”“信息越少越好”“一切都自动化”“点击越少认知负荷越低”。现行单一语义所有者、Fix → Infer → Recommend → Ask、Fast-to-Aha、UNKNOWN 与授权边界来自 Livingware/项目约束，不归功于这些论文。检查清单是把推论变为可证伪的工程问题，而非再次宣称原作者已经验证它们。

## 可验证的设计假设

**采用的方向：**自动确定上下文与让用户识别上下文分别设计。对于 resume-screening 示例，把真实作用范围放到动作前并消除竞争性 selector，预计减少归属误判和恢复时的查找；收益保持待测。**可反驳的情况：**用户仍看错工作区、误用示例、在窄屏找不到入口，或在比较时错误增加，则必须修订局部方案，不能以符合启发式为理由保留它。

**验证路线：**先用真实绑定、竞态/恢复反例和浏览器访问证明结构；若需要收益声明，再采用可比任务的人类研究，按现有研究流程声明指标、范围与停止条件。**本次停止点：**原始前提可追溯、规范与清单接入原技能、发布验证完成；不自动开启 UI 实施、人类实验或代理行为学习。具体页面的收益仍是 `UNMEASURED`，发布版本不改变这一状态。
