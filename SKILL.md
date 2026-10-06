---
name: H3MXA-onlyno999
description: MiniMax H3 导演台长视频生产 Agent（MXA＝导演台线）：走 RunningHub 工作流 2084788947984666625（MiniMaxH3Director · Node 12 时序总控），三视图原图直参锁角、英文官方六段式提示词、参考图双层正位（global＋segments 两层都写）、种子全程记录、长片走尾帧接力两段拼接（上一段尾帧作 Picture 3、提示词写死首帧原样承接）。用户说「导演台」「H3MXA」「导演工作台长视频」时触发。与 H3pro（h3pro-agent）、音频驱动（H3YQ-onlyno999）、复刻（fuke-onlyno999）是不同的线，不许混用节点映射与派发方式。
---

# H3MXA-onlyno999 · 导演台长视频 Agent

## 1. 定位与触发

- **触发**：用户点名「导演台 / H3MXA / 导演工作台」做视频，或明确要用 2084788947984666625 这条流出片。
- **本质**：MiniMax H3 Director（导演台）时序生成——提示词＋参考图喂 Node 12 `MiniMaxH3Director`，由 timeline_data 描述全片；工作流自带内循环与原生音轨（audioMode=generate，模型自生成声音）。
- **前段流程借 H3pro-onlyno999 的工法**（探针→提示词→派发→质检→交付），**只有云端出口换成本流**；其余生产线的节点映射一律不许套到本流上。

## 2. 云端工作流（实证钉死，2026-10-06）

- 工作流：RunningHub **2084788947984666625**（帖子 post/2084788947984666625，邀请码 zedwxo2q），**已发布** workflow（非 ai-app）。
- 节点共 11 个：1, 2, 3, 4, 6, 7, 8, 12, 16, 17, 25。普查档案见 `references/workflow_census.md`。
- **派发只动 Node 12**（MiniMaxH3Director），可写字段：task_type、global_prompt、timeline_data、total_frames、frame_rate、seed、width、height、steps、cfg、model、sampler、clip、ref_max_size、scheduler。
- Node 6 是 CreateVideo（输出合成），**不是图片入口**，不许往 Node 6 塞图。`r2v_groups` / `i2v_groups` 不是 API 可写字段。`ref_max_size` 写不写无任何影响（同种子对照实证）。
- **810 铁律**：未在网页端保存并成功运行过一次的工作流，API 侧一切端点都回 810，无法绕过；遇到 810 先请用户在网页界面手动跑一次再继续。本流已激活，不受此限。

## 3. 铁律（全部经 2026-10-06 实测钉死，违反必翻车）

1. **种子必记**：每一次派发的 seed 必须写进项目任务档案（TASK.md）；同一支片的所有段共用同一个种子。种子是随机起点编号——工作流＋提示词＋参考图＋参数＋种子相同 ≈ 可复现同一抽。
2. **实例规格**：一律 Standard（API `instanceType=default`），不许用 plus。
3. **参考图双层正位**：参考图必须在 `timeline_data.global.refs` **与** `segments[].refs` **两层都写**，对象格式固定 `{index, imageFile, fileName:"", type:"input", subfolder:""}`，index 与 `<Picture N>` 编号一致。**只写全局层会被现行线上版静默无视**（同种子对照实证：只写全局＝人物完全不落地、生成陌生人；双层写＝角色落地）。9 月旧版「段内 [] 回退全局」的说法已失效。
4. **主体零描述**：提示词里**绝不描写人物长相/服装细节**。主体只写一句绑定：「<Subject N> is the man/robot from <Picture N>, referenced 1:1 from his/its three-view sheet; face/outfit/appearance follow the reference image exactly and never change.」用文字描长相＝模型照文字重画＝必漂移。参考图直接上传演员三视图原图，不做定妆重绘。
5. **提示词语言**：全文英文官方六段式（顺序固定）：subject_definitions → summary → retention_analysis → detailed_description → overall_soundscape → non_diegetic_music（无配乐写 `N/A`）。只有对白可以是中文、且只许出现在 `<d>[中文] …</d>` 里并带 (Sx) 说话人编号；其余任何位置不许出现中文字符。
6. **单段帧数上限**：单个 timeline 段 **720 帧（30 秒）必爆显存**（torch.OutOfMemoryError 错误码 805，同参数连派 24 次全灭、零扣费）；480 帧（20 秒）单段可过。长片不许整段硬派，见第 5 节两种合法打法。
7. **打斗速度**：1.5 倍速写进提示词的动作节奏本身（"at 1.5x combat speed"、全程不停顿），不是后期变速；negative 里带 slow motion / frozen frame 封堵。
8. **音频预期**：本流自己生成音轨且**倾向自配乐**（实测多版 music 0.94–1.00，negative 拦不住），无人声旁白时人声一般干净。质检必须跑音频筛查并**如实报数**；判罚只认两样——能听懂的旁白与背景音乐。测试性质的片子保留原生轨交付＋报数，不许擅自换轨把测试结果洗白。

## 4. 标准生产流程

1. **立项**：建项目目录与 TASK.md，先定本片种子并记录；确认画幅（默认 9:16 竖屏 720×1280 → 工作流宽高 736×1280）、总时长与打法（第 5 节）。
2. **探针**：新端点/新工作流先走零扣费哨兵普查（只读字段、绝不建任务，无任何扣费），确认已发布与 Node 12 字段后再派发；已普查过的本流可跳过。本流普查结论在 `references/workflow_census.md`。
3. **参考图**：演员三视图原图上传 RunningHub（upload_media）拿到 `openapi/…` 路径，按出场顺序编号 Picture 1、Picture 2……
4. **写提示词**：按 `references/prompt_template.md` 的六段式模板写；主体只绑 Picture（铁律 4）；动作、运镜、场景全写在 detailed_description；只写画面里真实有的现场拟音。
5. **派发**：`scripts/dispatch_director.py run --prompt-file P --seed S --frames F --refs 路径1,路径2[,尾帧路径]`（脚本自动双层写 refs、Node 12 only、Standard）。派发后把 taskId＋seed 立刻记进 TASK.md。
6. **回片**：`poll TASKID --outdir DIR` 轮询下载；FAILED 先看 failedReason，805 显存问题不要原地连环重派同一参数（先降段长）。
7. **质检**（自己跑完，不拿判断题烦用户）：抽帧查人物锁定（尤其**中段**——长段里搭档可能在中途变形成另一个主角的样子再变回来，首尾帧查不出来）；音频筛查（YAMNet，人声/音乐报数）；分辨率与帧数核对。
8. **交付**：按交付编码规格收尾（视频 yuv420p、H.264 High@L4.0、bt709 tv range、avc1；音频 AAC LC 48kHz；`-map_metadata -1`；+faststart；成品 720×1280），ffprobe 验后交付，**每次返发用新文件名**。

## 5. 长片打法（二选一）

### A. 内循环整段（≤20 秒）
一段 timeline 写满全片剧情（一个 segment、≤480 帧），导演台内循环自己处理节奏。不许人工拆段、不许截尾帧接力——用户明确：整段提示词一次写完。

### B. 尾帧接力两段拼接（20 秒以上 / 用户点名分段时）— 2026-10-06 天空大战实证成功
1. 第 1 段按标准流程派（10 秒＝240 帧），回片后**抽取其真实尾帧**（成片最后一帧，不许用预置图冒充）。
2. 尾帧上传，作为 **Picture 3** 与两张三视图一起进双层 refs。
3. 第 2 段提示词必须**写死承接**（模板见 `references/prompt_template.md`）：
- subject_definitions 里加一行：「<Picture 3> is the tail frame of the previous segment. The first frame of this segment must be exactly <Picture 3>.」
- retention_analysis **逐项写清尾帧状态**：构图、机位、两人左右位置、姿势、正在进行的动作与运动方向；并写明本段首帧与之完全一致、动作无缝继续、不重开镜头。
- detailed_description 开头复述一次「The shot opens exactly on <Picture 3>: …」再接新剧情。
4. 同种子派第 2 段（240 帧）。实证：段2 首帧与段1 尾帧几乎逐像素一致，接缝不可见。
5. **拼接**（`scripts/splice_2x10.py`）：第 1 段取满额定帧数 ＋ 第 2 段**去掉第 0 帧**接上（只去首帧，不许剪音频、不许改时长对齐）；第 2 段音频整体后移 1 帧（1/24 秒）与画面对齐；硬切，不留渐黑。

## 6. 已知翻车点清单（质检必查）

- 搭档中段变形（20 秒水面版约 2–8 秒铁蛋变成第二个刁哥、10 秒变回；30 秒版末尾 5 秒刁哥变机器人）——长段越长越容易犯，抽帧必须密查中段与末段。
- 只写全局 refs → 人物不落地（铁律 3）。
- 提示词描长相 → 模型照文字重画漂移（铁律 4）。
- 单段 720 帧 → 805 显存爆（铁律 6）。
- 自配乐 → 如实报数（铁律 8），不许把拟音误报成 BGM，也**不许把真 BGM 说成拟音**：先看 YAMNet top 类与持续性再定性。

## 7. 案例

- 2026-10-06 导演台测试项目全程（水面 20 秒正位版、天空 30 秒内循环版、天空 2×10 尾帧接力版）：见 `references/case_2026-10-06_director_tests.md`。其中尾帧接力版为本 Agent 的定版成功案例。
