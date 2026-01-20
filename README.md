## 文件说明（每个文件一句话）

- `README.md`：当前项目的文件索引与用途说明。

### hugegraph-graduation-announcement/

- `hugegraph-graduation-announcement/原始Prompt.md`：生成 HugeGraph 毕业宣传推文与封面图提示词的原始需求 Prompt 留存。
- `hugegraph-graduation-announcement/NanoBananaPrompts.md`：用于生成推文封面图的 Nano Banana 提示词。
- `hugegraph-graduation-announcement/tweet-cn.md`：Apache HugeGraph 毕业（转 TLP）公告的中文推文文案。
- `hugegraph-graduation-announcement/tweet-en.md`：Apache HugeGraph 毕业（转 TLP）公告的英文推文文案。

### vote/

- `vote/vote_tally.py`：从保存的 `lists.apache.org` 邮件线程 HTML 中抽取并统计投票结果，输出 Markdown 报告到标准输出。
- `vote/vote-result.md`：`vote_tally.py` 的投票统计结果。
- `vote/[VOTE] 将 Apache HugeGraph 升级为顶级项目-Apache 邮件存档 --- [VOTE] Graduate Apache HugeGraph to Top-Level Project-Apache Mail Archives.htm`：从 `lists.apache.org` 保存的投票线程页面（供统计脚本作为输入数据源）。
