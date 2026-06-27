# Kế hoạch ra mắt tích hợp GitHub Trending — Harness

> **Dự án**: Harness — Agent Team & Skill Architect (Claude Code Plugin)
> **GitHub**: https://github.com/revfactory/harness
> **Ngày viết**: 2026-03-29
> **Ngày ra mắt mục tiêu**: 2026-04-07 (Thứ Ba)
> **Cơ sở viết**: tổng hợp sản phẩm của repo-auditor, content-creator, community-scout

---

## 1. Tóm tắt chiến lược

### Mục tiêu
- **Chính**: Vào Top 25 GitHub Trending (All Languages)
- **Phụ**: Vào #1 GitHub Trending (Markdown / Misc)
- **Vươn xa**: Giữ Hacker News Front Page hơn 12 giờ

### Category mục tiêu
- GitHub Trending: `All Languages` + `Unknown languages` (vì dựa trên Markdown nên khả năng cao bị phân loại ngôn ngữ là Unknown/Misc)
- Hacker News: `Show HN`
- Product Hunt: `AI Coding Agents` / `Developer Tools`

### KPI cốt lõi

| Chỉ số | D-Day +6h | D-Day +24h | D+3 | D+7 | D+14 |
|------|-----------|------------|-----|-----|------|
| GitHub Stars | 100+ | 300+ | 500+ | 800+ | 1.200+ |
| Star Velocity (stars/h) | 15-20 | 10-15 | 5-8 | 3-5 | 2-3 |
| Forks | 10+ | 30+ | 50+ | 80+ | 120+ |
| HN Points | 50+ | 100+ | — | — | — |
| Twitter Impressions | 10k+ | 50k+ | 100k+ | — | — |

### Lý do chọn ngày ra mắt
- Chọn **Thứ Ba (2026-04-07)**
  - Thứ Ba-Năm là ngày tối ưu nhất để vào GitHub Trending (đảm bảo đà tăng trước khi traffic giảm vào cuối tuần)
  - Loại Thứ Hai: đầu tuần công việc quá tải làm phân tán sự quan tâm của developer
  - Khung giờ tối ưu của HN khớp tốt nhất với Thứ Ba
  - D-7 = 31/3 (Thứ Ba), thời gian chuẩn bị tập trung vào ngày làm việc nên hiệu quả cao

---

## 2. D-7 ~ D-1: Chuẩn bị trước ra mắt

### D-7 (31/3, Thứ Ba) — Tối ưu cốt lõi repo

| # | Hành động | Cơ sở | Tiêu chí hoàn thành | Thời gian |
|---|------|------|-----------|------|
| 1 | **Tạo GitHub Releases** (v1.0.0, v1.0.1) | Audit R4 — tín hiệu tin cậy ở sidebar, ROI cao nhất | Trang Release hiện 2 release, có nội dung CHANGELOG | 30 phút |
| 2 | **Đặt GitHub Topics** | Audit R9 — cốt lõi để hiện trong search/Explore | Hoàn tất đặt `claude-code`, `claude-code-plugin`, `agent-team`, `ai-agent`, `llm`, `skill-generation`, `orchestration`, `claude` | 10 phút |
| 3 | **Đặt Repo Description** | Audit R13 — tối ưu hiện trong kết quả tìm kiếm | "Agent Team & Skill Architect — A Claude Code Plugin that designs domain-specific agent teams and generates skills" | 5 phút |
| 4 | **Upload ảnh Social Preview** | Audit R14 — tác động hình ảnh khi share SNS | Upload xong ảnh OG 1280×640px | 30 phút |
| 5 | **Deploy GitHub Pages** | Audit R12 — landing page live + tín hiệu tin cậy | Truy cập được `revfactory.github.io/harness` | 20 phút |
| 6 | **Đặt website URL trong Repo About** | Audit R15 | Đã link URL Pages | 5 phút |

**Thời gian D-7**: ~2 giờ
**Hiệu quả D-7**: Score 5.5 → 7.0 (cải thiện mạnh Discoverability)

### D-6 (1/4, Thứ Tư) — Hạ tầng cộng đồng

| # | Hành động | Cơ sở | Tiêu chí hoàn thành | Thời gian |
|---|------|------|-----------|------|
| 7 | **Thêm Issue Templates** (`bug_report.yml`, `feature_request.yml`) | Audit R5 | 2 file trong `.github/ISSUE_TEMPLATE/` | 30 phút |
| 8 | **Thêm PR Template** | Audit R6 | Tạo `.github/PULL_REQUEST_TEMPLATE.md` | 15 phút |
| 9 | **Viết CONTRIBUTING.md** | Audit R7 — cốt lõi để dẫn dắt contribute từ khách mới | Có section báo bug, hướng dẫn PR, môi trường phát triển | 30 phút |
| 10 | **Thêm CODE_OF_CONDUCT.md** | Audit R8 | Áp dụng template Contributor Covenant | 10 phút |
| 11 | **Đổi tên section "Quick Start" trong README** | Audit R2 | Section cài đặt → "Quick Start" (≤5 bước, bước đầu một dòng) | 15 phút |
| 12 | **Thêm section "Contributing" trong README** | Audit R3 | Có link tới CONTRIBUTING.md | 10 phút |

**Thời gian D-6**: ~2 giờ
**Hiệu quả D-6**: Score 7.0 → 7.5 (cải thiện mạnh Repo Structure)

### D-5 (2/4, Thứ Năm) — Tín hiệu tin cậy & CI

| # | Hành động | Cơ sở | Tiêu chí hoàn thành | Thời gian |
|---|------|------|-----------|------|
| 13 | **Thêm workflow CI GitHub Actions** | Audit R10 — badge CI xanh là tín hiệu tin cậy mạnh | Thêm markdown lint + kiểm định plugin.json + badge vào README | 1 giờ |
| 14 | **Thêm test kiểm định cơ bản** | Audit R11 | Kiểm định schema plugin.json, xác nhận SKILL.md tồn tại, kiểm định thư mục references | 1 giờ |

**Thời gian D-5**: ~2 giờ
**Hiệu quả D-5**: Score 7.5 → 8.0 (cải thiện lớn Trust Signals)

### D-4 (3/4, Thứ Sáu) — Chuẩn bị nội dung & xây dựng quan hệ trước

| # | Hành động | Phân loại | Tiêu chí hoàn thành | Thời gian |
|---|------|------|-----------|------|
| 15 | **Tạo GIF/Screencast demo** | Audit R1 — quyết định trong 3 giây phán đoán | GIF 30-60s "build a harness" → quá trình tạo agent team | 2 giờ |
| 16 | **Đặt GIF demo lên đầu README** | | Ngay dưới tagline | 15 phút |
| 17 | **Chuẩn bị 3-4 ảnh cho chuỗi Twitter/X** | Content #3 | Sơ đồ workflow, chart kết quả A/B, card mẫu kiến trúc | 1 giờ |
| 18 | **Soát toàn bộ text nội dung lần cuối** | | Kiểm tra ngữ pháp + link bản nháp HN/Reddit/Twitter/Dev.to | 30 phút |
| 19 | **Bắt đầu sắp xếp hunter Product Hunt** | Scout — bắt buộc cho launch PH | DM 2-3 hunter, chia sẻ ngày dự kiến ra mắt | 30 phút |
| 20 | **DM trước influencer** | Scout Tier 1 KOL | Message giới thiệu trước cho Nick Saraev, Boris Cherny | 30 phút |

**Thời gian D-4**: ~5 giờ (ngày làm việc nhiều nhất)

### D-3 ~ D-2 (4/4~5/4, Thứ Bảy~Chủ Nhật) — Kiểm tra cuối & chuẩn bị supporter

| # | Hành động | Tiêu chí hoàn thành | Thời gian |
|---|------|-----------|------|
| 21 | **Xác nhận repo harness-100 công khai** | README chuẩn chỉnh, link hoạt động đúng | 30 phút |
| 22 | **Xác nhận claude-code-harness (repo nghiên cứu) công khai** | Truy cập được dữ liệu/bài báo thử nghiệm A/B | 30 phút |
| 23 | **Lập nhóm supporter ban đầu** | Yêu cầu 5-10 đồng nghiệp/người quen hỗ trợ star/upvote ngày ra mắt. Tính theo timezone để đảm bảo có người tham gia vào tối~đêm KST | 1 giờ |
| 24 | **Chuẩn bị trước câu trả lời cho câu hỏi dự kiến trên HN** | Nháp 5-7 Q&A về hạn chế phương pháp luận, so sánh công cụ khác, khả năng tổng quát hóa | 1 giờ |
| 25 | **Kiểm tra hoạt động tài khoản Anthropic Discord** | Xác nhận truy cập được channel #showcase | 15 phút |

### D-1 (6/4, Thứ Hai) — Tổng duyệt cuối cùng

| # | Hành động | Tiêu chí hoàn thành | Thời gian |
|---|------|-----------|------|
| 26 | **Kiểm tra lại toàn bộ checklist** (xem Section 8) | Đã check mọi mục Pre-Launch | 30 phút |
| 27 | **Kiểm tra lần cuối GitHub Pages live** | Landing page truy cập được + toggle đa ngôn ngữ hoạt động | 10 phút |
| 28 | **Copy text đăng từng platform vào text editor** | Sẵn sàng copy-paste (tránh vỡ định dạng) | 20 phút |
| 29 | **Cập nhật bio profile Twitter** | Thêm nhắc đến Harness | 5 phút |
| 30 | **Đặt báo thức** | Báo thức dậy ngày D-Day (KST 16:00 = UTC 07:00) | 5 phút |

---

## 3. D-Day: Thực thi ra mắt (7/4, Thứ Ba)

### Chiến lược theo khung giờ

Nguyên lý cốt lõi: **Traffic HN/Reddit đạt đỉnh vào sáng Mỹ (UTC 13:00-16:00 = PST 6-9h sáng = EST 9h sáng-12h trưa)**. Nhưng HN cần **đăng sớm vài giờ để thời điểm đạt Front Page khớp với đỉnh traffic**. Tính theo khung tối~đêm KST.

| Giờ (UTC) | Giờ (KST) | Platform | Hành động | Hiệu quả dự kiến | Plan B |
|-----------|-----------|--------|------|-----------|--------|
| **07:00** | **16:00** | GitHub | Kiểm tra README lần cuối, xác nhận GIF demo hoạt động | Kiểm tra cơ bản | — |
| **08:00** | **17:00** | **Hacker News** | Đăng bài Show HN (text Content #1) | HN New → Rising. 2-3 upvote ban đầu để vào Rising | Nếu timing không hợp, đăng lại lúc UTC 12:00 (HN cho phép đăng lại) |
| **08:15** | **17:15** | **Supporter ban đầu** | Chia sẻ link HN + link GitHub cho nhóm supporter | 5-10 star ban đầu + 2-3 upvote HN (đà tới hạn) | Nếu thiếu supporter, huy động thêm network cá nhân |
| **08:30** | **17:30** | **Twitter/X** | Đăng chuỗi launch (Content #3, Tweet 1-9). Pin Tweet 1 | Engagement ban đầu từ follower, lan tỏa qua retweet | Nếu engagement chuỗi thấp, đăng lại riêng tweet cốt lõi |
| **09:00** | **18:00** | **r/ClaudeAI** | Đăng bài Reddit (Content #2a) | Cộng đồng mục tiêu tiếp nhận tốt nhất. Mục tiêu 50+ upvote | Nếu bài bị xóa, hỏi moderator rồi điều chỉnh tông đăng lại |
| **09:00** | **18:00** | **r/SideProject** | Đăng bài Reddit (Template D của Scout) | Cộng đồng cho phép tự quảng bá, traction ban đầu an toàn | — |
| **09:30** | **18:30** | **r/opensource** | Đăng bài Reddit | Hiện diện ở cộng đồng mã nguồn mở | — |
| **10:00** | **19:00** | **r/programming** | Đăng bài Reddit (Content #2c) | Đối tượng developer rộng. Cách nhau 1 giờ để tránh bị đánh dấu spam | Nếu bị xóa, viết lại bản nhấn mạnh giá trị kỹ thuật |
| **10:00** | **19:00** | **Product Hunt** | Ra mắt PH (qua hunter hoặc trực tiếp) — category "AI Coding Agents" | Mục tiêu Top 5 PH Daily | Nếu chưa có hunter, ra mắt trực tiếp, viết comment Maker ngay |
| **10:30** | **19:30** | **Anthropic Discord** | Chia sẻ project ở channel #showcase | Tiếp cận trực tiếp cộng đồng Claude | Channel thay thế #community-projects |
| **12:00** | **21:00** | **Dev.to** | Đăng bài blog kỹ thuật (Content #4) | SEO dài hạn, lưu lượng từ search | — |
| **12:00** | **21:00** | **Theo dõi HN** | Kiểm tra có vào Front Page chưa. Bắt đầu trả lời comment | Engagement comment là yếu tố cốt lõi ranking HN | Nếu không vào Front Page → tập trung Reddit/Twitter |
| **13:00-18:00** | **22:00-03:00** | **Toàn bộ platform** | Theo dõi thời gian thực + trả lời comment (chi tiết dưới) | Khung giờ đỉnh ở Mỹ, 6 giờ quan trọng nhất | Nếu mệt, chỉ tập trung platform cốt lõi (HN + r/ClaudeAI) |
| **14:00** | **23:00** | **Awesome Lists Tier 1** | Gửi issue awesome-claude-code (hesreallyhim) + PR jqueryscript + 2 PR awesome-claude-skills | Gửi PR đồng thời với lúc vào trending → tối đa xác suất duyệt | — |

### Chỉ số theo dõi thời gian thực & ngưỡng

| Chỉ số | Tần suất check | Xanh (bình thường) | Vàng (cần lưu ý) | Đỏ (cấp bách) |
|------|----------|------------|------------|------------|
| Star velocity | 30 phút | >10 stars/h | 5-10 stars/h | <5 stars/h |
| HN rank | 30 phút | Front Page (1-30) | Page 2 (31-60) | Page 3+ |
| HN comments | 1 giờ | 5+ comment/h | 2-4 comment/h | <2 comment/h |
| Reddit upvote (r/ClaudeAI) | 1 giờ | 50+ | 20-50 | <20 |
| Twitter thread impressions | 2 giờ | 5k+ | 1-5k | <1k |

### Kịch bản ứng phó cấp bách (Plan B)

| Kịch bản | Trigger | Hành động ngay |
|---------|--------|----------|
| Sau 3 giờ đăng HN vẫn chưa vào Front Page | Points < 10 lúc UTC 11:00 | Tập trung Reddit/Twitter. Xem xét đăng lại HN vào ngày hôm sau |
| Bài Reddit bị xóa | Nhận thông báo moderator xóa | Xem lại quy tắc subreddit đó → sửa tông rồi gửi modmail xin duyệt lại |
| Star velocity < 5/h (toàn kênh) | Thời điểm D-Day +6h | DM cấp bách influencer (Nick Saraev, Boris Cherny) + huy động lần 2 supporter |
| Nhiều comment tiêu cực | 3+ comment phản biện | Trả lời ngay lập tức, lễ độ. Thừa nhận hạn chế kỹ thuật + chia sẻ roadmap. Tuyệt đối không phòng thủ |

---

## 4. D+1 ~ D+3: Khuếch đại

### D+1 (8/4, Thứ Tư)

| Giờ (UTC) | Hành động | Platform | Điều kiện trigger |
|-----------|------|--------|------------|
| 08:00 | **Bài r/MachineLearning** (Content #2b — tập trung nghiên cứu) | Reddit | Thực hiện vô điều kiện |
| 10:00 | **Quote-tweet Twitter**: "Phần gây bất ngờ nhất trong kết quả nghiên cứu..." — nhấn mạnh phát hiện về scaling | Twitter/X | Thực hiện vô điều kiện |
| 10:00 | **Gửi vote cộng đồng Ben's Bites** | Newsletter | Thực hiện vô điều kiện |
| 12:00 | **Bài theo dõi Anthropic Discord** — chia sẻ phản ứng cộng đồng | Discord | Khi đạt 100+ star |
| 14:00 | **Trả lời comment HN sâu hơn** — trả lời chi tiết câu hỏi kỹ thuật | HN | Khi đang giữ Front Page HN |
| Liên tục | **Trả lời mọi GitHub Issues trong 24 giờ** | GitHub | Khi nhận issue |

### D+2 (9/4, Thứ Năm)

| Giờ (UTC) | Hành động | Platform | Điều kiện trigger |
|-----------|------|--------|------------|
| 08:00 | **Liên hệ team biên tập TLDR AI / TLDR Open Source** | Email | Tăng pitch khi đạt 200+ star |
| 10:00 | **Liên hệ team biên tập The Rundown AI** | Email | Thực hiện vô điều kiện |
| 10:00 | **Gửi Console.dev** | Web | Thực hiện vô điều kiện |
| 12:00 | **Cross-post r/LocalLLaMA** (bản kỹ thuật sâu) | Reddit | Khi r/ClaudeAI phản ứng tích cực |
| 14:00 | **Bài r/artificial** | Reddit | Thực hiện vô điều kiện |

### D+3 (10/4, Thứ Sáu)

| Giờ (UTC) | Hành động | Platform | Điều kiện trigger |
|-----------|------|--------|------------|
| 08:00 | **Bài riêng Twitter: "100 harnesses"** — giới thiệu companion repo | Twitter/X | Thực hiện vô điều kiện |
| 10:00 | **Gửi Changelog Weekly** | Newsletter | Thực hiện vô điều kiện |
| 12:00 | **Gửi AI Tool Report** | Newsletter | Thực hiện vô điều kiện |
| 14:00 | **Đăng ký project tại Star History** + embed graph star vào README | GitHub/Web | Graph ấn tượng khi đạt 300+ star |
| Liên tục | **Tweet mốc quan trọng**: "Launched 3 days ago → X stars" | Twitter/X | Khi đạt 500+ star |

---

## 5. D+4 ~ D+14: Duy trì

### D+4 ~ D+7 (11/4~14/4)

| Ngày | Hành động | Platform |
|------|------|--------|
| D+4 (Thứ Bảy) | **Gửi PR Awesome Lists Tier 2**: awesome-llm-agents, awesome-agents, awesome-ai-agents, awesome-ai-agents-2026, Awesome-Prompt-Engineering | GitHub |
| D+5 (Chủ Nhật) | **Bài Dev.to theo dõi**: "5 Architecture Patterns for AI Agent Teams" (nội dung lâu bền) | Dev.to |
| D+5 | **Liên hệ nhà sáng tạo YouTube**: Nick Saraev (ưu tiên cao nhất), Sabrina Ramonov, freeCodeCamp | Email/DM |
| D+6 (Thứ Hai) | **Kiểm tra badge Trendshift và embed vào README** | GitHub |
| D+7 (Thứ Ba) | **Tweet mốc hàng tuần**: "Week 1: X stars, Y forks, Z countries" + graph Star History | Twitter/X |
| D+7 | **Đăng ký awesomeclaude.ai** | Web |

### D+8 ~ D+14 (15/4~21/4)

| Ngày | Hành động | Platform |
|------|------|--------|
| D+8~10 | **Gửi PR Awesome Lists Tier 3**: jim-schwoebel, webfuse-com, BehiSecc, alvinunreal | GitHub |
| D+10 | **Liên hệ newsletter Superhuman AI, The Neuron** | Email |
| D+10 | **Bài theo dõi showcase r/MachineLearning** (phản ánh use case thực tế + phản hồi cộng đồng) | Reddit |
| D+12 | **Chuỗi tweet highlight phản hồi người dùng** — "Here's what people are building with Harness" | Twitter/X |
| D+14 | **Tweet mốc 2 tuần** + chia sẻ roadmap (kế hoạch phiên bản tiếp theo) | Twitter/X |
| Liên tục | **Duy trì trả lời mọi GitHub Issues/PR trong 48 giờ** | GitHub |
| Liên tục | **Trả lời mọi mention/quote Twitter** | Twitter/X |

### Nguyên tắc duy trì cộng đồng dài hạn

1. **Quy tắc trả lời issue 24-48 giờ**: Sau trending, phản hồi nhanh khi khách mới mở issue đầu tiên là yếu tố cốt lõi để hình thành cộng đồng
2. **Gắn label "Good First Issue"**: Chủ động tạo cơ hội đóng góp đơn giản để thu hút contributor
3. **Cập nhật CHANGELOG liên tục**: Ghi chú chi tiết mỗi release tạo cảm giác project hoạt động sôi nổi
4. **Bài cập nhật hàng tháng**: Chia sẻ tiến độ tại r/ClaudeAI + Twitter

---

## 6. Chỉ số thành công

### Mục tiêu Star Velocity (theo khung giờ)

| Thời điểm | Star tích lũy | Velocity (stars/h) | Tiêu chí ngưỡng Trending |
|------|-----------|-------------------|-------------------|
| D-Day +2h | 20-30 | 10-15 | Bắt đầu vào |
| D-Day +6h | 80-120 | 15-20 | Ứng viên Daily Trending |
| D-Day +12h | 150-200 | 10-15 | Vào Daily Trending |
| D-Day +24h | 250-350 | 8-12 | Ổn định ở Daily Trending |
| D+2 | 400-500 | 5-8 | Ứng viên Weekly Trending |
| D+3 | 500-600 | 4-6 | Vào Weekly Trending |
| D+7 | 700-900 | 2-4 | Duy trì Weekly Trending |
| D+14 | 1.000-1.500 | 1-3 | Monthly Trending |

### Chỉ số thành công tổng hợp

| Chỉ số | D-Day | D+3 | D+7 | D+14 | Ghi chú |
|------|-------|-----|-----|------|------|
| **GitHub Stars** | 300+ | 500+ | 800+ | 1.200+ | Chỉ số cốt lõi |
| **GitHub Forks** | 30+ | 50+ | 80+ | 120+ | Proxy cho mức dùng thực tế |
| **Xếp hạng GitHub Trending** | Top 50 | Top 25 | Duy trì Top 25 hoặc vào lại | — | Mục tiêu chính |
| **HN Points** | 100+ | — | — | — | Front Page = ~50+ points |
| **HN Comments** | 30+ | — | — | — | Độ sâu engagement |
| **Product Hunt Rank** | Top 10 | — | — | — | Rank theo ngày |
| **Tổng Upvote Reddit** | 200+ | 400+ | — | — | Cộng dồn toàn subreddit |
| **Twitter Impressions** | 50k+ | 100k+ | 150k+ | — | Chuỗi + mention |
| **PR Awesome List được merge** | 2+ | 4+ | 6+ | 8+ | Khả năng tìm thấy dài hạn |
| **GitHub Issues mở** | 5+ | 10+ | 20+ | 30+ | Chỉ số sức khỏe cộng đồng |
| **Contributor** | 1 | 2+ | 3+ | 5+ | Hình thành cộng đồng |

---

## 7. Rủi ro & giảm thiểu

| # | Rủi ro | Xác suất | Tác động | Chiến lược giảm thiểu |
|---|--------|------|------|-----------|
| 1 | **HN không quan tâm** — Show HN không vào được Front Page | Trung | Cao | HN có yếu tố may rủi. Nếu thất bại, tập trung hỏa lực vào Reddit/Twitter. Xem xét đăng lại vào D+2~3. Tham gia cả thread hàng tháng "Ask HN: What are you working on?" |
| 2 | **Bài Reddit bị xóa do tự quảng bá** — moderator xóa bài | Trung | Trung | Phân biệt tông theo từng subreddit (r/ClaudeAI dùng use case, r/programming dùng giá trị kỹ thuật, r/MachineLearning dùng nghiên cứu). Có lịch sử tham gia subreddit đó trước sẽ có lợi → tham gia thông thường ở subreddit đó 1 tuần trước ra mắt |
| 3 | **Thiếu Star velocity** — không đạt ngưỡng Trending (D-Day +12h dưới 100 star) | Trung | Cao | Plan B: DM cấp bách influencer + huy động lần 2 supporter + tận dụng thêm cộng đồng khung giờ châu Á (Hàn/Nhật). Vì đã có README tiếng Nhật, đăng bài tiếng Nhật ở cộng đồng developer Nhật (Zenn, Qiita) |
| 4 | **Phản hồi kỹ thuật tiêu cực** — "đây chẳng phải chỉ là prompt?", "nghi ngờ phương pháp luận A/B test" | Trung | Trung | Trả lời lễ độ và kỹ thuật bằng Q&A đã chuẩn bị trước. Thừa nhận hạn chế thẳng thắn nhưng có dữ liệu kết quả thực tế hậu thuẫn. "You're right that X is a limitation — here's what we're working on for v2" |
| 5 | **Product Hunt kém** — không vào Top 10 Daily | Trung | Thấp | PH là kênh phụ. Dù kém cũng không ảnh hưởng trực tiếp tới GitHub Trending. Tập trung năng lượng vào HN/Reddit hơn PH |
| 6 | **Project cạnh tranh ra mắt cùng lúc** — công cụ AI agent tương tự vào Trending cùng ngày | Thấp | Trung | Nhấn mạnh điểm khác biệt của Harness (meta-skill, kết quả nghiên cứu A/B, 100 cấu hình prebuilt). Chuẩn bị sẵn comment giải thích rõ khác biệt với project cạnh tranh |
| 7 | **Bất lợi timezone của tác giả** — chênh 12-14 giờ giữa KST và khung giờ đỉnh Mỹ làm chậm phản hồi thời gian thực | Cao | Trung | Lập kế hoạch theo dõi tập trung từ tối tới rạng sáng D-Day (KST 17:00 ~ 03:00 = UTC 08:00 ~ 18:00). D+1 catch-up trả lời comment từ sáng. Trước khi ngủ để lại comment "I'll respond to all questions in the morning" |
| 8 | **Sự cố dịch vụ GitHub** — GitHub down/chậm vào ngày ra mắt | Thấp | Cao | Theo dõi trước githubstatus.com. Nếu sự cố, dời ra mắt sang ngày sau. Nội dung đã chuẩn bị nên tái sử dụng được |

---

## 8. Checklist cuối cùng

### Trước ra mắt (hoàn thành tới D-1)

**Tối ưu Repo**
- [ ] Tạo GitHub Releases v1.0.0, v1.0.1
- [ ] Đặt 8 GitHub Topics
- [ ] Đặt Repo Description
- [ ] Upload ảnh Social Preview (1280×640)
- [ ] Deploy GitHub Pages + đặt URL trong About
- [ ] Thêm Issue Templates (bug_report.yml, feature_request.yml)
- [ ] Thêm PR Template
- [ ] Viết CONTRIBUTING.md
- [ ] Thêm CODE_OF_CONDUCT.md
- [ ] Thêm workflow CI + badge xanh
- [ ] Thêm test kiểm định
- [ ] Đổi tên section "Quick Start" trong README
- [ ] Thêm section "Contributing" trong README
- [ ] Tạo GIF demo + đặt đầu README

**Nội dung**
- [ ] Chuẩn bị bản cuối text HN Show HN
- [ ] Bản cuối 4 bài Reddit (r/ClaudeAI, r/programming, r/SideProject, r/opensource)
- [ ] Chuẩn bị 9 tweet chuỗi Twitter/X + 3-4 ảnh
- [ ] Bản cuối bài Dev.to
- [ ] Nháp trang ra mắt Product Hunt (tagline, description, ảnh)
- [ ] Xác nhận mọi link nội dung hoạt động đúng

**Outreach**
- [ ] Đã có hunter Product Hunt (hoặc quyết định ra mắt trực tiếp)
- [ ] Đã gửi DM trước cho Nick Saraev, Boris Cherny
- [ ] Đã có 5-10 supporter ban đầu + xác nhận tham gia D-Day
- [ ] Hoàn thành nháp 5-7 Q&A câu hỏi dự kiến HN
- [ ] Xác nhận truy cập được Anthropic Discord

**Liên kết Repo**
- [ ] Repo harness-100 công khai + README chuẩn chỉnh
- [ ] claude-code-harness (repo nghiên cứu) công khai
- [ ] Xác nhận cross-link giữa 3 repo hoạt động đúng
- [ ] Cập nhật bio profile Twitter

### D-Day (7/4, Thứ Ba)

**Thứ tự đăng**
- [ ] UTC 08:00 — Đăng HN Show HN
- [ ] UTC 08:15 — Chia sẻ link cho nhóm supporter
- [ ] UTC 08:30 — Đăng chuỗi Twitter/X + pin
- [ ] UTC 09:00 — Đăng r/ClaudeAI + r/SideProject
- [ ] UTC 09:30 — Đăng r/opensource
- [ ] UTC 10:00 — Đăng r/programming + Product Hunt
- [ ] UTC 10:30 — Đăng Anthropic Discord #showcase
- [ ] UTC 12:00 — Đăng bài Dev.to
- [ ] UTC 14:00 — Gửi 4 PR/issue Awesome Lists Tier 1

**Theo dõi**
- [ ] Check Star velocity mỗi 30 phút
- [ ] Check HN rank mỗi 30 phút
- [ ] Check Reddit upvote mỗi 1 giờ
- [ ] Trả lời mọi comment trong 1 giờ
- [ ] Trả lời ngay GitHub Issues

### Sau ra mắt (D+1 ~ D+14)

- [ ] D+1: Bài r/MachineLearning + QT Twitter + gửi Ben's Bites
- [ ] D+2: Liên hệ TLDR/Rundown/Console.dev
- [ ] D+3: Bài riêng "100 harnesses" + gửi Changelog + đăng ký Star History
- [ ] D+4: 5 PR Awesome Lists Tier 2
- [ ] D+5: Bài Dev.to theo dõi + liên hệ nhà sáng tạo YouTube
- [ ] D+7: Tweet mốc hàng tuần
- [ ] D+8~10: 4 PR Awesome Lists Tier 3 + liên hệ newsletter Tier 3
- [ ] D+14: Mốc 2 tuần + chia sẻ roadmap

---

## Thiết kế hiệu ứng dây chuyền (Cascade)

```
D-Day 08:00  HN Show HN ──────────────┐
D-Day 08:30  Twitter Thread ────────────┤
D-Day 09:00  Reddit (r/ClaudeAI) ───────┤
D-Day 10:00  Product Hunt ──────────────┤
                                        ▼
                              Star Velocity ban đầu
                              (30-50 stars trong 3h)
                                        │
                                        ▼
                              Thuật toán GitHub Trending phát hiện
                              (ứng viên Daily Trending)
                                        │
                          ┌─────────────┼─────────────┐
                          ▼             ▼             ▼
                    Trendshift       Alpha Signal   GitNews
                    tự thu thập      tự theo dõi    tự thu thập
                          │             │             │
                          ▼             ▼             ▼
                    Traffic lần 2 → Star Velocity tăng tốc
                                        │
                                        ▼
                              Vào ổn định GitHub Trending
                              (Top 25)
                                        │
                          ┌─────────────┼─────────────┐
                          ▼             ▼             ▼
                    TLDR AI pickup  Newsletter feature  Đẩy nhanh
                    (D+2~3)        (D+3~7)       duyệt PR Awesome List
                          │             │             │
                          ▼             ▼             ▼
                    Traffic lần 3 → Đảm bảo khả năng tìm thấy dài hạn → 1.000+ Stars
```

**Cốt lõi**: mỗi giai đoạn đóng vai trò trigger cho giai đoạn tiếp theo. Star velocity 24 giờ đầu là điều kiện khởi động cho toàn bộ phản ứng dây chuyền.

---

## Tóm tắt thực thi

| Giai đoạn | Khoảng thời gian | Mục tiêu cốt lõi | Tiêu chí thành công |
|------|------|----------|----------|
| **Trước ra mắt** | D-7 ~ D-1 | Score Repo 5.5 → 8.0 | Hoàn thành 100% checklist |
| **Ra mắt** | D-Day | Đạt Star velocity > 10/h | 300+ star trong 24h |
| **Khuếch đại** | D+1 ~ D+3 | Vào Trending + lan tỏa lần 2 | Vào Top 25 + 500+ star |
| **Duy trì** | D+4 ~ D+14 | Đảm bảo khả năng tìm thấy dài hạn | 1.200+ star + 8+ Awesome List merged |

> **Mục tiêu cuối cùng**: Định vị Harness là "ví dụ tiêu biểu của Claude Code Plugin", và xây dựng nhận diện trong cộng đồng developer AI toàn cầu thông qua GitHub Trending.
