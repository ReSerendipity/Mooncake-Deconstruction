# 发布 / 回滚 规范（Mooncake-Deconstruction）

> **来源与权威**：公共条款见 `ReSerendipity/.github` 的 `REPOSITORY_GUIDELINES.md` §10（发布 / 分发统一规范）。
> 本文件按账号统一模板 `RELEASE_GOVERNANCE_TEMPLATE.md` 收敛，只填**本仓特有**内容，不重写、不抵触 §10 的公共条款。
> 生成日期：2026-10-18（工单 C-09）。

---

## 0. 远端优先（根原则，不可改写）

发布链的构建、打包、扫描、上传、推送**全部在 GitHub Actions 远端完成**；本地只做三件事：改版本位、落 CHANGELOG、`git tag` + `git push`。本地不执行打包 / 镜像构建 / 发布上传。

本仓当前唯一的远端动作是 **GitHub Pages 部署**（`.github/workflows/pages.yml`，push 到 `main` 触发），构建与部署均在 runner 完成，符合「远端优先」。本地不产出任何站点交付物——`_site/` 临时目录由远端 runner 现场拼装。

## 1. 版本号规范

- 遵循 **SemVer** `MAJOR.MINOR.PATCH`；预发布用 `-alpha.N` / `-beta.N` / `-rc.N`。
- **唯一权威版本位**：**暂无**。本仓为零构建静态站，无 `package.json` / `pyproject.toml` / `config.yaml` 等版本声明文件，历史上也未打过任何 SemVer tag（`git tag` 为空）。版本位引入方式与首个版本号**待定（负责人 + 触发条件）**。
- 必须同步的其它版本位：无（暂无版本位，故无多点同步清单）。
- 版本位漂移校验入口：暂无（暂无版本位，无需一致性校验脚本；待引入版本位时，参照 TTS-MultiModel `tests/test_version_consistency.py` 建立，漂一处即判红）——**待定（负责人 + 触发条件）**。
- 自动化方式：手动 tag（人工）。当前无 release-please，亦无任何 release workflow；一旦出现可分发产物，按 §3 / §4 建 tag 驱动链。

## 2. CHANGELOG 管理

- 遵循 **Keep a Changelog**：`Added / Changed / Fixed / Deprecated / Removed / Security`。
- 每次合并 `main` 在 `[Unreleased]` 追加；type 映射 `feat→Added`、`fix→Fixed`、`refactor→Changed`。
- 发版时 `[Unreleased]` → `[VERSION] - YYYY-MM-DD`。
- **现状说明**：本仓已建立根级 `CHANGELOG.md`（2026-10-18 随 `ci/changelog` PR 落地，原 §10.6 欠账随之消除）。当前尚无 tag / Release，版本化发布尚未建立，`[Unreleased]` 按 Keep a Changelog 维护；首个版本号与发版日期仍待定（见 §1）。

## 3. 发布流程（远端）

> 本仓当前**无 tag 驱动的 release 链**（判断依据见 §4）。本节为一旦出现可分发产物时的标准流程占位，当前不实际执行。

1. 确认 `[Unreleased]` 条目完整
2. 同步版本位（见 §1 清单）
3. 本地打 tag 并推送：`git tag v<X.Y.Z>` → `git push origin v<X.Y.Z>`
4. 远端凭 tag 触发 `release.yml` 构建产物
5. 远端建 **draft Release** 并挂资产 → 人工审核后 `published`
6. 盯到终态：`gh run list` 确认绿；红了当场修或 revert 止损

当前实际对外发布路径仅为：push `main` → 远端 `pages.yml` 构建静态站 → GitHub Pages 发布（<https://reserendipity.github.io/Mooncake-Deconstruction/>）。此路径不打 tag、不产 Release 资产。

## 4. 分发产物与完整性

### 4.1 本仓发布链判断（本工单核心决定）

**决定：暂无发布产物，发布链待需要时再建。本工单不新建 `release.yml`、不挂 `SHA256SUMS`。**

判断依据（逐项排除 §10.3 的可分发产物形态）：

| 可分发形态 | 本仓是否具备 | 证据 |
|---|---|---|
| Python wheel / sdist | 否 | 无 `pyproject.toml` / `setup.py` / `setup.cfg`；`requirements.txt` 仅钉住无头验证工具链（`playwright==1.48.0`、`Pillow==10.4.0`），属开发/测试依赖，不作为分发包发布 |
| 容器镜像（ghcr） | 否 | 无 `Dockerfile`，无 `docker/build-push-action`，无镜像推送 workflow |
| 桌面 / 移动安装包（Tauri / NSIS / APK） | 否 | 无 `src-tauri/` / 打包工程 / 移动工程 |
| npm 包 | 否 | 无 `package.json` |

本仓唯一对外交付物是 **GitHub Pages 静态站点**（`index.html` + `demo-C2-月饼解构.html` + `demo-C3-月饼3D.html`，外加 `three.module.local.js` / `addons/` / `post-assets/` 等随仓文件）。它由 `.github/workflows/pages.yml` 在 push `main` 时于远端拼装部署，属 §10.4「远端侧部署」——**不产生可下载的 Release 资产**，因此不需要 tag 驱动的 `release.yml`，也不需要 `SHA256SUMS.txt`。

> 后续若本仓开始发布可下载产物（例如把 demo 单文件打包为离线 zip、或上架 npm 包），再按 §3 建最小 tag 驱动发布链：`push: tags: v*` 触发 `release.yml`，远端构建并在 draft Release 挂资产 + `SHA256SUMS.txt`，人工审核后 published。

### 4.2 完整性与签名

- 当前无 Release 资产，故无 `SHA256SUMS.txt` 产物。
- **不使用 GPG 分离签名**（2026-10-18 裁决撤掉，见 §10.6）；本仓亦无任何 `gpg-signed-release.yml`。
- 站点本身的静态完整性由 CI 兜底：`.github/workflows/ci.yml` 的 `integrity` 作业校验 `demo-C2` / `demo-C3` / `three.module.local.js` / `README.md` 存在且非空。
- 不以 floating `latest` 作任何发布基线（本仓无镜像、无包，本条款当前不适用；未来引入镜像时遵守 §10.3）。
- Trivy 扫描 / provenance / SBOM：当前无容器镜像，不适用；未来引入镜像时按 §10.4 阻断式扫描 + `provenance: true` + `sbom: true`。

## 5. 回滚

- **判定**（满足任一即触发）：Pages 站点上线后核心 demo 白屏 / 交互断言失败 / 语法门禁红。具体 SLO 阈值**待定（负责人 + 触发条件）**。
- **执行**：本仓为静态站，无不可变产物可重推；回滚以 `git revert <bad-commit>` 为主（保历史、可再 forward），push `main` 后由 `pages.yml` 自动重部署上一版。
- **破坏性动作**：重指向 / 删除 tag、移动任何远端 ref → **须仓库所有者单独授权**（当前无 tag，此条为预先声明）。
- **回滚后验证**：
  1. `node tools/check_html_scripts.js demo-C2-月饼解构.html demo-C3-月饼3D.html`（CI 同款语法门禁）；
  2. 无头全量断言：`python _mkverify.py` → `python -m http.server 8931` → `python _verify_run.py "http://127.0.0.1:8931/_verify-c3.html?static=1&verifyall=1"`（7 类型 × 合拢/展开共 14 组状态）；
  3. 线上 Pages 地址冒烟可访问。

## 6. SLA / 错误预算

- 目标可用性：静态展示站，无业务 SLA 承诺；参照性目标 <99.5%/月 ⇒ 错误预算 ≈3.6h/月。超出即冻结非紧急发布并复盘。**正式 SLO 待定（负责人 + 触发条件）**。

## 7. 发布前检查清单

- [ ] 版本位全部同步（见 §1 清单）——当前无版本位，N/A
- [ ] CHANGELOG `[Unreleased]` 已改版本 + 日期（见 §2）
- [ ] `node tools/check_html_scripts.js demo-C2-月饼解构.html demo-C3-月饼3D.html` 通过（CI `syntax` 作业）
- [ ] CI `integrity` 作业通过（demo 文件 / `three.module.local.js` / `README.md` 存在非空）
- [ ] 镜像类仓：Trivy 阻断通过，豁免已在 `.trivyignore.yaml` 登记理由 + expiration——本仓无镜像，N/A
- [ ] 镜像类仓：`provenance: true` + `sbom: true` 已开——本仓无镜像，N/A
- [ ] **本地未产出任何发布交付物**（全部远端构建）——本仓交付物即 Pages 站，由远端 runner 拼装，符合

---

## 差异点采集清单（本仓取值）

| 占位符 | 采集来源 | 本仓取值 |
|---|---|---|
| 版本位文件与字段 | 仓内版本声明 | 无（零构建静态站，无 package.json/pyproject.toml/config.yaml；无 tag） |
| 其它需同步版本位 | `grep -rn` 版本串 | 无 |
| 版本一致性校验入口 | `tests/**` | 无（待定：负责人 + 触发条件） |
| 自动化方式 | `.github/workflows/` | 手动 tag（人工）；当前无 release-please、无 release workflow |
| 发布 workflow 文件名 | `.github/workflows/` | 无 release.yml；部署为 `pages.yml`（push main 触发 Pages） |
| 产物形态与标签规则 | 构建 workflow | 无 Release 产物；Pages 站不可变 URL，不打 tag |
| 完整性手段 | Release 资产清单 | 无 Release 资产；CI 静态完整性校验兜底；无 GPG |
| 回滚判定阈值 | 运行手册 / 监控 | 待定（负责人 + 触发条件） |
| 回滚后验证命令 | `tests/smoke` 等 | `node tools/check_html_scripts.js ...` + `_verify_run.py ?verifyall=1` 14 组断言 |
| 技术栈 | 静态站 | 纯 HTML + Three.js（CDN importmap + 本地 vendor `three.module.local.js`），零构建 |
| 部署目标 | Pages workflow | GitHub Pages（`pages.yml`） |

## 禁止事项

- 不重写 §10 的公共条款（远端优先、tag 驱动、版本位一致、不可变标签、扫描阻断、无 GPG）。
- 不引入 `latest` 作发布基线；不保留或新建 GPG 签名流程。
- 不留空占位符；未确定项已标注「待定（负责人 + 触发条件）」，不编造阈值。