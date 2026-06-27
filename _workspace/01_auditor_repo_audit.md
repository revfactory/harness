# Harness — Audit Sẵn Sàng GitHub Trending

**Ngày:** 2026-03-29
**Repo:** [revfactory/harness](https://github.com/revfactory/harness)
**Tagline:** Agent Team & Skill Architect — A Claude Code Plugin

---

## Điểm mạnh chính

1. **Cấu trúc README xuất sắc** — Ảnh banner ngay đầu trang, 6 badge, hỗ trợ đa ngôn ngữ (EN/KO/JA), sơ đồ quy trình rõ ràng, bảng mẫu kiến trúc, và nhiều prompt use-case phong phú. Đã trên trung bình so với phần lớn repo trending.
2. **Landing page (index.html)** — Một landing page tối màu, hoàn thiện, có toggle đa ngôn ngữ. Nhiều repo trending không có web presence nào.
3. **Câu chuyện mạnh** — README có section "Built with Harness" với kết quả thử nghiệm A/B định lượng (+60% cải thiện chất lượng, tỷ lệ thắng 100%). Loại bằng chứng này hiếm và rất thuyết phục.
4. **Đa ngôn ngữ từ ngày đầu** — README ở 3 ngôn ngữ (EN, KO, JA) cùng i18n trên landing page. Mở rộng khả năng được tìm thấy qua các cộng đồng ngôn ngữ.
5. **Cấu trúc plugin rõ ràng** — `plugin.json`, `SKILL.md`, và thư mục references được tổ chức tốt. Đóng gói chuyên nghiệp.
6. **CHANGELOG** — Tuân theo Semantic Versioning với các mục chi tiết. Cho thấy duy trì chủ động.
7. **Giấy phép Apache 2.0** — Linh hoạt, thân thiện với doanh nghiệp.

---

## Điểm số Audit

| Hạng mục | Điểm | Ghi chú |
|----------|:-----:|-------|
| 1. Chất lượng README | **8/10** | Mạnh. Thiếu: GIF/screencast demo, Quick Start có thể nổi bật hơn |
| 2. Cấu trúc repo | **4/10** | Không có issue template, PR template, CONTRIBUTING.md, CODE_OF_CONDUCT.md, không có tag/release |
| 3. Tín hiệu tin cậy | **3/10** | Không có CI/CD, không có test, không có docs site, không có release |
| 4. Khả năng được tìm thấy | **7/10** | README đa ngôn ngữ, landing page, badge. Thiếu: GitHub Topics, social preview, SEO description |

**Điểm tổng: 5.5 / 10**

---

## Phát hiện chi tiết & khuyến nghị

### 1. Chất lượng README (8/10)

| Mục | Trạng thái | Ghi chú |
|------|--------|-------|
| Tagline | ✅ | "Agent Team & Skill Architect — A Claude Code Plugin" |
| Ảnh banner ngay đầu trang | ✅ | `harness_banner.png` |
| Badge (3-5) | ✅ | 6 badge bao gồm version, license, stars |
| Quick Start (≤5 bước) | ⚠️ | Có phần Installation nhưng không đặt tên "Quick Start" |
| Section cài đặt | ✅ | Marketplace + cài trực tiếp |
| Ví dụ sử dụng | ✅ | 8 ví dụ prompt chi tiết |
| Link Contributing | ❌ | Không có CONTRIBUTING.md hoặc link |
| License | ✅ | Apache 2.0 |
| GIF/screencast demo | ❌ | Không có demo động cho thấy plugin hoạt động |

#### Khuyến nghị

| # | Khuyến nghị | Tác động | Công sức |
|---|---------------|--------|--------|
| R1 | **Thêm GIF/screencast demo** cho thấy Harness sinh đội agent từ một prompt. Đặt ngay sau tagline. Đây là yếu tố hình ảnh có tác động cao nhất cho GitHub Trending — người xem quyết định trong 3 giây. | **Cao** | **Trung bình** |
| R2 | **Đổi tên section cài đặt thành "Quick Start"** và đảm bảo ≤5 bước có số thứ tự. Bước đầu nên là một lệnh copy-paste một dòng. | **Trung bình** | **Thấp** |
| R3 | **Thêm section "Contributing"** ở cuối README link tới CONTRIBUTING.md (xem R7). | **Trung bình** | **Thấp** |

---

### 2. Cấu trúc repo (4/10)

| Mục | Trạng thái |
|------|--------|
| `.github/ISSUE_TEMPLATE/` | ❌ Thiếu |
| `.github/PULL_REQUEST_TEMPLATE.md` | ❌ Thiếu |
| `CONTRIBUTING.md` | ❌ Thiếu |
| `CODE_OF_CONDUCT.md` | ❌ Thiếu |
| `.gitignore` | ✅ Có (tối giản) |
| Git tag / GitHub Releases | ❌ Không có tag |
| GitHub Topics | ❌ Chưa đặt |
| LICENSE | ✅ Có |
| CHANGELOG.md | ✅ Có |

#### Khuyến nghị

| # | Khuyến nghị | Tác động | Công sức |
|---|---------------|--------|--------|
| R4 | **Tạo GitHub Releases** với tag `v1.0.0` và `v1.0.1`. Release hiện ở sidebar và báo hiệu độ trưởng thành của project. Đưa release notes từ CHANGELOG.md. | **Cao** | **Thấp** |
| R5 | **Thêm issue template** — tối thiểu: `bug_report.yml`, `feature_request.yml`. Giảm rào cản cho contributor lần đầu và báo hiệu sẵn sàng cho cộng đồng. | **Cao** | **Thấp** |
| R6 | **Thêm PR template** (`.github/PULL_REQUEST_TEMPLATE.md`) với checklist: mô tả, test, screenshot. | **Trung bình** | **Thấp** |
| R7 | **Thêm CONTRIBUTING.md** — dù ngắn, cần có: cách báo bug, cách gửi PR, thiết lập môi trường phát triển. Quan trọng cho trending vì người xem mới tìm cái này. | **Cao** | **Thấp** |
| R8 | **Thêm CODE_OF_CONDUCT.md** — dùng template Contributor Covenant. GitHub hiện badge "Code of Conduct" trong community profile. | **Trung bình** | **Thấp** |
| R9 | **Đặt GitHub Topics** cho repo: `claude-code`, `claude-code-plugin`, `agent-team`, `ai-agent`, `llm`, `skill-generation`, `orchestration`, `claude`. Topics dẫn dắt tìm kiếm GitHub và đề xuất "Explore". | **Cao** | **Thấp** |

---

### 3. Tín hiệu tin cậy (3/10)

| Mục | Trạng thái |
|------|--------|
| CI/CD (GitHub Actions) | ❌ Không có |
| Test | ❌ Không có test suite |
| Docs site | ⚠️ Có landing page nhưng không có docs riêng |
| Commit gần đây | ✅ Hoạt động (nhiều commit trong 2 ngày gần nhất) |
| Thời gian phản hồi issue | N/A (chưa có issue) |

#### Khuyến nghị

| # | Khuyến nghị | Tác động | Công sức |
|---|---------------|--------|--------|
| R10 | **Thêm workflow CI cơ bản bằng GitHub Actions** — dù chỉ đơn giản kiểm định YAML/JSON, chạy linter markdown, hoặc kiểm tra plugin.json hợp lệ. Badge CI xanh trong README là tín hiệu tin cậy mạnh. | **Cao** | **Thấp** |
| R11 | **Thêm test kiểm định** — plugin đã đề cập "kiểm thử dry-run" và "so sánh with-skill vs without-skill". Đóng gói tối thiểu một smoke test kiểm định cấu trúc plugin (schema plugin.json, SKILL.md tồn tại, references tồn tại). | **Cao** | **Trung bình** |
| R12 | **Deploy landing page lên GitHub Pages** — bật Pages cho repo để `index.html` chạy live tại `revfactory.github.io/harness`. Thêm URL vào section "About" của repo. Việc này cũng kiêm luôn vai trò docs site. | **Cao** | **Thấp** |

---

### 4. Khả năng được tìm thấy (7/10)

| Mục | Trạng thái |
|------|--------|
| GitHub Topics | ❌ Chưa đặt |
| SEO description (repo About) | ⚠️ Chưa rõ — cần đặt qua GitHub UI |
| Ảnh social preview | ❌ Chưa đặt (dùng mặc định tự sinh của GitHub) |
| README đa ngôn ngữ | ✅ EN, KO, JA |
| Landing page | ✅ `index.html` có i18n |

#### Khuyến nghị

| # | Khuyến nghị | Tác động | Công sức |
|---|---------------|--------|--------|
| R13 | **Đặt description repo** trong section "About" của GitHub: "Agent Team & Skill Architect — A Claude Code Plugin that designs domain-specific agent teams and generates skills" | **Cao** | **Thấp** |
| R14 | **Upload ảnh social preview** (1280×640px) qua Settings → Social preview. Quyết định cách repo hiện khi share trên Twitter/X, Discord, Slack, v.v. Dùng ảnh banner chỉnh sang tỷ lệ 2:1. | **Cao** | **Thấp** |
| R15 | **Đặt website URL** trong About repo tới URL GitHub Pages (xem R12). | **Trung bình** | **Thấp** |

---

## Ma trận ưu tiên (10 hành động hàng đầu)

Sắp xếp theo tỷ lệ Tác động ÷ Công sức để sẵn sàng trending tối đa:

| Ưu tiên | Rec | Hành động | Tác động | Công sức |
|:--------:|:---:|--------|--------|--------|
| 1 | R4 | Tạo GitHub Releases (v1.0.0, v1.0.1) | Cao | Thấp |
| 2 | R9 | Đặt GitHub Topics | Cao | Thấp |
| 3 | R13 | Đặt description repo | Cao | Thấp |
| 4 | R14 | Upload ảnh social preview | Cao | Thấp |
| 5 | R12 | Deploy landing page lên GitHub Pages | Cao | Thấp |
| 6 | R5 | Thêm issue template | Cao | Thấp |
| 7 | R7 | Thêm CONTRIBUTING.md | Cao | Thấp |
| 8 | R10 | Thêm workflow CI kèm badge | Cao | Thấp |
| 9 | R1 | Thêm GIF/screencast demo | Cao | Trung bình |
| 10 | R11 | Thêm test kiểm định | Cao | Trung bình |

---

## Tổng kết

Repo Harness có **nền tảng vững** — README có cấu trúc tốt với hỗ trợ đa ngôn ngữ, landing page hoàn thiện, và bằng chứng thử nghiệm A/B là điểm khác biệt nổi bật. Khoảng trống chính nằm ở **hạ tầng cộng đồng** (không có issue template, PR template, CONTRIBUTING.md, CODE_OF_CONDUCT.md) và **tín hiệu tin cậy** (không CI/CD, không test, không release/tag). Tin tốt là phần lớn các sửa có tác động cao lại tốn ít công sức — đặt topics, tạo release, thêm template, và deploy landing page lên GitHub Pages đều có thể làm trong một buổi và sẽ nâng điểm tổng từ **5.5 lên ~8/10**.
