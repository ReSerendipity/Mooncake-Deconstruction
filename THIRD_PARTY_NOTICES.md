# 第三方源码与许可证声明（Third Party Notices）

本文件登记**随本仓库分发的第三方代码**。本仓自研内容（演示页、脚本、截图）为 Apache-2.0，见根目录 [`LICENSE`](LICENSE)（11,344 B）。

文中「逐字节相同」= 两侧文件的 git blob SHA 相等（SHA 按内容寻址，相等即字节相等）。

登记基准：`Mooncake-Deconstruction @ ef01d991658717513fd105f5ace084d833e110f3`（该 ref 共 48 个 blob）——下文所有「逐字节相同」的比对与体积数字都是在这份文件树上做的。

台账复核：当前 `main` tip 为 `a6c941e6697b3aac206a09c5c47bff1355a66da7`（49 个 blob）。`compare/ef01d99…a6c941e` 的差集只有本文件自身，因此上述比对对象在当前 tip 上字节未变，无需重验。

最后核验日期：2026-10-12（`git/trees?recursive=1` 复算 blob 数与 `post-assets/` 文件数，`truncated=false`）。

---

## 一、three.js r160 — **MIT**（本仓唯一的第三方代码）

### 1.1 三处本地载体

| 本仓路径 | 字节数 | 归属证据 |
|---|---|---|
| `three.module.local.js` | 1,272,972 | 文件第 2–4 行自带许可证头（见下），第 6 行 `const REVISION = '160';` |
| `addons/controls/OrbitControls.js` | 29,868 | 自身**无**许可证头（上游 r160 同文件第 1 行即 `import {`）⇒ 适用包级 LICENSE |
| `addons/environments/RoomEnvironment.js` | 3,735 | 自身**无**许可证头，第 1–3 行为来源注释 ⇒ 见 §1.3 双记 |

`three.module.local.js` 第 1–6 行逐字：

```
/**
 * @license
 * Copyright 2010-2023 Three.js Authors
 * SPDX-License-Identifier: MIT
 */
const REVISION = '160';
```

### 1.2 版本与完整性

- 名称：three.js　版本：**r160**（直读 `REVISION = '160'` 字面量，非按体积或日期推断）
- 上游：`mrdoob/three.js` 的 **`r160` tag**，包级 `LICENSE` 1,081 B，前 3 行逐字：
  `The MIT License` / （空行） / `Copyright © 2010-2023 three.js authors`
- 两个 addon 与上游 r160 的对应文件**逐字节相同**：
  - `addons/controls/OrbitControls.js` ≡ `examples/jsm/controls/OrbitControls.js`（blob SHA `f29e7feb0f…`）
  - `addons/environments/RoomEnvironment.js` ≡ `examples/jsm/environments/RoomEnvironment.js`（blob SHA `f51f72b229…`）
  ⇒ 本仓未对 three.js 做任何修改，是原样发行物。
- ⚠️ 措辞差异是**有意的**：文件头写 `Copyright 2010-2023 Three.js Authors`，包级 LICENSE 写 `Copyright © 2010-2023 three.js authors`。两处都是 MIT，本文件各引各的原文，不做统一。

### 1.3 `RoomEnvironment.js` 的双许可证登记

该文件第 1–3 行逐字：

```
/**
 * https://github.com/google/model-viewer/blob/master/packages/model-viewer/src/three-components/EnvironmentScene.ts
 */
```

即其内容原型来自 **`google/model-viewer`**（许可证 **Apache-2.0**，其仓 `LICENSE` 11,358 B；源文件头部为 `Copyright 2021 Google LLC. All Rights Reserved.` / `Licensed under the Apache License, Version 2.0`），随后由 three.js 侧改写并作为 MIT 发行物发布。

本文件对这一个文件**同时登记两条**，各写清覆盖范围：

- 本仓这份副本**是** three.js r160 的发行物 ⇒ **MIT**（Copyright 2010-2023 Three.js Authors）；
- 其内容原型来自 google/model-viewer ⇒ **Apache-2.0**（Copyright 2021 Google LLC）。

这不是"二选一"的裁断，而是两层事实并列：任何一侧的归属声明都不会被漏掉。

### 1.4 同一依赖的第二份载体：CDN 引用

`demo-C3-月饼3D.html:126-129` 的 importmap：

```
  "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
  "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
```

即同一个 three.js 在本仓**既有本地副本、又有 CDN 引用**两种载体。当前两侧版本一致（`0.160.0` / r160）。
访问者经 CDN 加载时，three.js 由 unpkg 直接分发，本仓不承担该份的再分发；本仓承担的是 §1.1 那三份本地文件的分发义务。

---

## 二、MIT License（three.js 适用条款全文）

以下为 `mrdoob/three.js` 的 `r160` 包级 `LICENSE`（1,081 B）逐字：

```
The MIT License

Copyright © 2010-2023 three.js authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

`RoomEnvironment.js` 的 Apache-2.0 原型侧条款见 <https://www.apache.org/licenses/LICENSE-2.0>；本仓根目录 `LICENSE`（11,344 B）即同一份 Apache-2.0 全文，随本文件一同分发。

---

## 三、素材与自产内容

| 素材 | 来源 | 状态 |
|---|---|---|
| `post-assets/` 18 个文件（16 张 `.png` + 2 个 `.gif`：`explode-custard.gif`、`explode-custard-sm.gif`） | 自产展示截图与封面 | 随本仓 Apache-2.0 分发；仅作展示，可替换重拍 |
| 程序化月饼纹样（回纹 / 卷草 / 祥云 / 中心开光汉印） | 代码内程序化生成，非位图素材 | 自产 |
| 字体 | 仓内**无自带字体文件**，页面使用系统字体 | 不涉及分发 |
| `demo-C3-月饼3D.html:137-138` 内嵌 base64 顶面贴图 | **出处未记录**：注释自述"由真实广式月饼俯拍照片处理而来"，原照片的拍摄者与授权均无记录 | **UNKNOWN**，见下 |

关于内嵌实拍贴图：该贴图**默认不启用**（`demo-C3-月饼3D.html:150-152`，仅当 URL 带 `?phototop=1` 时才加载），
但只要它留在文件里，就是随本仓库分发的一份第三方素材副本。
在补上出处之前，本文件不声称它可商用；如需对外商用，请补充摄影者授权或将其移除/替换为程序化贴图。

---

## 四、义务清单（给后续改动的自己看）

1. `three.module.local.js` 第 1–5 行的 `@license` 头**不得删除**；若日后升级 three.js 版本，需同步更新 §1.1 的 `REVISION` 与 §1.4 的 CDN 版本号，并重新核对两处是否仍一致。
2. 若把 `addons/` 下的两个文件换成修改版，需按 Apache/MIT 标注修改（当前是原样发行物，无此义务）。
3. 若移除内嵌实拍贴图，本文件 §三 对应行要一并删除。
4. **ThreeUI spark-badge 改编块的归属注释（`demo-C4-月饼3D-组件拆解增强.html` 内）不得删除**，见 §五；删除该粒子氛围功能时应一并删除本登记。

---

## 五、ThreeUI spark-badge 改编（**MIT**，2026-10-28 登记）

### 5.1 载体与归属证据

| 项 | 值 |
|---|---|
| 上游仓库 | `MengTo/threeui` @ `main`，路径 `src/shaders/spark-badge/spark-badge.html` |
| 上游许可 | **MIT**：仓库根 `LICENSE` 1,064 B，首行 `MIT License`，`Copyright (c) 2026 Meng To`（2026-10-28 经 `raw.githubusercontent.com` 直取核验） |
| 上游文件字节 | 38,119（同一次 raw 直取） |
| 本项目载体 | `demo-C4-月饼3D-组件拆解增强.html` 内经典 `<script>` 块「金色流萤 · 背景粒子氛围」 |
| 改编块体积 | 约 8.5 KB（含注释） |

### 5.2 改编说明（保留 / 删除 / 变更）

- **保留**：`mulberry32` 随机数、可平铺 curl 噪声场（`makeCurlField` / `curlSample` / `curlAt`）、粒子 tick 运动模糊渲染（短线段沿运动方向）。
- **删除**：原"徽章图形"整套（`buildMasks` / `buildEmitters` 及 badge/浏览器/iPhone/显示器四个变体的图形雕刻），以及雨丝（rain）、水纹（water）两个子系统——本项目只需氛围，不需要图形轮廓。
- **变更**：颜色白 → 金色系 4 色；粒子密度下调至面积自适应 700–3200（上游 17,600 余烬）；绘制区域由整页主画布改为 `position:fixed` 透明背景层；新增 `prefers-reduced-motion` 降速、`?noparts=1` / `?static=1` 禁用、弱机自动停止（`window.__dustCtl.stop()`）。

### 5.3 义务

MIT 允许使用/修改/再分发，要求保留版权与许可声明。本项目以代码内注释保留出处与许可；本登记随仓库分发。删除该功能时同步删除 §四.4 与本登记。

---

## §六 demo-C5「解构秀」第三方依赖与借鉴登记

### 6.1 结论

**demo-C5 未引入任何新的第三方代码文件。** 其 UI 壳、滚动驱动拆解（scroll-scrub）、镜头推移、胶片颗粒/光标光晕/滚动显现质感层均为本项目原创实现；仅**借鉴**了样品站的展示范式（非代码）：全屏电影感舞台、scroll-linked 章节、爆炸装配图开篇、玻璃拟态 HUD、状态循环徽标。借鉴行为不产生版权义务，故本登记仅作溯源说明。

### 6.2 样品溯源（2026-10-28 实地访问）

| 样品站 | 访问入口 | 借鉴点 |
|---|---|---|
| ThreeUI | threeui.com/browse/tag/3d（280 个 3D 组件） | 爆炸装配图开篇 · scroll-linked act · 编辑式产品叙事 · 玻璃 HUD · 状态循环徽标 |
| Refero | doc.refero.design / llms.txt | 设计规格纪律（字体/间距/圆角/阴影归零的免费档口径） |
| Inspora | inspora.site（直连失败，沿用此前搜索所得） | paper-fold 逐层交错 · progressive-blur 渐进模糊 |
| Awwwards / Jiro / MotionSites | awwwards.com · jiro.build · motionsites.ai | 展示纪律/规格（免费档为提示词库，无源码资产，仅取审美口径） |

### 6.3 与 C4 的关系

demo-C5 基于 demo-C4 的全部 Three.js 建模、标注/摘取/检视交互与数值自检契约（`?static=1&verifyall=1`、`__jumpState/__pickPart/__partCount/__clearPick`），仅重做展示壳与叙事层。C4 的 ThreeUI 粒子改编登记（§四/§五）随代码一并继承。

---

## §七 demo-C5「单文件离线版」内嵌依赖登记

### 7.1 说明

`demo-C5-月饼3D-解构秀-单文件.html`（约 1.8 MB）将 three.js 运行时与两个 addons **内嵌为单个 HTML**，双击打开即用、零网络依赖（无 CDN、无 importmap）。内嵌源码的版权头随代码保留。

### 7.2 内嵌清单（全部 MIT，均保留原始版权注释）

| 模块 | 来源 | 版本 | 说明 |
|---|---|---|---|
| three.module.js | three.js 官方 build（MIT，`Copyright 2010-2023 Three.js Authors`） | r160 | 全文内嵌；仅新增 `const THREE = { 416 导出符号 }` 命名空间桥接 |
| OrbitControls.js | three.js `examples/jsm/controls/`（MIT） | r160 | 去除 import 行，export 改为 IIFE 返回值 |
| RoomEnvironment.js | three.js `examples/jsm/environments/`（MIT） | r160 | 同上 |

### 7.3 改造方法（可复现）

1. 删除页面 importmap 与主逻辑三个 import（`THREE` / `OrbitControls` / `RoomEnvironment`）。
2. 依次内联 three.module.js 全文 → `const THREE = {…}`（从尾部 `export {}` 解析 416 符号）→ 两个 addons（去 import、export 改 return，包进 IIFE 隔离作用域）→ 主逻辑（包进 IIFE 隔离，避免与 three 打包短名如 `_v3` 撞名）。
3. 验证：`file://` 协议下 `?static=1&verifyall=1` → 14/14 ALL-OK、console 0 错误。
