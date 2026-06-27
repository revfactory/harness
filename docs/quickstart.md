# Quickstart — 5 Phút Để Có Harness Đầu Tiên

> **Ngân sách thời gian: 5 phút (nghiêm ngặt).** Nếu sau 5 phút bạn chưa tới Bước 5, hãy dừng lại và mở issue — đó là bug của tài liệu này, không phải lỗi của bạn.

<!-- TODO: Loom embed — bản ghi màn hình 60s hiển thị Bước 1→5 toàn trình. Thay comment này bằng `<iframe>` sau khi ghi xong. -->

**Bạn sẽ có được gì cuối bài:** một thư mục `.claude/agents/` hoạt động với 3–5 agent chuyên biệt theo lĩnh vực, được sinh từ một prompt một câu, sẵn sàng chạy trên một nhiệm vụ mẫu.

**Yêu cầu trước (kiểm tra trước khi bắt đầu):**
- Claude Code **v2.x hoặc mới hơn** (`claude --version` phải trả về `2.x` hoặc cao hơn)
- Một shell giữ được `export` qua các lệnh (bash, zsh, hoặc fish)
- Có thể truy cập mạng tới `github.com` và `api.anthropic.com`

---

## Bước 1 — Thêm marketplace (60 giây)

```bash
claude plugin marketplace add revfactory/harness
```

**Việc này làm gì:** Đăng ký marketplace `harness` để Claude Code có thể tìm thấy các plugin do `revfactory` công bố.

**Output mong đợi:** `Added marketplace: revfactory/harness`

---

## Bước 2 — Cài plugin và bật Experimental flag (40 giây)

```bash
claude plugin install harness@harness
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

*(Để giữ flag này qua các session shell, thêm dòng `export` vào `~/.zshrc` hoặc `~/.bashrc`.)*

**Việc này làm gì:** Cài plugin `harness` từ marketplace `harness`, sau đó bật Agent Teams — API của Claude Code mà harness dùng để điều phối quy trình multi-agent. Xem [`docs/experimental-dependency.md`](./experimental-dependency.md) để hiểu vì sao cần flag này.

**Failure FAQ #1 — `AGENT_TEAMS not found` / đội không khởi tạo được**
**Nguyên nhân:** Phiên bản Claude Code cũ hơn v2.x (Agent Teams được giới thiệu từ v2.0).
**Cách sửa:** Chạy `claude --version`. Nếu dưới 2.0, nâng cấp qua `npm i -g @anthropic-ai/claude-code` (hoặc installer của distro bạn), rồi làm lại Bước 2.

---

## Bước 3 — Sinh harness từ một câu (2 phút)

```bash
claude "build a harness for a fintech risk-assessment team"
```

**Việc này làm gì:** Gọi meta-skill `/harness:harness`, phân tích câu mô tả lĩnh vực của bạn và scaffold một đội agent chuyên biệt + skill của chúng vào `.claude/agents/` và `.claude/skills/` trong thư mục hiện tại.

**Thử các prompt thay thế sau** — cái nào cũng chạy được:
- `claude "하네스 구성해줘 — 핀테크 리스크 평가 팀"` (tiếng Hàn cũng dùng được)
- `claude "build a harness for an e-commerce fraud-detection workflow"`
- `claude "design an agent team for technical due diligence on open-source repos"`

> **Phiên bản tiếng Việt:** `claude "xây dựng harness cho đội đánh giá rủi ro fintech"`

**Output mong đợi:** Một kế hoạch hiển thị dạng streaming, sau đó xác nhận đã ghi 3–5 file `.md` agent và skill của chúng.

**Failure FAQ #2 — Prompt tiếng Hàn không trả về gì / prompt tiếng Anh thành công nhưng tiếng Hàn thì không**
**Nguyên nhân:** Sai định tuyến locale hoặc tokenizer; orchestrator của harness khớp theo từ khóa trigger tiếng Hàn ("하네스 구성"), được build sẵn trong định nghĩa skill.
**Cách sửa:** Nếu tiếng Hàn thất bại, chạy lại với prompt tiếng Anh trên — skill nền tảng giống nhau. Nếu cả hai đều thất bại, chuyển sang Failure FAQ #3.

---

## Bước 4 — Xác minh file đã sinh ra (30 giây)

```bash
ls -la .claude/agents/
ls -la .claude/skills/
```

**Việc này làm gì:** Xác nhận meta-skill đã ghi file vào đúng vị trí mong đợi.

**Output mong đợi:** 3–5 file mỗi thư mục, tên phản ánh lĩnh vực của bạn (ví dụ: `risk-analyst.md`, `compliance-reviewer.md`, `portfolio-monitor.md` cho ví dụ fintech).

**Failure FAQ #3 — "Không sinh ra gì" / thư mục trống**
**Nguyên nhân:** Plugin chưa được cài thực sự hoặc không active trong dự án hiện tại.
**Cách sửa:** Chạy `claude plugin list`. Nếu không thấy `harness@harness`, làm lại Bước 2. Nếu có nhưng inactive, chạy `claude plugin enable harness@harness`, rồi làm lại Bước 3.

---

## Bước 5 — Chạy một nhiệm vụ mẫu với đội mới (90 giây)

Copy một prompt kiểu Jira ticket thực tế và đưa cho đội mới của bạn:

```bash
claude "Ticket FIN-427: A new corporate customer (mid-cap manufacturer, \$80M revenue, South Korea) has applied for a \$5M working-capital line. Produce a risk assessment covering (1) credit-history red flags, (2) sector concentration vs. our existing book, (3) regulatory exposure (KFTC, FSC). Output: a 1-page memo with a go/no-go recommendation."
```

**Việc này làm gì:** Claude Code phát hiện agent mới trong `.claude/agents/`, định tuyến nhiệm vụ qua các mẫu đội mà harness đã sinh (thường là Producer-Reviewer hoặc Expert-Pool cho công việc đánh giá rủi ro), và trả về một memo có cấu trúc.

**Failure FAQ #4 — "Đội không thực thi / chỉ một agent phản hồi"**
**Nguyên nhân:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` được đặt ở shell chạy Bước 3 nhưng không có ở shell chạy Bước 5 (xảy ra khi mở terminal mới).
**Cách sửa:** Export lại ở shell hiện tại: `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, rồi chạy lại Bước 5. Để giữ vĩnh viễn, thêm dòng này vào file rc của shell.

**Failure FAQ #5 — "Quá nhiều API call / lo ngại về chi phí"**
**Nguyên nhân:** Đội multi-agent có thể fan-out tới 5+ lệnh gọi Claude song song mỗi nhiệm vụ. Một ticket phức tạp có thể tốn 50K–200K token.
**Cách sửa:** Giới hạn một nhiệm vụ mỗi lần chạy (không chain nhiều lệnh gọi harness bằng `&&`), và dùng flag `--max-turns` nếu phiên bản Claude Code của bạn hỗ trợ. Với production, đặt cổng kiểm soát chi phí trước khi gọi harness — xem `docs/cost-controls.md` *(sắp ra mắt)*.

---

## Hoàn tất

Tới đây bạn nên có:

- [x] Một thư mục `.claude/agents/` với agent chuyên biệt theo lĩnh vực
- [x] Một thư mục `.claude/skills/` với skill hỗ trợ của chúng
- [x] Một lần thực thi nhiệm vụ mẫu thành công
- [x] Một môi trường `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` hoạt động

**Đọc tiếp:**
- [`docs/experimental-dependency.md`](./experimental-dependency.md) — Vì sao cần flag này, và chúng tôi sẽ làm gì khi nó thay đổi
- [`revfactory/harness-100`](https://github.com/revfactory/harness-100) — Danh mục 100+ harness theo lĩnh vực dựng sẵn, nếu bạn muốn clone thay vì sinh
- [`revfactory/claude-code-harness`](https://github.com/revfactory/claude-code-harness) — Harness thử nghiệm A/B chúng tôi dùng để đo +60% chất lượng trên 15 nhiệm vụ

**Nếu gặp vấn đề tài liệu này chưa đề cập:** mở issue với label `quickstart-gap` và kèm: (a) bước nào thất bại, (b) `claude --version`, (c) thông báo lỗi chính xác. SLA cho issue `quickstart-gap` là **48 giờ** cho phản hồi lần đầu (xem `CONTRIBUTING.md`).
