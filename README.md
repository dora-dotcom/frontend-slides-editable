# Frontend Slides - Editable

一个适用于 Claude Code / Codex 的技能，用来生成惊艳、带动画、单文件的 HTML 演示文稿，并内置浏览器编辑器：可拖拽对象、调整大小、编辑文本、重排页面、本地保存，并导出干净的独立 HTML 或高质量 PDF。

A Claude Code / Codex skill for creating stunning, animation-rich, single-file HTML presentations with a built-in browser editor: drag objects, resize blocks, edit text, reorder slides, save locally, and export clean standalone HTML or print-quality PDF.

> **本版本 (dora-dotcom/frontend-slides-editable)** Fork 自 [archlizheng/frontend-slides-editable](https://github.com/archlizheng/frontend-slides-editable)，在原有编辑运行时基础上新增：高质量 Export PDF（固定像素注入方案）、图片上传与背景替换、自适应发现流程（Context Scan）、Design System 自动检测。
>
> **This fork (dora-dotcom/frontend-slides-editable)** is based on [archlizheng/frontend-slides-editable](https://github.com/archlizheng/frontend-slides-editable) with additions: high-quality Export PDF (fixed-px injection, no scaling), image upload + background replace, adaptive Context Scan discovery flow, and design system auto-detection.

## 这个 Skill 是做什么的 / What This Does

**Frontend Slides - Editable** 是 **frontend-slides** 的可编辑分支。它保留了原始 skill 的风格探索流程、视口适配规则和 PPT 转换能力，并在此基础上加入完整的浏览器内编辑运行时。**交付用的幻灯片仍应按 `STYLE_PRESETS.md` 实现各预设的布局与签名元素**；可编辑只是增加运行时，不是把多套风格压成同一套版式原型。

**Frontend Slides - Editable** is the editable fork of **frontend-slides**. It preserves style discovery, viewport discipline, and PPT conversion from the original skill, then adds a full in-browser editing runtime. **Real decks should still implement each preset's layout and signature elements from `STYLE_PRESETS.md`** — edit mode is an add-on, not permission to reuse one generic slide prototype for every aesthetic.

它适合"生成后还要继续改"的场景：

It is designed for workflows where the generated output must remain editable:

- 直接在幻灯片上移动对象、调整大小、编辑文本
- 使用 **Ctrl+点击** 多选，吸附对齐其他对象或幻灯片中心
- 使用 **Undo / Redo** 撤销任意操作
- 在 **Pages** 侧栏重排或删除页面
- 上传图片到幻灯片，或替换背景图
- 将完整 deck 结构保存到 `localStorage`，或导出独立 HTML / PDF

- move, resize, and edit text directly on slides
- use **Ctrl+click** multi-select with snap alignment
- use **Undo / Redo** for any operation
- reorder and delete slides from the **Pages** sidebar
- upload images or replace slide backgrounds
- persist to `localStorage`, or export standalone HTML / PDF

如果只需要更轻量的只读输出，请使用父 skill **frontend-slides**。

If you only need the smallest read-only output, use the parent **frontend-slides** skill.

## 本版本新增 / What's New in This Fork

| 功能 | 说明 |
|------|------|
| **Export PDF（高质量）** | 固定像素注入方案，不使用 CSS transform 缩放。浏览器以目标分辨率（16:9 / 4:3）原生渲染，无模糊、无色彩损失 |
| **多页 PDF** | 多 slide deck 自动循环生成，每页对应一个 `@page` 打印页 |
| **图片上传** | 侧边栏 **＋ Add Image** 上传图片对象到当前幻灯片；双击图片对象可替换 |
| **背景替换** | 编辑模式下悬停背景区域，点击 **📷 Replace background** 上传新背景图，支持 Undo |
| **Context Scan（自适应发现）** | 在提问前先扫描已有上下文，只问真正缺失的信息；全部已知则直接生成 |
| **Design System 自动检测** | 检测到 `design.md` / `brand.md` / `tokens.json` 等文件时，自动跳过风格选择阶段 |
| **Agent 调用优化** | Agent 或自动化流程调用时不重复询问上下文已有的信息 |
| **字号连续调节** | 富文本工具栏改为 A−/A+ 步进按钮（±1px），取代 S/M/L/XL 固定档位，可无限精确调节 |

| Feature | Description |
|------|------|
| **Export PDF (high quality)** | Fixed-px injection — no CSS transform scaling. Browser renders at target resolution (16:9 / 4:3) natively; no blur, no color loss |
| **Multi-slide PDF** | Multi-slide decks loop through all slides, producing one `@page` per slide |
| **Image upload** | Sidebar **＋ Add Image** uploads a new image object to the current slide; double-click any graphic to replace it |
| **Background replace** | Hover background in edit mode → **📷 Replace background** → upload new image; supports Undo |
| **Context Scan (adaptive discovery)** | Scans existing context before asking questions; skips phases when information is already known; generates directly if all 5 essentials are covered |
| **Design System auto-detection** | Detects `design.md` / `brand.md` / `tokens.json` etc. and skips style selection entirely |
| **Agent invocation support** | When called by an agent, does not re-ask what the invoking context already knows |
| **Continuous font size (A−/A+)** | Toolbar replaces S/M/L/XL presets with step buttons: each click reads computed `px` size and adjusts ±1px with full undo/redo support |

## Skill 对照表 / Skill Comparison

| 维度 / Dimension | `frontend-slides` | `frontend-slides-editable` |
|------|------|------|
| 核心定位 / Primary job | 生成更轻量的只读 HTML 演示 | 生成可继续编辑的 HTML 演示 |
| 输出重量 / Output weight | 更小、更干净 | 更重，但包含完整编辑器 |
| 浏览器内编辑 / In-browser editing | 可选文本编辑 | 默认完整编辑运行时 |
| 页面管理 / Slide management | 无 Pages 侧栏 | 有缩略图侧栏、重排、删除 |
| 对象操作 / Object manipulation | 不支持对象级拖拽缩放 | 拖拽、缩放、吸附、多选 |
| 历史记录 / Undo and redo | 无 | 内置 Undo / Redo |
| 导出 PDF / Export PDF | 无 | 固定像素原生渲染，高质量 |
| 图片上传 / Image upload | 无 | 侧边栏上传 + 双击替换 |
| 背景替换 / Background replace | 无 | 支持，含 Undo |
| Design System 检测 | 无 | 自动检测，跳过风格阶段 |
| 适合场景 / Best for | 交付成品、体积敏感、只读展示 | 评审后继续改稿、团队协作、客户反馈迭代 |

## 核心特性 / Key Features

- **零依赖**：单个 HTML 文件，CSS/JS 内联，无需 npm、构建工具或框架
- **自适应发现流程**：Context Scan 扫描已有上下文，只问缺失信息；支持 Design System 自动检测
- **可视化风格探索**：通过预览选风格，而不是抽象描述
- **完整可编辑运行时**：拖拽、缩放、文本格式化、缩略图侧栏和历史记录
- **PPT 转换**：将 `.pptx` 转为可编辑网页幻灯片并保留资源
- **视口安全**：每一页都要求适配视口，不允许内部滚动
- **持久化与导出**：`Ctrl+S` 保存结构化状态；Export HTML 剥离临时编辑态；Export PDF 固定像素原生渲染（16:9 / 4:3）
- **图片支持**：侧边栏 ＋ Add Image 上传图片对象；双击图片对象可替换；支持背景图替换（含 Undo）
- **反模板感**：通过精选风格预设，避免千篇一律

- **Zero dependencies**: Single-file HTML with inline CSS/JS, no npm/build/framework
- **Adaptive discovery**: Context Scan scores known essentials and skips phases; design system auto-detected
- **Visual style discovery**: pick by preview, not design jargon
- **Full editable runtime**: drag/resize/text formatting/filmstrip/history included
- **PPT conversion**: convert `.pptx` into editable web slides with preserved assets
- **Viewport-safe output**: every slide must fit the viewport without internal scrolling
- **Persistence + export**: `Ctrl+S` saves structure; Export HTML strips edit state; Export PDF fixed-px native render (16:9 or 4:3), no quality loss
- **Image support**: sidebar ＋ Add Image uploads image object; double-click graphic to replace; background replacement with Undo
- **Anti-generic aesthetics**: curated presets over bland default templates

## 安装 / Installation

```bash
# Claude Code
cp -r frontend-slides-editable ~/.claude/skills/

# Codex
cp -r frontend-slides-editable ~/.codex/skills/
```

然后调用 / Then invoke:

```text
/frontend-slides-editable
```

## 用法 / Usage

### 新建可编辑演示 / Create a new editable presentation

```text
/frontend-slides-editable

> "帮我做一个关于 AI agents for product teams 的分享"
```

这个 skill 会先执行 **Context Scan**：扫描对话上下文与工作目录，判断已经知道哪些信息（目的、页数、内容、风格、图片），只询问真正缺失的部分。如果检测到 `design.md` / `brand.md` / `tokens.json` 等 design system 文件，将自动跳过风格选择阶段。

The skill runs a **Context Scan** first: it checks conversation context and the working directory to score what's already known (purpose, length, content, style, images), then asks only for genuinely missing information. If a design system file (`design.md`, `brand.md`, `tokens.json`, etc.) is detected, style selection is skipped entirely.

### 增强现有 HTML / Enhance an existing HTML deck

```text
/frontend-slides-editable

> "Improve this HTML deck and keep it editable"
```

Skill 会读取现有演示、检查密度与视口适配、保护编辑运行时契约，在保持编辑/持久化/导出能力的前提下更新 deck。

### 转换 PowerPoint / Convert a PowerPoint

```text
/frontend-slides-editable

> "Convert presentation.pptx into an editable web slideshow"
```

提取 PPT 文字、图片和备注 → 确认结构 → 询问风格偏好（或使用 design system）→ 生成可编辑 HTML deck。

## 编辑体验 / Editing Experience

生成后的 deck 默认包含：

Generated decks include:

- **编辑模式 / Edit mode**：按 `E` 或从左上角悬停呼出控件
- **Pages 侧栏 / Pages sidebar**：缩略图导航、重排、删除
- **对象编辑 / Object editing**：用 **⠿** 拖动，角点缩放，吸附线对齐幻灯片中心与其他对象
- **富文本工具栏 / Rich text toolbar**：**粗体/斜体/字体**，字号用 **A− / A+** 步进（±1px，无上限，含 Undo）
- **历史记录 / History**：`Ctrl+Z`、`Ctrl+Y`、`Ctrl+Shift+Z` 及 macOS 等价键
- **持久化 / Persistence**：`Ctrl+S` 保存完整 `.slides-offset` 到 `localStorage`
- **Export HTML**：下载不含临时编辑态与选中态类名的干净 `.html`
- **Export PDF**：侧边栏选择 16:9 或 4:3，固定像素注入方案，在新标签页原生渲染并自动打印 — 无模糊无色彩损失
- **图片上传 / Image upload**：侧边栏 **＋ Add Image** 上传图片到当前幻灯片；双击图片对象可替换
- **背景替换 / Background replace**：编辑模式下悬停幻灯片背景区域，点击 **📷 Replace background** 上传新背景图

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
| `editor-runtime.md` | 运行时 DOM 契约、Export PDF 方案、检查项 / Runtime DOM contracts, Export PDF, checklist |
| `examples/editable-deck-reference.html` | 标准参考实现 / Canonical runtime reference |
| `STYLE_PRESETS.md` | 12 个精选风格 / 12 curated style presets |
| `viewport-base.css` | 视口适配基础样式 / Viewport-fit base CSS |
| `html-template.md` | HTML 基础结构说明 / Base HTML integration notes |
| `animation-patterns.md` | 动画参考 / CSS/JS animation reference |
| `scripts/extract-pptx.py` | PPT 内容提取脚本 / PPT extraction script |

## 架构说明 / Architecture

运行时有几个不可破坏的约束：

The runtime depends on non-negotiable contracts:

- 每页必须是带稳定 `id` 的 `section.slide`
- 可移动内容位于 `.slide-edit-layer`，可编辑块使用 `[data-slide-object][data-oid]`
- 页面枚举必须限定真实 deck 根（`.slides-offset :scope > section.slide`），不能包含缩略图克隆
- Export PDF 必须使用固定像素注入方案，不得使用 `transform: scale()`

- each slide is a `section.slide` with stable `id`
- movable content lives in `.slide-edit-layer` as `[data-slide-object][data-oid]`
- slide enumeration must stay scoped to the true deck root, never include sidebar thumbnail clones
- Export PDF must use fixed-px injection — never `transform: scale()`

## 设计理念 / Philosophy

1. **通过"看见选项"建立审美。** 风格预览比抽象问卷更有效。
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

## 致谢 / Credits

本版本 Fork 自 [@archlizheng](https://github.com/archlizheng/frontend-slides-editable) 的 **frontend-slides-editable**，在其可编辑运行时基础上新增 Export PDF 高质量方案、图片支持、自适应发现流程与 Design System 自动检测。

原始 **frontend-slides** 由 [@zarazhangrui](https://github.com/zarazhangrui/frontend-slides) 创建。

This fork builds on **frontend-slides-editable** by [@archlizheng](https://github.com/archlizheng/frontend-slides-editable), adding high-quality Export PDF, image support, adaptive Context Scan discovery, and design system auto-detection.

Original **frontend-slides** by [@zarazhangrui](https://github.com/zarazhangrui/frontend-slides).

## 许可证 / License

MIT（与上游项目一致）。

MIT (same as upstream).
