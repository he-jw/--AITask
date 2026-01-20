# HugeGraph graduation tweet kit — generation process

## 原始需求 Prompt（原文留存）

```
请为 Apache HugeGraph 从 Apache 基金会毕业这一重要里程碑创建完整的推文宣传材料，包括以下具体内容：

**1. 推文内容创作**
- 英文推文：创建文件 `hugegraph-graduation-announcement/tweet-en.md`，内容需要包含：
  - 正式宣布 HugeGraph 从 Apache 孵化器毕业成为顶级项目
  - 突出关键成就（210+ 贡献者、5个Apache发布版本、多行业生产环境应用等）
  - 感谢社区和导师支持
  - 包含相关链接（官网、GitHub等）
  - 适合 Twitter/X 平台发布的格式和长度

- 中文推文：创建文件 `hugegraph-graduation-announcement/tweet-cn.md`，内容为英文版本的中文翻译，需要：
  - 保持与英文版本信息一致
  - 使用适合中文社交媒体的表达方式
  - 保留所有重要链接和数据

**2. 推文封面图设计提示词**
为 Nano Banana（AI 图像生成工具）创建详细的提示词，用于生成推文封面图，要求：
- 体现 Apache 基金会的专业性和权威性
- 突出 HugeGraph 图数据库的技术特色
- 包含毕业庆祝的元素
- 适合社交媒体使用的视觉效果

**3. 参考格式要求**
首先访问并分析参考链接：https://news.apache.org/foundation/entry/the-apache-software-foundation-announces-new-top-level-projects-3
- 请先展示你从该链接获取的内容，确保理解了 Apache 基金会官方公告的标准格式
- 推文内容应参考该格式的语调、结构和重点信息呈现方式

**4. 参考资料使用**
基于提供的 Jermy Li 的毕业投票邮件内容，提取以下关键信息用于推文：
- 社区成长数据（210+ 贡献者、10个新提交者、2个新PPMC成员）
- 技术成就（5个Apache发布版本、多组件协调发布）
- 应用场景（金融、电商、电信等行业生产环境使用）
- 生态合作（与 Apache SeaTunnel、TinkerPop 等项目集成）
- 访问邮件中提到的所有参考链接，获取更多背景信息

Key Highlights:  关键要点：

- Since joining the Incubator in January 2022, HugeGraph has successfully
  built a friendly, diverse, and independent community under the guidance of
  the Apache Way.
- Community Growth: The community has grown to 210+ contributors. We have
  elected 10 new committers and 2 new PPMC members during
  incubation. The PPMC and committer group represents 8+ different companies
  and universities, ensuring vendor-neutrality.
- Releases: We have published 5 Apache releases (1.0 to 1.7), managed by 5
  different release managers. We coordinate synchronized releases across
  Server, Toolchain, Computer, and AI components.
- Adoption: HugeGraph is used in production by diverse organizations worldwide
  across finance, e-commerce, and telecommunications.
- Ecosystem: We actively participate in GSoC and OSPP. The project is
  integrated
  with Apache SeaTunnel & TinkerPop and has deep technical
  cooperation with other open-source projects.
- Governance: The initial PMC membership has been confirmed, and the Chair/VP
  has been selected. We have strictly followed ASF policies
  regarding license compliance and branding. The trademark transfer is proceeding
  in parallel with graduation.

References:
[1] https://lists.apache.org/thread/7tx4g7ytc7fg96c64o6451q6y6k6qq9w (Graduation Discussion in Incubator)
[2] https://lists.apache.org/thread/mb77pmhft4bhrmmypcwl94dg9fcfgp2y (HugeGraph Community Vote)
[3] https://hugegraph.apache.org/ (Website Link)
[4] https://github.com/apache/incubator-hugegraph (GitHub Link)
[5] https://incubator.apache.org/projects/hugegraph.html (Project Status)
[6] https://whimsy.apache.org/roster/ppmc/hugegraph (HugeGraph Roster)

**输出要求**
- 两个独立的 markdown 文件内容
- 一个详细的图像生成提示词
- 确保所有内容专业、准确、具有庆祝性质
```
