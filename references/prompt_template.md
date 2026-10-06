# 提示词模板 · 英文官方六段式（H3MXA 定版）

规则：全文英文；主体只绑 Picture、零长相描述；对白只有中文可出现、且只在 `<d>` 内；
派发文件里用一行 `====DETAIL====` 分隔：之前进 timeline 的 global.prompt（主体定义），
之后进 segments[0].prompt；Node 12 的 global_prompt 恒为全文。

## A. 普通段（第 1 段 / 整段内循环）

```
subject_definitions:
<Subject 1> is the man from <Picture 1> (Name), referenced 1:1 from his three-view sheet; his face and outfit follow the reference image exactly and never change.
<Subject 2> is the robot from <Picture 2> (Name), referenced 1:1 from its three-view sheet; its appearance follows the reference image exactly and never changes.
There is no dialogue in this video.
====DETAIL====
summary:
[reference generation] One-sentence statement of the whole segment: who, where, what happens, how it ends (end on a bright frame mid-action if another segment follows).

retention_analysis:
Each subject keeps its 1:1 reference appearance from its picture; the scene stays one continuous location; the camera move is one uncut move.

detailed_description:
[Shot 1] Full action choreography in one flowing paragraph: opening situation, the beats in order, at 1.5x combat speed for fights, non-stop with no pauses, the exact camera behaviour, the closing state. Vertical 9:16, realistic cinematic look.

overall_soundscape:
Only on-site foley: <list only the sounds that truly occur in the picture>. No one speaks.

non_diegetic_music:
N/A
```

有对白时：subject_definitions 末行改写为对白说明，台词在 detailed_description 里写成
`<Subject 1> says, <d>[中文台词]</d>` 形式并带 (S1)/(S2) 编号，全片编号一致。

## B. 尾帧接力段（第 2 段起，Picture 3 = 上一段真实尾帧）

subject_definitions 在 A 的基础上**加一行**：

```
<Picture 3> is the tail frame of the previous segment. The first frame of this segment must be exactly <Picture 3>.
```

retention_analysis **换成尾帧状态逐项描述**（照真实尾帧写，不许凭剧情想象）：

```
<Picture 3> is the tail frame of the previous segment: <构图与场景一句话>; <Subject 1> is on the <left/right>, <姿势、朝向、正在进行的动作逐项>; <Subject 2> is on the <left/right>, <姿势、朝向、动作逐项>; both are <共同状态>. The first frame of this segment keeps the composition, camera angle, positions, poses and ongoing action of <Picture 3> exactly, and the action continues seamlessly from that frame with no restart and no cut. <Subject 1> keeps his 1:1 reference appearance from <Picture 1>; <Subject 2> keeps its 1:1 reference appearance from <Picture 2>.
```

detailed_description 开头固定句式：

```
[Shot 1] The shot opens exactly on <Picture 3>: <用一句话复述尾帧画面与动作状态>, and <动作从这一帧直接继续，接新剧情……>
```

## C. negative（脚本内置，勿改词表）

```
background music, bgm, score, orchestral music, subtitles, text overlay, watermark, deformed limbs, extra fingers, blurry, low quality, slow motion, speech, dialogue, singing, frozen frame
```

注：negative 拦不住本流自配乐（已知行为），不要因此加词或改写正文去「强调禁止」——
禁止句写进正文只会给模型递概念；防线是写死在 non_diegetic_music 的 N/A + 如实报数。
