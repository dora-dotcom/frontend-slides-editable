# Frontend Slides - Editable

一个适用于 Claude Code / Codex 的技能，用来生成惊艳、带动画、单文件的 HTML 演示文稿，并内置浏览器编辑器：可拖拽对象、调整大小、编辑文本、重排页面、本地保存，并导出干净的独立 HTML。

A Claude Code / Codex skill for creating stunning, animation-rich, single-file HTML presentations with a built-in browser editor: drag objects, resize blocks, edit text, reorder slides, save locally, and export a clean standalone HTML.

## 这个 Skill 是做什么的 / What This Does

**Frontend Slides - Editable** 是 **frontend-slides** 的可编辑分支。它保留了原始 skill 的风格探索流程、视口适配规则和 PPT 转换能力，并在此基础上加入完整的浏览器内编辑运行时。**交付用的幻灯片仍应按 `STYLE_PRESETS.md` 实现各预设的布局与签名元素**；可编辑只是增加运行时，不是把多套风格压成同一套版式原型。`examples/generated/presets/` 仅为运行时自检样例。

**Frontend Slides - Editable** is the editable fork of **frontend-slides**. It preserves style discovery, viewport discipline, and PPT conversion from the original skill, then adds a full in-browser editing runtime. **Real decks should still implement each preset’s layout and signature elements from `STYLE_PRESETS.md`** — edit mode is an add-on, not permission to reuse one generic slide prototype for every aesthetic. `examples/generated/presets/` is for runtime smoke tests only.


https://github.com/user-attachments/assets/dc1db494-5e8c-4bbc-9c4a-d02be74c8e89


它适合“生成后还要继续改”的场景，例如：

It is designed for workflows where the generated output must remain editable:

- 直接在幻灯片上移动对象
- 使用 **Ctrl+点击** 多选
- 调整文本框大小并让文字自动重排
- 对文本进行 **粗体 / 斜体 / 字体 / 字号** 编辑
- 使用 **Undo / Redo**
- 在 **Pages** 侧栏重排或删除页面
- 将完整 deck 结构保存到 `localStorage`
- 导出清理过临时编辑状态的独立 `.html`

- move objects directly on slides
- use **Ctrl+click** multi-select
- resize text blocks with automatic reflow
- edit text inline with **bold / italic / font / size**
- use **Undo / Redo**
- reorder and delete slides from the **Pages** sidebar
- persist full deck structure to `localStorage`
- export a sanitized standalone `.html`

如果只需要更轻量的只读输出，请使用父 skill **frontend-slides**。

If you only need the smallest read-only output, use the parent **frontend-slides** skill.

## Skill 对照表 / Skill Comparison

| 维度 / Dimension | `frontend-slides` | `frontend-slides-editable` |
|------|------|------|
| 核心定位 / Primary job | 生成更轻量的只读 HTML 演示 / Generate lighter read-only HTML decks | 生成可继续编辑的 HTML 演示 / Generate editable HTML decks |
| 输出重量 / Output weight | 更小、更干净 / Smaller and lighter | 更重，但包含完整编辑器 / Heavier, with full editor runtime |
| 样式流程 / Style flow | 依赖父 skill 当前安装版本 / Depends on the installed parent-skill version | 先问样式偏好，再推荐预设，再决定直选或看预览 / Ask style preference first, recommend presets, then choose direct pick or previews |
| 预设表现 / Preset fidelity | 按 `STYLE_PRESETS` 逐套实现版式与签名元素 / Implement layout + signatures per preset | **同上，不得因可编辑而统一成单一首屏模板** / **Same — do not collapse all styles into one title-slide template** |
| 浏览器内编辑 / In-browser editing | 可选文本编辑 / Optional text editing | 默认完整编辑运行时 / Full editing runtime by default |
| 页面管理 / Slide management | 无 Pages 侧栏 / No Pages sidebar | 有缩略图侧栏、重排、删除 / Sidebar with thumbnails, reorder, delete |
| 对象操作 / Object manipulation | 不支持对象级拖拽缩放 / No object-level drag or resize | 支持拖拽、缩放、吸附、多选 / Drag, resize, snap, multi-select |
| 历史记录 / Undo and redo | 无完整对象历史 / No full object history | 内置 Undo / Redo / Built-in undo and redo |
| 本地保存 / Local persistence | 仅在启用编辑时保存文本改动 / Save text edits when editing is enabled | 保存完整 deck 结构 / Save full deck structure |
| 适合场景 / Best for | 交付成品、体积敏感、只读展示 / Final delivery, size-sensitive, read-only decks | 评审后继续改稿、团队协作、客户反馈迭代 / Post-review edits, collaboration, iterative feedback |
| 什么时候选它 / When to choose it | 你已经接近定稿 / You are close to final | 你预期还会持续改布局和内容 / You expect continued layout and content changes |

## 核心特性 / Key Features

- **零依赖**：单个 HTML 文件，CSS/JS 内联，无需 npm、构建工具或框架
- **可视化风格探索**：通过预览选风格，而不是抽象描述
- **完整可编辑运行时**：支持拖拽、缩放、文本格式化、缩略图侧栏和历史记录
- **PPT 转换**：将 `.pptx` 转为可编辑网页幻灯片并保留资源
- **视口安全**：每一页都要求适配视口，不允许内部滚动
- **持久化与导出**：`Ctrl+S` 保存结构化状态；Export HTML 剥离临时编辑态；Export PDF 生成固定像素尺寸文件（16:9 / 4:3）
- **图片支持**：侧边栏 ＋ Add Image 上传图片对象；双击图片对象可替换；支持背景图替换
- **反模板感**：通过精选风格预设，避免千篇一律

- **Zero dependencies**: Single-file HTML with inline CSS/JS, no npm/build/framework
- **Visual style discovery**: pick by preview, not design jargon
- **Full editable runtime**: drag/resize/text formatting/filmstrip/history included
- **PPT conversion**: convert `.pptx` into editable web slides with preserved assets
- **Viewport-safe output**: every slide must fit the viewport without internal scrolling
- **Persistence + export**: `Ctrl+S` saves structure; Export HTML strips edit state; Export PDF produces a fixed-pixel file (16:9 or 4:3) via native browser print — no quality loss
- **Image support**: sidebar ＋ Add Image uploads a new image object; double-click any graphic to replace it; background replacement supported per slide
- **Anti-generic aesthetics**: curated presets over bland default templates

## 适合什么场景 / When To Use This

适合 **frontend-slides-editable**：

Use **frontend-slides-editable** when you want:

- 生成后仍可在浏览器继续微调
- 支持客户/团队评审后的布局修订
- 单文件、零构建的可交付结果
- PowerPoint 转网页后继续编辑

- a generated deck you can continue refining in browser
- post-generation layout iteration during reviews
- a single-file deliverable with no build step
- PowerPoint-to-web conversion with continued editing

适合 **frontend-slides**：

Use **frontend-slides** when you want:

- 更小更轻的只读输出
- 不需要编辑器界面
- 最轻量的生成文件

- a smaller read-only output
- presentation-only HTML without editor chrome
- the lightest possible generated file

## 安装 / Installation

把目录复制到你的 skill 目录：

Copy this directory into your skill folder:

### Claude Code 用户 / For Claude Code users

```bash
cp -r frontend-slides-editable ~/.claude/skills/
```

### Codex 用户 / For Codex users

```bash
cp -r frontend-slides-editable ~/.codex/skills/
```

然后调用：

Then invoke it with:

```text
/frontend-slides-editable
```

## 用法 / Usage

### 新建可编辑演示 / Create a new editable presentation

```text
/frontend-slides-editable

> "帮我做一个关于 AI agents for product teams 的分享"
```

这个 skill 会：

The skill will:

1. 先**成组提问**（目标、页数、内容准备情况、样式偏好、编辑范围、**是否有图片素材**）——除非用户已经提供了完整 brief，或显式调用本可编辑 skill 且信息已经足够，否则不应直接生成整稿；详见 `SKILL.md` 的 **Discovery gate**。
2. 根据你的样式偏好、受众和内容，先推荐一组更匹配的风格预设。
3. 分析你提供的文本和图片（若 Question 6 为无图则跳过图片评估）。
4. 让你直接选推荐预设，或基于推荐方向生成风格预览。
5. 产出带编辑运行时的单文件 HTML 演示，并在浏览器中打开。

1. **Ask in one grouped turn** (purpose, deck length, content readiness, style preference, runtime scope, **image assets or not**) — do not generate the full deck until discovery is satisfied unless the user supplied a complete brief, or explicitly invoked this editable skill with enough detail to skip discovery; see **Discovery gate** in `SKILL.md`.
2. Recommend a shortlist of presets based on style preference, audience, and content.
3. Review provided text and images (skip image evaluation if Phase 1 says no images).
4. Let the user pick from those recommendations directly or generate previews from that direction.
5. Build a single-file HTML deck with editable runtime and open it in the browser.

### 增强现有 HTML / Enhance an existing HTML deck

```text
/frontend-slides-editable

> "Improve this HTML deck and keep it editable"
```

这个 skill 会：

The skill will:

1. 读取现有演示文稿。
2. 修改前检查内容密度与视口适配。
3. 保护编辑运行时契约（如 `section.slide`、`.slide-edit-layer`、`data-oid`）。
4. 在保持编辑/持久化/导出能力的前提下更新 deck。

1. Read the current deck.
2. Validate density and viewport fit before edits.
3. Preserve runtime contracts (`section.slide`, `.slide-edit-layer`, `data-oid`, etc.).
4. Update content while keeping edit/persist/export intact.

### 转换 PowerPoint / Convert a PowerPoint

```text
/frontend-slides-editable

> "Convert presentation.pptx into an editable web slideshow"
```

这个 skill 会：

The skill will:

1. 提取 PPT 文字、图片和备注。
2. 与你确认结构。
3. 先询问样式偏好，并给出对应的视觉风格推荐。
4. 生成可编辑 HTML deck 并保留内容与资源。

1. Extract text, images, and notes from PPT.
2. Confirm the extracted structure.
3. Ask for style preference first and recommend matching visual directions.
4. Generate an editable HTML deck with preserved assets.

## 编辑体验 / Editing Experience

生成后的 deck 默认包含：

Generated decks include:

- **编辑模式 / Edit mode**：按 `E` 或从左上角呼出控件
- **Pages 侧栏 / Pages sidebar**：缩略图导航、重排、删除
- **对象编辑 / Object editing**：用 **⠿** 拖动，角点缩放，吸附线对齐
- **富文本工具栏 / Rich text toolbar**：支持 **粗体/斜体/字体/字号**
- **历史记录 / History**：`Ctrl+Z`、`Ctrl+Y`、`Ctrl+Shift+Z` 及 macOS 等价键
- **持久化 / Persistence**：`Ctrl+S` 保存完整 `.slides-offset` 到 `localStorage`
- **Export HTML**：下载不含临时编辑态与选中态类名的干净 `.html`（可演示版）
- **Export PDF**：侧边栏选择 16:9 或 4:3，在新标签页生成固定像素 HTML 并自动触发打印对话框
- **图片上传 / Image upload**：侧边栏 **＋ Add Image** 上传图片到当前幻灯片；双击图片对象可替换
- **背景替换 / Background replace**：编辑模式下悬停幻灯片背景区域，点击 **📷 Replace background** 按钮上传新背景图

## 内置风格 / Included Styles

### 深色主题 / Dark Themes
- **Bold Signal** - 自信、高冲击力 / Confident, high-impact
- **Electric Studio** - 干净、专业 / Clean, professional
- **Creative Voltage** - 高能霓虹 / Energetic neon
- **Dark Botanical** - 优雅精致 / Elegant, refined

### 浅色主题 / Light Themes
- **Notebook Tabs** - 编辑感与纸张感 / Editorial paper feel
- **Pastel Geometry** - 友好轻快 / Friendly pastel geometry
- **Split Pastel** - 活泼双色分割 / Playful two-tone split
- **Vintage Editorial** - 杂志感与个性化 / Personality-driven editorial

### 特殊风格 / Specialty
- **Neon Cyber** - 未来感霓虹 / Futuristic neon glow
- **Terminal Green** - 开发者终端风 / Hacker-terminal aesthetic
- **Swiss Modern** - 包豪斯极简 / Bauhaus-inspired minimal
- **Paper & Ink** - 文艺排版 / Literary paper-and-ink

## 文档结构 / Documentation Map

| 文件 File | 作用 Purpose |
|------|------|
| `SKILL.md` | 核心流程与交付规则 / Workflow and delivery behavior |
| `editor-runtime.md` | 运行时 DOM 契约与检查项 / Runtime DOM contracts and checklist |
| `examples/editable-deck-reference.html` | 标准参考实现 / Canonical runtime reference |
| `STYLE_PRESETS.md` | 12 个精选风格 / 12 curated style presets |
| `viewport-base.css` | 视口适配基础样式 / Viewport-fit base CSS |
| `html-template.md` | HTML 基础结构说明 / Base HTML integration notes |
| `animation-patterns.md` | 动画参考 / CSS/JS animation reference |
| `scripts/extract-pptx.py` | PPT 内容提取脚本 / PPT extraction script |
| `examples/generated/presets/*.html` | 12 个单风格可编辑样例（与 STYLE_PRESETS 一一对应） / One editable deck per preset |
| `scripts/build-preset-decks.py` | 从参考实现批量生成上述样例 / Build all preset sample files |

## 架构说明 / Architecture

这个 skill 延续父项目“渐进式披露”策略：

This skill follows the parent project's progressive-disclosure approach:

- `SKILL.md` 承载流程和规则 / `SKILL.md` carries workflow and rules
- 支撑文件按需加载 / supporting docs load on demand
- 可编辑运行时保持唯一参考实现 / one canonical runtime implementation
- 生成结果零依赖且可移植 / generated decks stay dependency-free and portable

运行时有几个不可破坏的约束：

The runtime depends on non-negotiable contracts:

- 每页必须是带稳定 `id` 的 `section.slide`
- 可移动内容位于 `.slide-edit-layer`
- 可编辑块使用 `[data-slide-object][data-oid]`
- 页面枚举必须限定真实 deck 根，不能包含缩略图克隆

- each slide is a `section.slide` with stable `id`
- movable content lives in `.slide-edit-layer`
- editable blocks use `[data-slide-object][data-oid]`
- slide enumeration must stay scoped to the true deck root

## 设计理念 / Philosophy

1. **通过“看见选项”建立审美。** 风格预览比抽象问卷更有效。  
2. **生成不是定稿。** 第一版必须天然可编辑。  
3. **依赖就是债务。** 单文件 HTML 应该多年后仍可用。  
4. **尊重视口。** 放不下就拆页，而不是隐藏溢出。  
5. **有辨识度优先。** 工具应帮助产出可记忆的内容。  

1. **People discover taste by seeing options.** Previews beat abstract questionnaires.  
2. **Generated is not final.** The first draft should remain editable.  
3. **Dependencies are debt.** A single HTML should still work years later.  
4. **Respect the viewport.** Split slides instead of hiding overflow.  
5. **Distinctiveness wins.** Presentation tools should produce memorable output.  

## 依赖要求 / Requirements

- [Claude Code](https://claude.ai/claude-code) 或兼容运行器
- 如需 PPT 转换：Python + `python-pptx`
- 如需浏览器编辑/导出：现代 Chromium、Safari 或 Firefox

- [Claude Code](https://claude.ai/claude-code) or a compatible runner
- For PPT conversion: Python + `python-pptx`
- For editing/export: modern Chromium, Safari, or Firefox-class browser

## 试用参考 / Try The Reference

打开：

Open:

```text
examples/editable-deck-reference.html
```

**12 个独立可编辑样例（每种风格一个 HTML）：**

**Twelve separate editable decks (one file per preset):**

```text
examples/generated/presets/bold-signal.html
examples/generated/presets/electric-studio.html
examples/generated/presets/creative-voltage.html
examples/generated/presets/dark-botanical.html
examples/generated/presets/notebook-tabs.html
examples/generated/presets/pastel-geometry.html
examples/generated/presets/split-pastel.html
examples/generated/presets/vintage-editorial.html
examples/generated/presets/neon-cyber.html
examples/generated/presets/terminal-green.html
examples/generated/presets/swiss-modern.html
examples/generated/presets/paper-ink.html
```

重新生成上述文件：

Regenerate all preset samples:

```bash
python3 scripts/build-preset-decks.py
```

然后试试：

Then try:

- 按 `E` / press `E`
- 点击文本编辑 / click text to edit
- 使用浮动工具栏 / use the floating toolbar
- 用 **⠿** 拖拽对象 / drag objects with **⠿**
- 缩放选中对象 / resize a selected object
- 在 **Pages** 重排 / reorder in **Pages**
- 按 `Ctrl+S` 保存 / press `Ctrl+S`
- 导出 deck / export the deck

## 致谢 / Credits

基于 [@zarazhangrui](https://github.com/zarazhangrui/frontend-slides) 的 **frontend-slides** 扩展而来，本分支新增可编辑运行时。

Based on **frontend-slides** by [@zarazhangrui](https://github.com/zarazhangrui/frontend-slides), with editable runtime added in this fork.

## 许可证 / License

MIT（与父项目一致，除非另有说明）。

MIT (same as the parent project unless otherwise noted).
