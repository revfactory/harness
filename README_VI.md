<p align="center">
  <img src="harness_banner.png" alt="Harness Banner" width="600">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.2.0-brightgreen.svg" alt="Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-purple.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Patterns-6_Architectures-orange.svg" alt="6 Architecture Patterns">
  <img src="https://img.shields.io/badge/Mode-Agent_Teams-green.svg" alt="Agent Teams">
  <a href="https://github.com/revfactory/harness/stargazers"><img src="https://img.shields.io/github/stars/revfactory/harness?style=social" alt="GitHub Stars"></a>
</p>

<p align="center">
  <a href="#category--where-harness-sits"><img src="https://img.shields.io/badge/Layer-L3%20Meta--Factory-orange" alt="Layer"></a>
  <a href="#category--where-harness-sits"><img src="https://img.shields.io/badge/Sub--layer-Team--Architecture%20Factory-teal" alt="Sub-layer"></a>
  <a href="#"><img src="https://img.shields.io/badge/README-EN%20%7C%20KO%20%7C%20JA-lightgrey" alt="i18n"></a>
</p>

# Harness — Nhà máy Kiến trúc Đội cho Claude Code

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | **Tiếng Việt**

> **Harness là một nhà máy kiến trúc đội (team-architecture factory) cho Claude Code.** Chỉ cần nói **"build a harness for this project"** (English), **"하네스 구성해줘"** (한국어), **"ハーネスを構成して"** (日本語), hoặc **"xây dựng harness cho dự án này"** (Tiếng Việt), plugin sẽ chuyển mô tả lĩnh vực (domain) của bạn thành một đội agent cùng các skill mà chúng sử dụng — được chọn từ sáu mẫu kiến trúc đội (team-architecture pattern) đã được định nghĩa sẵn.

## Tổng quan

Harness tận dụng hệ thống Agent Teams của Claude Code để phân rã các nhiệm vụ phức tạp thành các đội agent chuyên biệt được điều phối với nhau. Chỉ cần nói "build a harness for this project" (xây dựng harness cho dự án này), hệ thống sẽ tự động sinh ra các định nghĩa agent (`.claude/agents/`) và skill (`.claude/skills/`) phù hợp với lĩnh vực của bạn.

## Phân loại — Vị trí của Harness

Harness nằm ở tầng **L3 Meta-Factory** trong hệ sinh thái Claude Code — tầng chuyên sinh ra các harness khác, thay vì là một harness đơn lẻ. Trong L3, chúng tôi chọn một tầng con cụ thể: **Nhà máy Kiến trúc Đội (Team-Architecture Factory)**.

| Tầng | Chức năng | Hàng xóm cùng tồn tại |
|-------|--------------|---------------------------|
| **L3 — Meta-Factory / Nhà máy Kiến trúc Đội** (chúng tôi) | Câu mô tả lĩnh vực → đội agent + skill, qua 6 mẫu đội đã định nghĩa sẵn | — |
| L3 — Meta-Factory / Nhà máy Cấu hình Runtime | Cấu hình runtime tất định, có thể lặp lại | [coleam00/Archon](https://github.com/coleam00/Archon) |
| L3 — Meta-Factory / Codex Runtime Port | Cùng khái niệm, chạy trên Codex runtime | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | Chuẩn hóa skill/rule/hook giữa nhiều harness | [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) |

> Archon sinh ra các cấu hình runtime tất định. Harness sinh ra kiến trúc đội (pipeline, fan-out/fan-in, expert pool, producer-reviewer, supervisor, hierarchical delegation) cùng các skill mà agent sử dụng. Đây là hai tầng con khác nhau của cùng tầng L3. Chọn Archon nếu cần tính tất định của runtime, chọn Harness nếu cần kiến trúc đội, hoặc kết hợp cả hai.

## Lịch sử Star

<a href="https://www.star-history.com/?repos=revfactory%2Fharness&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
 </picture>
</a>


## Tính năng chính

- **Thiết kế đội agent** — 6 mẫu kiến trúc: Pipeline, Fan-out/Fan-in, Expert Pool (Nhóm chuyên gia), Producer-Reviewer (Sản xuất-Kiểm duyệt), Supervisor (Giám sát viên), và Hierarchical Delegation (Ủy quyền phân cấp)
- **Sinh skill** — Tự động sinh skill với Progressive Disclosure để quản lý cửa sổ ngữ cảnh hiệu quả
- **Điều phối** — Truyền dữ liệu liên-agent, xử lý lỗi, và các giao thức điều phối đội
- **Kiểm định** — Kiểm tra trigger, dry-run testing, và các bài kiểm tra so sánh có-skill và không-skill


## Quy trình

```
Giai đoạn 1: Phân tích lĩnh vực
    ↓
Giai đoạn 2: Thiết kế kiến trúc đội (Agent Teams vs Subagents)
    ↓
Giai đoạn 3: Sinh định nghĩa agent (.claude/agents/)
    ↓
Giai đoạn 4: Sinh skill (.claude/skills/)
    ↓
Giai đoạn 5: Tích hợp & điều phối
    ↓
Giai đoạn 6: Kiểm định & kiểm thử
```

## Cài đặt

### Qua Marketplace

#### Thêm marketplace
```shell
/plugin marketplace add revfactory/harness
```

#### Cài plugin
```shell
/plugin install harness@harness-marketplace
```

### Cài trực tiếp dưới dạng Global Skill

```shell
# Copy thư mục skills vào ~/.claude/skills/harness/
cp -r skills/harness ~/.claude/skills/harness
```

## Cấu trúc Plugin

```
harness/
├── .claude-plugin/
│   └── plugin.json                 # Plugin manifest
├── skills/
│   └── harness/
│       ├── SKILL.md                # Định nghĩa skill chính (quy trình 6 giai đoạn)
│       └── references/
│           ├── agent-design-patterns.md   # 6 mẫu kiến trúc
│           ├── orchestrator-template.md   # Template orchestrator cho team/subagent
│           ├── team-examples.md           # 5 cấu hình đội thực tế
│           ├── skill-writing-guide.md     # Hướng dẫn viết skill
│           ├── skill-testing-guide.md     # Phương pháp kiểm thử & đánh giá
│           └── qa-agent-guide.md          # Hướng dẫn tích hợp agent QA
└── README.md
```

## Cách sử dụng

Kích hoạt trong Claude Code với các prompt như:

```
Build a harness for this project
Design an agent team for this domain
Set up a harness
```

### Các chế độ thực thi

| Chế độ | Mô tả | Khuyến nghị cho |
|------|-------------|-----------------|
| **Agent Teams** (mặc định) | TeamCreate + SendMessage + TaskCreate | 2 agent trở lên cần phối hợp |
| **Subagents** | Gọi trực tiếp công cụ Agent | Nhiệm vụ một lần, không cần giao tiếp liên-agent |

<p align="center">
  <img src="harness_team.png" alt="Harness Agent Team" width="500">
</p>

### Các mẫu kiến trúc

| Mẫu | Mô tả |
|---------|-------------|
| Pipeline | Nhiệm vụ phụ thuộc tuần tự |
| Fan-out/Fan-in | Nhiệm vụ song song độc lập |
| Expert Pool | Gọi chọn lọc theo ngữ cảnh |
| Producer-Reviewer | Sinh nội dung sau đó kiểm tra chất lượng |
| Supervisor | Agent trung tâm phân phối nhiệm vụ động |
| Hierarchical Delegation | Ủy quyền đệ quy từ trên xuống |

## Đầu ra

Các file được Harness sinh ra:

```
your-project/
├── .claude/
│   ├── agents/          # File định nghĩa agent
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # File skill
│       ├── analyze/
│       │   └── SKILL.md
│       └── build/
│           ├── SKILL.md
│           └── references/
```

## Use Case — Thử các prompt sau

Copy bất kỳ prompt nào dưới đây vào Claude Code sau khi cài Harness:

**Nghiên cứu chuyên sâu**
```
Build a harness for deep research. I need an agent team that can investigate
any topic from multiple angles — web search, academic sources, community
sentiment — then cross-validate findings and produce a comprehensive report.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness cho nghiên cứu chuyên sâu. Tôi cần một đội agent có thể điều tra bất kỳ chủ đề nào từ nhiều góc độ — tìm kiếm web, nguồn học thuật, cảm nhận cộng đồng — sau đó đối chiếu chéo các phát hiện và tạo ra một báo cáo toàn diện."

**Phát triển website**
```
Build a harness for full-stack website development. The team should handle
design, frontend (React/Next.js), backend (API), and QA testing in a
coordinated pipeline from wireframe to deployment.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness cho phát triển website full-stack. Đội cần xử lý thiết kế, frontend (React/Next.js), backend (API), và kiểm thử QA trong một pipeline được điều phối từ wireframe đến triển khai."

**Sản xuất webtoon / truyện tranh**
```
Build a harness for webtoon episode production. I need agents for story
writing, character design prompts, panel layout planning, and dialogue
editing. They should review each other's work for style consistency.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness cho sản xuất tập webtoon. Tôi cần agent cho việc viết truyện, prompt thiết kế nhân vật, lập kế hoạch bố cục khung hình, và biên tập lời thoại. Các agent cần kiểm tra chéo công việc của nhau để đảm bảo tính nhất quán về phong cách."

**Lập kế hoạch nội dung YouTube**
```
Build a harness for YouTube content creation. The team should research
trending topics, write scripts, optimize titles/tags for SEO, and plan
thumbnail concepts — all coordinated by a supervisor agent.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness cho sáng tạo nội dung YouTube. Đội cần nghiên cứu các chủ đề đang hot, viết script, tối ưu title/tag cho SEO, và lên ý tưởng thumbnail — tất cả được điều phối bởi một agent giám sát (supervisor)."

**Review code & tái cấu trúc**
```
Build a harness for comprehensive code review. I want parallel agents
checking architecture, security vulnerabilities, performance bottlenecks,
and code style — then merging all findings into a single report.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness cho review code toàn diện. Tôi muốn các agent chạy song song kiểm tra kiến trúc, lỗ hổng an ninh, điểm nghẽn hiệu năng, và phong cách code — sau đó hợp nhất tất cả phát hiện vào một báo cáo duy nhất."

**Tài liệu kỹ thuật**
```
Build a harness that generates API documentation from this codebase.
Agents should analyze endpoints, write descriptions, generate usage
examples, and review for completeness.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness để sinh tài liệu API từ codebase này. Các agent cần phân tích endpoint, viết mô tả, tạo ví dụ sử dụng, và kiểm tra tính đầy đủ."

**Thiết kế Data Pipeline**
```
Build a harness for designing data pipelines. I need agents for schema
design, ETL logic, data validation rules, and monitoring setup that
delegate sub-tasks hierarchically.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness để thiết kế data pipeline. Tôi cần agent cho thiết kế schema, logic ETL, quy tắc kiểm định dữ liệu, và thiết lập giám sát, ủy quyền nhiệm vụ con theo phân cấp."

**Chiến dịch Marketing**
```
Build a harness for marketing campaign creation. The team should research
the target market, write ad copy, design visual concepts, and set up
A/B test plans with iterative quality review.
```
> **Phiên bản tiếng Việt:** "Xây dựng harness cho tạo chiến dịch marketing. Đội cần nghiên cứu thị trường mục tiêu, viết nội dung quảng cáo, thiết kế ý tưởng hình ảnh, và thiết lập kế hoạch thử nghiệm A/B với kiểm tra chất lượng lặp lại."

## Cùng tồn tại — Harness và các hàng xóm

Harness không đơn độc trong hệ sinh thái Claude Code / agent-framework. Các repo sau nằm ở các tầng liền kề; mỗi repo được mô tả theo dạng song song "X là …, Harness là …" để bạn có thể chọn cái phù hợp với nhu cầu hoặc kết hợp nhiều repo.

| Repo | Vị trí của họ | Mối quan hệ với Harness |
|------|----------------|-------------------------|
| [coleam00/Archon](https://github.com/coleam00/Archon) | "harness builder" — cấu hình runtime tất định, có thể lặp lại | **Cùng L3, tầng con hàng xóm.** Archon là Nhà máy Cấu hình Runtime, Harness là Nhà máy Kiến trúc Đội. Chọn Archon nếu cần tính tất định của runtime, chọn Harness nếu cần kiến trúc đội, hoặc kết hợp cả hai. |
| [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) | Bản port Codex của cùng khái niệm | **Cùng L3, runtime khác.** Dùng Harness trên Claude Code, meta-harness trên Codex. |
| [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) | "Tầng hiệu năng & quy trình của agent harness" (nằm trên các harness hiện có) | **Tầng khác.** ECC là tầng chuẩn hóa giữa các harness; Harness là nhà máy sinh ra harness. Có thể kết hợp nối tiếp. |
| [wshobson/agents](https://github.com/wshobson/agents) | Danh mục subagent / skill (182 agent, 149 skill) | **Nhà máy ↔ nguồn cung linh kiện.** wshobson là danh mục để chọn dùng; Harness thiết kế đội. Có thể hấp thụ các mục từ wshobson làm linh kiện trong một đội do Harness sinh ra. |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Điều phối state-graph, không phụ thuộc LLM cụ thể | **Hướng đi khác.** LangGraph dành cho điều phối dài hạn, có thể khôi phục trạng thái; Harness dành cho thiết kế đội nhanh, thuần Claude Code. |

## Xây dựng bằng Harness

### Harness 100

**[revfactory/harness-100](https://github.com/revfactory/harness-100)** — 100 harness đội agent sẵn sàng sản xuất trên 10 lĩnh vực, có cả phiên bản tiếng Anh và tiếng Hàn (tổng 200 package). Mỗi harness đi kèm 4-5 agent chuyên biệt, một skill orchestrator, và các skill theo lĩnh vực — tất cả được sinh ra bởi plugin này. 1.808 file markdown bao gồm sáng tạo nội dung, phát triển phần mềm, dữ liệu/AI, chiến lược kinh doanh, giáo dục, pháp lý, y tế, và nhiều hơn nữa.

### Nghiên cứu: Thử nghiệm A/B đo hiệu quả của Harness

**[revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)** — Một thử nghiệm có kiểm soát trên 15 nhiệm vụ kỹ thuật phần mềm đo lường tác động của việc cấu hình trước có cấu trúc đến chất lượng đầu ra của LLM code agent.

| Chỉ số | Không có Harness | Có Harness | Cải thiện |
|--------|:-:|:-:|:-:|
| Điểm chất lượng trung bình | 49.5 | 79.3 | **+60%** |
| Tỷ lệ thắng | — | — | **100%** (15/15) |
| Độ phân tán đầu ra | — | — | **-32%** |

Phát hiện chính: hiệu quả tăng theo độ phức tạp nhiệm vụ — nhiệm vụ khó hơn thì mức cải thiện càng lớn (+23.8 Cơ bản, +29.6 Nâng cao, +36.2 Chuyên gia).

**Cách diễn đạt chính xác để dùng mọi nơi:** +60% chất lượng trung bình (49.5 → 79.3), tỷ lệ thắng 15/15, độ phân tán −32% (n=15, A/B do tác giả tự đo, đang chờ tái lập độc lập từ bên thứ ba).

> Bài báo đầy đủ: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality.*

## Yêu cầu

- [Agent Teams đã được bật](https://code.claude.com/docs/en/agent-teams): `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

## Câu hỏi thường gặp

<details>
<summary><b>Câu 1. "+60%" có phải là phóng đại không?</b></summary>

**Trả lời.** Con số +60% đến từ một **thử nghiệm A/B do tác giả tự đo (n=15, 15 nhiệm vụ, đo trên repo song sinh `claude-code-harness`)**. Mọi lần trích dẫn số liệu này trong repo đều đi kèm ghi chú "n=15, do tác giả tự đo, đang chờ tái lập độc lập từ bên thứ ba" trong cùng câu. Để ra quyết định áp dụng, chúng tôi khuyên bạn nên chạy thử pilot nội bộ 2–4 tuần và đo số liệu của riêng mình.

**Bằng chứng:**
- A/B của tác giả: [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)
- Bài báo: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality*
</details>

<details>
<summary><b>Câu 2. Vì sao gọi là "nhà máy harness" mà không phải "harness builder"? Có cạnh tranh với Archon không?</b></summary>

**Trả lời.** Archon sinh ra các cấu hình runtime tất định — đó là một **Nhà máy Cấu hình Runtime**. Harness sinh ra kiến trúc đội agent (cấu trúc đội, giao thức message, cổng kiểm duyệt) — đó là một **Nhà máy Kiến trúc Đội**. Đây là **hai tầng con hàng xóm của cùng tầng L3 Meta-Factory** và phục vụ các nhu cầu khác nhau. Chọn Archon nếu cần tính tất định của runtime, chọn Harness nếu cần mẫu kiến trúc đội, hoặc kết hợp cả hai (thiết kế kiến trúc với Harness → triển khai runtime với Archon).

**Bằng chứng:**
- Tự định nghĩa của Archon: [clawfit docs/reference-levels.md](https://github.com/hongsw/clawfit/blob/main/docs/reference-levels.md)
- Khai báo tầng con: xem mục **Phân loại — Vị trí của Harness** ở trên
- Repo Archon: [github.com/coleam00/Archon](https://github.com/coleam00/Archon)
</details>

<details>
<summary><b>Câu 3. "Chỉ dành cho Claude Code" có quá hẹp không? Còn Gemini/Codex thì sao?</b></summary>

**Trả lời.** Hiện tại runtime chính thức chỉ là Claude Code. Một bản port Codex của cùng khái niệm — [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) — đã công khai, nên các đội dùng Codex có thể bắt đầu từ đó. Harness chọn hướng "thuần Claude Code, đào sâu" thay vì "đa runtime, hời hợt"; hợp tác đa runtime với các repo anh em (meta-harness, harness-init, OpenRig) đang trong lộ trình.

**Bằng chứng:**
- Bản port Codex: [github.com/SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness)
- Scaffolder đa runtime: [github.com/Gizele1/harness-init](https://github.com/Gizele1/harness-init)
</details>

## Giấy phép

Apache 2.0
