# Đóng góp cho Harness

Cảm ơn bạn đã xem xét đóng góp cho **Harness** — một nhà máy meta-skill của Claude Code chuyên thiết kế đội agent và sinh skill.

Tài liệu này bao gồm: SLA phản hồi, cách đóng góp, thiết lập môi trường phát triển, quy ước PR, quy tắc commit message, code of conduct, và danh sách maintainer.

---

## SLA phản hồi (cam kết)

Đây là mục tiêu phản hồi của maintainer cho repo này. Các chỉ số này được đặt **bảo thủ** để một team maintainer nhỏ có thể thực hiện được khi quy mô tăng lên.

| Bề mặt | Mục tiêu | Ghi chú |
|---------|--------|-------|
| PR — phản hồi lần đầu | **< 72h** | Ngày làm việc. "Phản hồi lần đầu" nghĩa là tối thiểu một label + một comment xác nhận đã nhận PR. |
| Phân loại & gắn label Issue | **< 48h** | Mọi issue mới sẽ được bỏ label `needs-triage` và gắn label loại (`bug` / `enhancement` / `question` / `discussion`) trong 48h. |
| Xử lý bug (P0 / P1) | **< 14 ngày** | P0 = mất dữ liệu / an ninh / cài đặt bị hỏng. P1 = luồng phổ biến bị hỏng. P2/P3 theo dõi trên roadmap, không có SLA cứng. |
| Báo cáo bảo mật | **< 7 ngày** | Xác nhận ban đầu trong 7 ngày. Mục tiêu patch trong 30 ngày. Xem mục **Security** dưới đây cho kênh riêng tư. |
| Nhịp release | **mỗi 2 tuần** | Gắn tag hai tuần một lần, trừ khi không có gì để release. Fix P0 có thể phát hành patch ngoài lịch. |

Nếu chúng tôi trễ SLA, hãy ping vào issue/PR — điều đó không hề thất thố, đó là vòng phản hồi đã được thống nhất.

---

## Cách đóng góp

Mỗi loại đóng góp đi qua một điểm vào khác nhau. Chọn loại phù hợp.

### Báo cáo lỗi (Bug report)

- Mở issue dùng form **Bug report** (`.github/ISSUE_TEMPLATE/bug_report.yml`).
- Bắt buộc: phiên bản Claude Code, trạng thái flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, bước tái hiện lỗi, kỳ vọng vs thực tế, OS.
- Tái hiện ngắn (< 30 dòng) là lý tưởng nhất. Nếu cần cả project để tái hiện, hãy link một fork công khai.

### Yêu cầu tính năng (Feature request)

- Mở issue dùng form **Feature request**.
- Chúng tôi mong có một đoạn ngắn "vấn đề này giải quyết điều gì". Nếu có đề xuất, hãy trình bày ở dạng sẵn sàng đưa vào PR (đề xuất này mở rộng/thay thế mẫu kiến trúc nào trong 6 mẫu?).

### Câu hỏi

- Mở issue dùng form **Question**, **hoặc** mở thread trong [GitHub Discussions](https://github.com/revfactory/harness/discussions) nếu vấn đề còn mở.

### Thảo luận (ý tưởng cỡ RFC)

- Ưu tiên GitHub Discussions. Chỉ nâng lên issue khi đã có đồng thuận cơ bản về hướng đi.

### Pull Request

- Xem **Hướng dẫn Pull Request** dưới đây.
- PR nhỏ được merge nhanh hơn. Diff > 400 dòng nên được thảo luận trước qua Discussion.

### Bảo mật

- **Không** mở issue công khai cho bất kỳ điều gì có thể bị lợi dụng.
- Email: `robin.hwang@kakaocorp.com` với tiền tố subject `[harness-security]`.
- Chúng tôi cố gắng xác nhận trong 7 ngày (xem bảng SLA).

---

## Thiết lập môi trường phát triển

### Yêu cầu trước

- Claude Code `v2.x` (cần Agent Teams API)
- Node.js `>= 18` (cho tooling cục bộ dùng trong CI)
- Git

### Cờ môi trường

Hiện tại Harness yêu cầu tính năng Agent Teams thử nghiệm của Claude Code. Đặt cờ này trong shell profile hoặc theo phiên:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Chúng tôi theo dõi phụ thuộc này tại `docs/experimental-dependency.md` (nếu Anthropic chuyển cờ này thành stable, chúng tôi sẽ cập nhật README trong 72h theo SLA trên).

### Link plugin cục bộ

Để kiểm thử thay đổi của bạn trong một phiên Claude Code cục bộ mà không cần publish lên marketplace:

```bash
# Từ checkout của bạn
claude plugin link ./harness

# Kiểm tra
claude plugin list | grep harness
```

Unlink bằng `claude plugin unlink harness` khi xong.

### Chạy meta-skill

```bash
claude "build a harness for a fintech risk-assessment team"
```

Agent và skill được scaffold sẽ nằm dưới `.claude/agents/` và `.claude/skills/` trong project đích.

### Test & lint

- Markdown lint: `npx markdownlint '**/*.md'`
- YAML lint (issue template & workflow): `npx yaml-lint .github/`
- Kiểm định metadata skill: `python scripts/validate_skills.py` (nếu có)

CI chạy các bước này trên mọi PR. Khuyến khích chạy cục bộ nhưng không bắt buộc — chúng tôi sẽ không chặn merge với các lỗi CI phát hiện nhưng dễ sửa.

---

## Hướng dẫn Pull Request

### Đặt tên branch

Dùng cấu trúc `type/short-description`:

| Tiền tố | Dùng cho | Ví dụ |
|--------|---------|---------|
| `feat/` | Tính năng mới hiển thị với người dùng | `feat/expert-pool-variance-mode` |
| `fix/` | Sửa lỗi | `fix/agent-teams-flag-detection` |
| `docs/` | Chỉ thay đổi docs | `docs/quickstart-gemini-section` |
| `refactor/` | Tái cấu trúc nội bộ, không đổi hành vi | `refactor/skill-loader-split` |
| `chore/` | Build, dependency, dọn dẹp | `chore/upgrade-markdownlint` |
| `test/` | Chỉ test | `test/fan-out-fan-in-e2e` |

### Ngôn ngữ commit message

- **Cả tiếng Hàn và tiếng Anh đều được chấp nhận.** Viết bằng ngôn ngữ bạn diễn đạt chính xác hơn.
- Nếu thay đổi sẽ xuất hiện trong CHANGELOG hoặc release notes, vui lòng cũng cung cấp title tiếng Anh trong PR description để người đọc sau có thể theo dõi.

### Template PR

Mọi nội dung PR được điền sẵn từ `.github/PULL_REQUEST_TEMPLATE.md`. Vui lòng điền:

- **Tóm tắt** (cái gì & vì sao, 2–4 câu)
- **Động lực** (link issue, tham chiếu nghiên cứu, hoặc lý do 1 dòng)
- **Phạm vi thay đổi** (checklist các bề mặt bị ảnh hưởng)
- **Test** (bạn đã chạy/thêm gì)
- **CHANGELOG** (đã cập nhật `CHANGELOG.md` chưa? Y/N/NA)
- **Tác động SemVer** (patch / minor / major — xem mục tiếp theo)

### Kỳ vọng review

- Cần ít nhất một review chấp thuận từ maintainer.
- Chúng tôi cố gắng phản hồi PR trong 72h (xem SLA). Nếu bị chặn, hãy ping.

---

## Quy ước Commit Message

Chúng tôi theo một biến thể nhẹ của **Conventional Commits**, ánh xạ trực tiếp sang SemVer.

```
<type>(<scope>)!: <short summary>

<body — optional>

<footer — optional>
```

### Loại & ánh xạ SemVer

| Loại commit | Tác động SemVer | Ví dụ |
|-------------|---------------|---------|
| `feat!:` hoặc `BREAKING CHANGE:` trong footer | **major** (ví dụ 1.x → 2.0) | `feat!: rename primary pattern "Supervisor" → "Orchestrator"` |
| `feat:` | **minor** (ví dụ 1.2 → 1.3) | `feat: add Producer-Reviewer variance metric` |
| `fix:` | **patch** (ví dụ 1.2.3 → 1.2.4) | `fix: correct flag detection on zsh` |
| `docs:` / `chore:` / `refactor:` / `test:` | không tăng version release | `docs: clarify Gemini roadmap` |

- Tóm tắt bằng tiếng Hàn cũng được: `feat: 전문가 풀 패턴에 분산 지표 추가`.
- Hậu tố `!` (hoặc footer `BREAKING CHANGE:`) là **duy nhất** trigger chính thức cho major version. Vui lòng không dùng tùy tiện.

### Gắn tag release

- Release được phát hành mỗi 2 tuần (xem SLA).
- Gắn tag được thực hiện từ `main` sau khi CI pass và CHANGELOG đã cập nhật.
- Tag theo định dạng `vMAJOR.MINOR.PATCH` (ví dụ `v1.3.0`).

---

## Quy tắc ứng xử (Code of Conduct)

Project này tuân theo **Contributor Covenant v1.4** — tóm tắt:

- Chào đón và bao trùm. Giả định ý định tốt.
- Không quấy rối, không tấn công cá nhân, không ngôn từ phân biệt.
- Phê bình ý tưởng, không phê bình con người. Hỗ trợ luận điểm bằng tham chiếu khi có thể.
- Maintainer có thể kiểm duyệt, sửa, hoặc xóa comment/commit/issue/PR vi phạm các nguyên tắc này, và có thể cấm người vi phạm.

Toàn văn: <https://www.contributor-covenant.org/version/1/4/code-of-conduct/>

Báo cáo vi phạm Code of Conduct riêng tư tới `robin.hwang@kakaocorp.com` với tiền tố subject `[harness-coc]`.

---

## Maintainer

| Vai trò | Handle | Phụ trách |
|------|--------|------|
| Lead maintainer | [@revfactory](https://github.com/revfactory) | Định hướng project, release, review cuối |
| Contributor | [@hnts03](https://github.com/hnts03) | Template skill, tài liệu tiếng Hàn |
| Contributor | [@JunghwanNA](https://github.com/JunghwanNA) | Mẫu agent, test tích hợp |
| Contributor | [@shaun0927](https://github.com/shaun0927) | Tooling, CI, infra |

Contributor mới sẽ được đưa vào danh sách này sau khi đóng góp liên tục (không phải chỉ một PR). Hãy để lại ghi chú trong Discussion nếu bạn muốn thảo luận về con đường trở thành maintainer.

---

## Giấy phép

Khi đóng góp, bạn đồng ý rằng đóng góp của bạn sẽ được cấp phép theo cùng giấy phép của repo này (xem [`LICENSE`](./LICENSE)).
