# Post-M0 Audit — 2026-04-18

**Phụ trách:** agent repo-auditor
**Repo đối tượng:** `/Users/robin/IdeaProjects/harness`
**Công việc cấp trên:** kiểm chứng tích hợp kết quả áp dụng song song M0 Quick Wins của 4 agent release-engineer / content-creator / launch-strategist / community-scout
**Cách kiểm chứng:** chỉ đọc (cấm Edit/Write). Dùng `git diff`·`git status`·Read từng file để phán định tính nhất quán·xung đột·mất section.

---

## 1. Kết quả kiểm chứng (ma trận PASS/FAIL)

### A. Tính nhất quán phiên bản (release-engineer)

| Vùng | Hạng mục kiểm chứng | Kết quả | Ghi chú |
|------|-----------|------|------|
| A-1 | Badge `Version-1.2.0` tại `README.md:6` | **PASS** | Giữ `brightgreen`, xác nhận đổi từ `1.0.1` gốc |
| A-2 | Badge `Version-1.2.0` tại `README_KO.md:6` | **PASS** | Chuỗi nhất quán giống bản EN |
| A-3 | Badge `Version-1.2.0` tại `README_JA.md:6` | **PASS** | Chuỗi nhất quán giống bản EN |
| A-4 | `"version": "1.2.0"` tại `.claude-plugin/marketplace.json:14` | **PASS** | Đổi từ `1.1.0` gốc → `1.2.0` |
| A-5 | Giữ `"version": "1.2.0"` tại `.claude-plugin/plugin.json:4` | **PASS (số liệu)** / **FAIL (chính sách)** | Field version vẫn là `1.2.0` nhưng `description`·`keywords` đã bị đổi — xem §4 audit xung đột |
| A-6 | Entry [1.2.1] trong `CHANGELOG.md` | **PASS** | Section `[1.2.1] - 2026-04-18` ở đầu, đủ 3 block Fixed/Added/Changed |
| A-7 | Sự tồn tại của `_workspace/release/audit-2026-04-18.md` | **PASS** | 228 dòng, đủ 5 section + 2 phụ lục |

### B. Định vị "harness factory" trong README (content-creator)

| Vùng | Hạng mục kiểm chứng | EN | KO | JA | Ghi chú |
|------|-----------|----|----|----|------|
| B-1 | H1 `Harness — The Team-Architecture Factory for Claude Code` (dịch theo từng ngôn ngữ) | **PASS** | **PASS** | **PASS** | EN(L20), KO(L20 "팀 아키텍처 팩토리"), JA(L20 "チームアーキテクチャファクトリー") |
| B-2 | Đoạn callout dưới H1 (song ngữ trigger 3 ngôn ngữ) | **PASS** | **PASS** | **PASS** | EN(L24), KO(L24), JA(L24) — tất cả đều ghi kèm cụm trigger 3 ngôn ngữ Anh/Hàn/Nhật |
| B-3 | 3 badge (Layer / Sub-layer / i18n) | **PASS** | **PASS** | **PASS** | EN(L14–18), KO(L14–18), JA(L14–18) — cả 3 đều link tới anchor theo ngôn ngữ tương ứng |
| B-4 | Bảng 4 dòng "Category — Where Harness Sits" | **PASS** | **PASS** | **PASS** | EN(L30–39 + footnote L41), KO(L30–41), JA(L30–41) — bảng 4 dòng + đoạn tóm tắt Archon vs. Harness |
| B-5 | Section "Harness Evolution Mechanism" | **PASS** | **PASS** | **PASS** | EN(L61–74), KO(L50–63), JA(L50–63) — có kèm sơ đồ ASCII bắt delta |
| B-6 | Cụm từ phòng vệ chính thức "+60%" (n=15, author-measured, third-party replications pending) | **PASS** | **PASS** | **PASS** | EN(L273), KO(L255), JA(L262) — cả 3 ngôn ngữ đều có cùng cụm từ. Xác nhận lại ở FAQ Q1 (EN:L286 / KO:L268 / JA:L275) |
| B-7 | Bảng 5 dòng "Coexistence" | **PASS** | **PASS** | **PASS** | EN(L247–253), KO(L229–235), JA(L236–242) — 5 dòng (Archon·meta-harness·ECC·wshobson·LangGraph) |
| B-8 | Section "FAQ" (Q1~Q3 details) | **PASS** | **PASS** | **PASS** | Cả 3 bản đều có 3 `<details>` (+60% / harness factory / Claude Code only) |

### C. Thư mục docs/ (launch-strategist)

| Vùng | Hạng mục kiểm chứng | Kết quả | Ghi chú |
|------|-----------|------|------|
| C-1 | `docs/experimental-dependency.md` (~150 dòng) | **PASS** | 154 dòng. Có đủ Current State / Dependency Graph / 3 Scenarios (A·B·C T+24/48/72h) / bảng Monitoring SLA / Enterprise FAQ Q1–Q3 |
| C-2 | `docs/quickstart.md` (~120 dòng, 5 bước·5 failure FAQ) | **PASS** | 118 dòng. Step 1–5 + mỗi bước có Failure FAQ #1–#5. Ngân sách thời gian 5 phút ghi rõ ở đầu |
| C-3 | `docs/show-hn-launch-kit.md` (~220 dòng, 2026-05-06 07:05 PT) | **PASS** | 224 dòng. Bảng lịch trình ghi rõ `2026-05-06 Wed 07:05 PT`. Có đủ Title A/B/C · Body 380 từ · timeline T-72h~T+72h · phân nhánh Post-launch · đối ứng 5%-oversold · Crossposting Rules |

### D. Quản trị (community-scout)

| Vùng | Hạng mục kiểm chứng | Kết quả | Ghi chú |
|------|-----------|------|------|
| D-1 | Công bố số liệu 5 hạng mục SLA trong `CONTRIBUTING.md` | **PASS** | PR phản hồi lần đầu 72h / Issue triage 48h / Bug P0–P1 14d / Security 7d / Release 2 tuần — cả 5 hạng mục đều công khai số liệu trong bảng |
| D-2 | `.github/ISSUE_TEMPLATE/bug_report.yml` | **PASS** | Có field bắt buộc: claude-code-version · dropdown experimental-flag · các trường tái hiện·kỳ vọng·thực tế·dropdown OS |
| D-3 | `.github/ISSUE_TEMPLATE/feature_request.yml` | **PASS** | Cấu trúc problem / proposal / alternatives / dropdown related-pattern (6 mẫu+N) |
| D-4 | `.github/ISSUE_TEMPLATE/question.yml` | **PASS** | 3 field question / tried / docs |
| D-5 | `.github/ISSUE_TEMPLATE/config.yml` | **PASS** | `blank_issues_enabled: false` + link Discussions + mailto bảo mật |
| D-6 | `.github/PULL_REQUEST_TEMPLATE.md` | **PASS** | Summary/Motivation/Scope checkbox 8 mục/Tests/CHANGELOG/4 lựa chọn SemVer |
| D-7 | `_workspace/community/issue-3-reply.md` (tiếng Anh) | **PASS** | Có nhắc roadmap PoC Gemini P-01, SaehwanPark/meta-harness, gồm phương án thay thế Gizele1/harness-init·OpenRig |
| D-8 | `_workspace/community/issue-2-reply.md` (tiếng Anh) | **PASS** | Trích dẫn trực tiếp hesreallyhim ("really good stuff ... Nice job."), thêm badge + đề xuất category "Harness Factories" |

---

## 2. Vấn đề phát hiện

| # | Mức độ | Vị trí | Vấn đề | Hành động khuyến nghị |
|---|--------|------|------|----------|
| **1** | **Critical** | `.claude-plugin/plugin.json:3, 12–28` | **`plugin.json` được chỉ thị là "không nên đụng tới" nhưng `description` đã bị viết lại toàn bộ + thêm 7 `keywords`.** Tài liệu audit của release-engineer (`audit-2026-04-18.md:89–91`) tuyên bố "plugin.json không sửa" nhưng `git diff` thực tế cho thấy file này đã thay đổi. Đây được phán đoán là **dấu vết content-creator tự ý sửa để đồng nhất định vị**, gây xung đột. | Chọn 1 trong 2 hướng: (a) **Chấp nhận**: thêm rõ vào block Changed của CHANGELOG 1.2.1 dòng "đồng bộ description·keywords của plugin.json với tuyên bố định vị", và sửa lại câu "không sửa" ở §3.3 audit của release-engineer thành "description·keywords được content-creator điều chỉnh, version giữ nguyên". (b) **Khôi phục**: dùng `git restore .claude-plugin/plugin.json` để hoàn nguyên rồi tách thành PR riêng. — Nếu commit ở trạng thái hiện tại, sẽ tồn tại vấn đề vệ sinh "tài liệu audit mâu thuẫn với trạng thái thực tế". |
| **2** | Minor | `README.md:42` vs `README_KO.md`/`README_JA.md` | README bản EN giữ lại section `## Star History` (L43–51) nhưng KO/JA **không có** section này. Ở HEAD gốc KO/JA cũng không có nên **không phải bị xóa** — nhưng từ góc nhìn "đối xứng giữa 3 ngôn ngữ" thì đây là điểm lệch. | **Cho phép** ở release này (giữ nguyên gốc). Khuyến nghị mở issue `docs/i18n-parity` ở PR sau để bổ sung section Star History vào KO/JA ở cùng vị trí (ngay sau section Category). |
| **3** | Minor | `README.md:15–17` / `README_KO.md:15–17` / `README_JA.md:15–17` | Anchor của badge `Layer` khác nhau theo từng ngôn ngữ (EN: `#category--where-harness-sits`, KO: `#카테고리--harness는-어디에-서-있나요`, JA: `#カテゴリー--harness-はどこに位置するか`). Cần khớp với anchor GitHub tự sinh theo từng ngôn ngữ, nhưng quy tắc anchor tiếng Hàn·Nhật của GitHub là `khoảng trắng→gạch ngang + viết thường + xóa một số ký tự đặc biệt`. **Khả năng cao `—(em dash)` trong anchor KO `카테고리--harness는-어디에-서-있나요` không render thành `--`** (thường `—` bị xóa hoặc thay bằng `-` đơn). Cần kiểm chứng. | Khuyến nghị kiểm chứng render bằng GitHub Preview hoặc grip cục bộ trước khi commit. Nếu lỗi, sửa anchor thành `#카테고리-harness는-어디에-서-있나요` (xóa em dash) hoặc dùng anchor `<a name="">` rõ ràng. JA cũng cần lưu ý tương tự. |
| **4** | Info | `_workspace/release/audit-2026-04-18.md:156` | §4.4 có mục chờ thực thi `git push origin v1.0.0 v1.0.1 v1.1.0 v1.2.0`, nhưng kết quả M0 lần này không bao gồm tạo tag·push — đây là **trạng thái chờ phê duyệt có chủ đích**, không phải vấn đề. Nhưng cần quyết định xử lý 4 tag trước khi vào Phase tiếp theo. | 4 tag + nháp GitHub Release thực hiện riêng trước khi bắt đầu M1. Nằm ngoài phạm vi audit M0 này. |
| **5** | Info | `docs/experimental-dependency.md:65` | Link "phát hiện bởi Nightly CI tại P-13" của Scenario A là `[P-13](#)` — link placeholder. Chưa chỉ định số roadmap·issue thực tế. | Mở issue roadmap P-13 thực tế rồi thay bằng `#số`. Công việc tiếp theo của launch-strategist. |

---

## 3. Đánh giá theo nguyên tắc 5 giây

### 3.1 Kịch bản quét 5 giây đầu trang

Thứ tự thông tin thị giác khách xem gặp đầu tiên ở `README.md`:

1. **Ảnh banner** (L1–3) — `harness_banner.png`
2. **6 badge cơ bản** (L5–12) — Version `1.2.0` / License Apache 2.0 / Claude Code Plugin / 6 Architectures / Agent Teams / GitHub Stars
3. **3 badge định vị** (L14–18) — `Layer: L3 Meta-Factory` / `Sub-layer: Team-Architecture Factory` / `README: EN | KO | JA`
4. **H1** (L20) — `Harness — The Team-Architecture Factory for Claude Code`
5. **Toggle ngôn ngữ** (L22) — `English | 한국어 | 日本語`
6. **Block Callout** (L24) — một câu tóm tắt kèm trigger 3 ngôn ngữ

### 3.2 Phán định nguyên tắc 5 giây

| Tiêu chí | Đánh giá |
|------|------|
| Có hiểu được đây là "nhà máy kiến trúc đội" không? | **PASS** — hiện 3 lần qua H1 + badge Sub-layer + Callout. Có thể nắm tới L3 Meta-Factory trong vòng 5 giây |
| Có hình ảnh hóa câu trigger không? | **PASS** — Callout ghi kèm 3 câu `"build a harness for this project"` / `"하네스 구성해줘"` / `"ハーネスを構成して"` |
| Tín hiệu tin cậy (version·star·license) có hiện đồng thời không? | **PASS** — 6 badge cơ bản ở dòng đầu |
| Người đọc 3 ngôn ngữ có cùng trải nghiệm không? | **PASS** — cả EN/KO/JA đều có cấu trúc 3 tầng giống nhau (ảnh→badge→H1→Callout), chỉ khác chuỗi văn bản |
| Có yếu tố lãng phí tầm mắt (badge quảng cáo, link trùng) không? | **PASS** — 9 badge (6 cơ bản + 3 định vị) nằm trong ngưỡng trên của trung bình repo Trending (5–7). Không quá nhiều |

### 3.3 Đánh giá logic thứ tự section

Thứ tự section theo bản EN:

```
(1) Overview → (2) Category — Where Harness Sits → (3) Star History → (4) Key Features
→ (5) Harness Evolution Mechanism → (6) Workflow → (7) Installation → (8) Plugin Structure
→ (9) Usage (chế độ·mẫu) → (10) Output → (11) 8 Use Cases → (12) Coexistence
→ (13) Built with Harness (100 + nghiên cứu A/B) → (14) Requirements → (15) FAQ Q1–Q3 → (16) License
```

- **PASS** — Thứ tự "mình là gì (1–2) → mình tiến hóa thế nào (5) → cài thế nào (7) → dùng thế nào (9–11) → cùng tồn tại với hàng xóm thế nào (12) → bằng chứng (13) → phản biện·FAQ (15)" rất tự nhiên.
- Tuy nhiên KO/JA không có (3) Star History nên đi thẳng (2) → (4). Luồng thị giác lại càng mượt hơn nên không thành vấn đề.

---

## 4. Audit xung đột giữa các agent

### 4.1 Bảng quy thuộc người sửa theo từng file

| File | release-engineer | content-creator | launch-strategist | community-scout |
|------|------------------|-----------------|-------------------|-----------------|
| `README.md` | Badge L6(Version) | H1·Callout·3 badge·Category·Evolution·Coexistence·FAQ | — | — |
| `README_KO.md` | Badge L6 | H1·Callout·badge·Category·Evolution·Coexistence·FAQ | — | — |
| `README_JA.md` | Badge L6 | H1·Callout·badge·Category·Evolution·Coexistence·FAQ | — | — |
| `.claude-plugin/marketplace.json` | version L14 | — | — | — |
| `.claude-plugin/plugin.json` | **(tuyên bố không đụng tới)** | **sửa description·keywords (xung đột)** | — | — |
| `CHANGELOG.md` | Thêm block [1.2.1] | — | — | — |
| `CONTRIBUTING.md` | — | — | — | Mới |
| `.github/ISSUE_TEMPLATE/*` | — | — | — | Mới (4 file) |
| `.github/PULL_REQUEST_TEMPLATE.md` | — | — | — | Mới |
| `docs/experimental-dependency.md` | — | — | Mới | — |
| `docs/quickstart.md` | — | — | Mới | — |
| `docs/show-hn-launch-kit.md` | — | — | Mới | — |
| `_workspace/release/audit-2026-04-18.md` | Mới | — | — | — |
| `_workspace/community/issue-{2,3}-reply.md` | — | — | — | Mới (2 file) |

### 4.2 Có sửa đồng thời cùng dòng không

- **Dòng badge README (3 bản, L6)** — release-engineer (chỉ đổi chuỗi badge Version ở L6) vs content-creator (viết lại section dưới H1). **Không chồng lấp**. content-creator cũng chỉ **thêm block badge mới** ở L14–18, không đụng L6 nên không xung đột. **PASS**
- **H1 README (L20)** — release-engineer không sửa. Chỉ content-creator sửa riêng. **PASS**
- **`.claude-plugin/plugin.json`** — chính sách của release-engineer là không đụng L4(version) và thực tế L4 không đổi. Nhưng L3(description) + L12–28(keywords) **đã bị sửa**. Nếu sửa này do content-creator thực hiện thì có **mâu thuẫn giữa tuyên bố và thực tế** với §3.3 tài liệu audit của release-engineer. Đây không phải xung đột merge đơn giản mà là **xung đột phối hợp mang tính vi phạm chính sách**. → xem **vấn đề Critical số 1**
- `_workspace/release/audit-2026-04-18.md` — chỉ release-engineer. **PASS**

### 4.3 Section gốc bị mất

| Section | Tồn tại ở gốc (HEAD) | EN hiện tại | KO hiện tại | JA hiện tại | Phán định |
|------|-----------------|-------|-------|-------|------|
| Star History | Chỉ có ở EN | Giữ (L43) | Vốn không có | Vốn không có | **PASS** (mất 0) |
| Installation | Có ở EN/KO/JA | Giữ (L92) | Giữ (L81) | Giữ (L81) | **PASS** |
| Plugin Structure | Có ở EN/KO/JA | Giữ (L113) | Giữ (L102) | Giữ (L102) | **PASS** |
| Usage chế độ·mẫu | Có ở EN/KO/JA | Giữ (L132–162) | Giữ (L121–151) | Giữ (L121–151) | **PASS** |
| 8 Use Cases | Có ở EN/KO/JA | Giữ (L183–241) | Giữ (L172–223) | Giữ (L172–230) | **PASS** |
| Built with Harness (100 + nghiên cứu A/B) | Có ở EN/KO/JA | Giữ (L255–275) | Giữ (L237–257) | Giữ (L244–264) | **PASS** |
| Requirements / License | Có ở EN/KO/JA | Giữ | Giữ | Giữ | **PASS** |

**Tổng hợp:** 0 section gốc bị mất. Việc merge được thực hiện theo cách "chèn section mới giữa text hiện có" nên thành công song song không xung đột.

---

## 5. Kết luận

### 5.1 Tổng hợp PASS/FAIL

- **Vùng A (tính nhất quán version):** 6 PASS / 1 **FAIL chính sách** (sửa description·keywords plugin.json không được phép) trong 7 mục
- **Vùng B (định vị):** toàn bộ 24 mục (8 × 3 ngôn ngữ) PASS
- **Vùng C (docs/):** 3 PASS
- **Vùng D (quản trị):** 8 PASS
- **Nguyên tắc 5 giây:** PASS
- **Xung đột agent:** 1 Critical (vi phạm chính sách plugin.json) + 2 Minor (kiểm chứng render anchor i18n / thiếu Star History ở KO·JA)

**Tổng vấn đề Critical: 1**
**Tổng vấn đề Minor: 2**
**Mục Info (khuyến nghị): 2**

### 5.2 Có thể commit không

**Có thể commit có điều kiện.** Cần quyết định 1 việc sau trước khi commit:

#### Hành động bắt buộc trước — giải quyết xung đột `plugin.json` (chọn 1)

- **Phương án A (khuyến nghị): Chấp nhận** — sửa bảng §3 và câu §3.3 trong `_workspace/release/audit-2026-04-18.md` để ghi rõ "bao gồm thay đổi description·keywords". Thêm dòng sau vào section Changed của `CHANGELOG.md` [1.2.1]:
  > - Đồng bộ description và keywords của `.claude-plugin/plugin.json` với tuyên bố định vị "harness factory" (giữ version 1.2.0)
- **Phương án B: Khôi phục** — dùng `git restore .claude-plugin/plugin.json` để hoàn nguyên, sau đó content-creator yêu cầu chính thức ở PR riêng sau.

→ **repo-auditor khuyến nghị Phương án A.** Cơ sở: (a) nội dung thay đổi vốn phù hợp với tính nhất quán định vị và vô hại, (b) version tại `.claude-plugin/plugin.json:4` vẫn giữ `1.2.0` nên không ảnh hưởng chức năng runtime Claude Code, (c) nếu hoàn nguyên sẽ tạo ra **khoảng lệch tính nhất quán mới** giữa description mới của README/marketplace.json và description cũ của plugin.json.

#### Cụm từ commit message khuyến nghị (nếu chọn Phương án A)

```
feat: M0 Quick Wins — 포지셔닝 선언, 버전 정합성, 거버넌스 공개

- README 3종(EN/KO/JA) 상단을 "Team-Architecture Factory" 포지셔닝으로 재작성
  (Category · Evolution · Coexistence · FAQ 섹션 신설, Layer/Sub-layer/i18n 뱃지 3종 추가)
- 버전 1.2.0 정합성 동기화: README 뱃지 3종(1.0.1→1.2.0), marketplace.json(1.1.0→1.2.0)
- plugin.json description·keywords를 포지셔닝 선언과 정렬 (version 1.2.0 유지)
- CHANGELOG [1.2.1] 엔트리 추가
- CONTRIBUTING.md 신설: 5항목 SLA 수치 공개 (PR 72h / 이슈 48h / P0 14d / 보안 7d / 릴리스 2주)
- .github/ISSUE_TEMPLATE 4종(bug/feature/question/config) + PR 템플릿 신설
- docs/ 신설: experimental-dependency (3 시나리오 SLA), quickstart (5분 5단계), show-hn-launch-kit (2026-05-06 07:05 PT)
- _workspace/community: Issue #2 (awesome-claude-code 큐레이터) / Issue #3 (Gemini 질의) 답변 초안
- _workspace/release/audit-2026-04-18.md + post-m0-audit-2026-04-18.md: 감사 기록
```

### 5.3 Khuyến nghị không cần sửa trước (Info)

- **Tạo truy hồi 4 tag (v1.0.0/v1.0.1/v1.1.0/v1.2.0) + nháp GitHub Release** — nội dung lệnh đang chờ ở §4, §5 của `_workspace/release/audit-2026-04-18.md`. Thực hiện riêng trước khi vào M1.
- **Bổ sung section Star History vào README KO/JA** — tách ra PR sau (`docs/i18n-parity`).
- **Kiểm chứng render anchor GitHub** — kiểm tra trực quan ở tab Preview sau khi `gh pr create --draft`, xem badge Layer/Sub-layer có click đúng ở KO/JA không.

---

## Phụ lục. Danh sách file làm cơ sở audit

- `/Users/robin/IdeaProjects/harness/README.md` (317 dòng)
- `/Users/robin/IdeaProjects/harness/README_KO.md` (299 dòng)
- `/Users/robin/IdeaProjects/harness/README_JA.md` (306 dòng)
- `/Users/robin/IdeaProjects/harness/.claude-plugin/plugin.json` (đã sửa, §2.1 Critical)
- `/Users/robin/IdeaProjects/harness/.claude-plugin/marketplace.json`
- `/Users/robin/IdeaProjects/harness/CHANGELOG.md`
- `/Users/robin/IdeaProjects/harness/CONTRIBUTING.md`
- `/Users/robin/IdeaProjects/harness/.github/ISSUE_TEMPLATE/{bug_report,feature_request,question,config}.yml`
- `/Users/robin/IdeaProjects/harness/.github/PULL_REQUEST_TEMPLATE.md`
- `/Users/robin/IdeaProjects/harness/docs/experimental-dependency.md`
- `/Users/robin/IdeaProjects/harness/docs/quickstart.md`
- `/Users/robin/IdeaProjects/harness/docs/show-hn-launch-kit.md`
- `/Users/robin/IdeaProjects/harness/_workspace/release/audit-2026-04-18.md`
- `/Users/robin/IdeaProjects/harness/_workspace/community/issue-{2,3}-reply.md`

Log lệnh audit: `git status`, `git diff --stat`, `git diff .claude-plugin/plugin.json`, `git show HEAD:README.md`, gọi công cụ Read cho từng file.
