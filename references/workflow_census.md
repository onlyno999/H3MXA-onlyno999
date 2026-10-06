# 工作流普查档案 · 2084788947984666625（2026-10-06，零扣费哨兵法，建任务 0 / 扣费 0）

- 身份：RunningHub 已发布 workflow（帖子 post/2084788947984666625，邀请码 zedwxo2q）；workflow 端点在线、ai-app 端点 901 不存在（不是 AI App）。
- 节点（11 个）：1, 2, 3, 4, 6, 7, 8, 12, 16, 17, 25。
  - **12 = MiniMaxH3Director（时序总控，唯一派发入口）**
  - 6 = CreateVideo（输出合成，字段 audio/fps/images 是输出侧，**不是图片入口**）
  - 7 = SaveVideo；16/17/25 = 模型相关节点。
- Node 12 可写字段（探针实证）：task_type、global_prompt、timeline_data、total_frames、frame_rate、seed、width、height、steps、cfg、model、sampler、clip、ref_max_size、scheduler。
  - `ref_max_size`：写与不写同种子画面完全一致，无作用。
  - `r2v_groups` / `i2v_groups`：不是 API 可写字段，写了报 field 类错误。
- timeline_data 结构（version 5）：global{taskType, prompt, negativePrompt, refs[]} + segments[]{id, start, length, frameCount, durationSec, prompt, negativePrompt, refs[]} + output{totalFrames, frameRate, width, height} + continuityOverlapFrames=22。
- **refs 正位（2026-10-06 同种子对照实证，本流最重要的一条）**：refs 对象 `{index, imageFile, fileName:"", type:"input", subfolder:""}` 必须在 global.refs 与 segments[].refs **两层都写**；只写全局层、段内 [] → 参考图被静默无视（生成结果与参考人物毫无关系）；双层写 → 人物落地。9 月旧版「段内空则回退全局」在现行线上版失效。
- 显存上限（实证）：单 segment 720 帧 → torch.OutOfMemoryError（failedReason code 805），同参数连派 24 次全灭、零扣费；480 帧单段正常；720 帧拆 3 个 timeline 段可过（但用户不取人工拆段，见 SKILL.md 第 5 节）。
- 音频行为：出片自带音轨（模型自生成）；多版实测自配乐（YAMNet music 0.94–1.00），negative 拦不住；无对白时人声一般 ≤0.13。
- 原始普查全文：本地 `~/workspace/probe_2084788947984666625/probe_2084788947984666625_census.md`（不入仓）。
