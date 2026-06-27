# Phụ thuộc vào Experimental Flag

> **Trạng thái:** Đang hoạt động · **Chủ sở hữu:** revfactory · **Cập nhật lần cuối:** 2026-04-18 · **SLA:** Xem [Cam kết giám sát](#cam-kết-giám-sát)

Tài liệu này giải thích vì sao `harness` yêu cầu `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, ba tương lai khả dĩ của flag đó, và những gì repo này sẽ làm trong mỗi trường hợp — kèm cam kết có khung thời gian để các đơn vị áp dụng cấp doanh nghiệp có thể lập kế hoạch theo đó.

---

## Tình trạng hiện tại

### Vì sao cần flag này

`harness` là một nhà máy meta-skill được xây dựng trên **Agent Teams API** của Claude Code. Ba primitive của Claude Code được gọi nội bộ mỗi khi người dùng chạy `claude "build a harness for <domain>"`:

| Primitive | Mục đích | Bị chặn bởi flag? |
|-----------|---------|-------------|
| `TeamCreate` | Khởi tạo đội multi-agent với ngữ cảnh chung | **Có** |
| `SendMessage` | Định tuyến message giữa thành viên đội (supervisor ↔ worker) | **Có** |
| `TaskCreate` | Tạo subtask chạy dài trong một đội | **Có** |
| Công cụ `Agent` (gọi) | Phân phối agent đơn | Không (GA) |

Cả ba primitive bị chặn bởi flag đều yêu cầu:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Nếu shell khởi chạy `claude` không đặt biến này, các đội do harness sinh ra sẽ rơi về thực thi đơn agent, làm hỏng âm thầm các mẫu Pipeline / Fan-out-in / Supervisor / Hierarchical Delegation.

### Tài liệu tham khảo từ Anthropic (cần đọc trước khi mở issue)

Lý do thiết kế và roadmap cho flag này nằm trong ba bài viết Anthropic Engineering. Người dùng đánh giá harness nên đọc ít nhất bài đầu:

1. [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — định nghĩa danh mục "harness" mà Anthropic ủng hộ và hợp đồng cho agent chạy dài.
2. [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — các mẫu mà `harness` mã hóa (Pipeline, Producer-Reviewer, Supervisor, v.v.).
3. [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) — hướng đi có thể thay thế Experimental flag (xem Kịch bản B).

---

## Đồ thị phụ thuộc

```
harness (v1.2.0)
  └── Agent Teams API (Claude Code)
        ├── TeamCreate            ← EXPERIMENTAL_AGENT_TEAMS=1
        ├── SendMessage           ← EXPERIMENTAL_AGENT_TEAMS=1
        ├── TaskCreate            ← EXPERIMENTAL_AGENT_TEAMS=1
        └── Agent (invoke)        ← GA (không phụ thuộc flag)
              └── Roadmap của Anthropic
                    ├── Kịch bản A: Flag bị loại bỏ (lên GA)
                    ├── Kịch bản B: Managed Agents lên GA (hướng song song)
                    └── Kịch bản C: Thay đổi signature gây breaking
```

**Đọc đồ thị này từ trên xuống:** harness phụ thuộc Agent Teams API, cái này phụ thuộc một Experimental flag duy nhất, cái này phụ thuộc roadmap riêng của Anthropic. Nếu node nào ở trên thay đổi, repo này có trách nhiệm thích nghi trong SLA dưới đây.

---

## 3 Kịch bản

Mỗi kịch bản liệt kê **trigger phát hiện** (cách chúng ta biết sự việc đã xảy ra), **hành động ở T+24h / T+48h / T+72h** mà repo này cam kết, và **artifact người dùng nhìn thấy** ở mỗi checkpoint.

### Kịch bản A — Flag bị loại bỏ (Agent Teams lên GA)

**Phát hiện trigger:** Anthropic Claude Code Changelog công bố "Agent Teams is now GA" **hoặc** binary `claude-code` không còn yêu cầu `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (phát hiện bởi CI hàng đêm tại [P-13](#)).

**Xác suất (chủ quan):** Cao — đây là hướng mà ba bài blog trên ngụ ý.

| Checkpoint | Hành động | Artifact |
|------------|--------|----------|
| **T+24h** | Mở branch `feat/drop-experimental-flag`. Xóa dòng `export` khỏi mọi README / docs / Quickstart. Thêm cận dưới `claude-code >= X.Y.Z` vào `plugin.json`. | Branch + PR (draft) |
| **T+48h** | Công bố `docs/migrating-from-experimental.md`. Cập nhật headline của `docs/experimental-dependency.md` (file này) thành "không cần flag từ vX.Y". Pin GitHub issue: "Action required: drop the export line". | Migration guide + issue pin |
| **T+72h** | Phát hành **v1.3.0** kèm: (a) mục CHANGELOG, (b) `gh release create` với ghi chú migration, (c) follow-up trên HN: "We dropped the experimental flag". | Tag git `v1.3.0` + GH Release |

**Tác động tới người dùng:** Tích cực. Trở ngại phê duyệt doanh nghiệp giảm — một checkbox ("không có experimental flag") trở nên thỏa được. Không có breaking change với code người dùng harness.

---

### Kịch bản B — Managed Agents lên GA (hướng song song)

**Phát hiện trigger:** Anthropic công bố "[Managed Agents](https://www.anthropic.com/engineering/managed-agents) is generally available" với CLI/SDK `claude-agents` ổn định.

**Xác suất (chủ quan):** Trung bình-cao trong 90 ngày. Managed Agents là mô hình thực thi phía server; điều phối đội phía client của harness **không** tự động chuyển đổi tương thích.

| Checkpoint | Hành động | Artifact |
|------------|--------|----------|
| **T+24h** | Mở PR `feat/managed-agents-compat`. Thêm scaffold `adapters/managed-agents/` để map 6 mẫu đội của harness sang cách gọi Managed Agents. Xác định mẫu không tương thích (khả năng cao: Hierarchical Delegation). | Compat PR (draft) |
| **T+48h** | Công bố blog post: **"Harness + Managed Agents: one layer up, not replaced"** trên Dev.to và trong repo. Định vị lại harness là tầng **thời điểm thiết kế** sinh ra config cho Managed Agents, không phải đối thủ ở runtime. | Blog định vị cùng tồn tại |
| **T+72h** | Công bố `docs/managed-agents-migration.md` kèm ma trận theo từng mẫu (mẫu nào trong 6 mẫu map 1:1, mẫu nào cần viết lại). Cập nhật section repo anh em trong README. | Migration guide |

**Ghi chú chiến lược:** harness định vị lại là **tầng trên của Managed Agents** — "Managed Agents chạy đội, harness thiết kế đội." Đây là khung cùng tồn tại ở §4.2 của kế hoạch GTM.

**Tác động tới người dùng:** Trung tính đến tích cực. Người dùng harness hiện tại tiếp tục dùng đường Experimental flag; người dùng mới có thể chọn output Managed Agents.

---

### Kịch bản C — Breaking change (thay đổi signature API)

**Phát hiện trigger:** CI hàng đêm (`.github/workflows/nightly-compat.yml`, theo dõi ở roadmap P-13) thất bại với nightly build mới nhất của Claude Code **hoặc** Changelog công bố đổi tên env var / thay đổi signature `TeamCreate`.

**Xác suất (chủ quan):** Trung bình. API thử nghiệm thường bị đổi tên không có khung khử dần (deprecation window).

| Checkpoint | Hành động | Artifact |
|------------|--------|----------|
| **T+0 đến T+24h** | Cảnh báo CI hàng đêm nổ ra ở Slack/Discord. Tác giả mở branch `hotfix/compat-<date>`, patch các điểm gọi bị ảnh hưởng. Unit test pass với cả signature cũ + mới (cố gắng tối đa). | Hotfix branch |
| **T+24h** | Merge hotfix. Push tag patch `v1.2.x`. Cập nhật dòng `docs/compatibility-matrix.md` cho phiên bản Claude Code bị ảnh hưởng. | Patch release `v1.2.x` |
| **T+72h** | Nếu thay đổi không nhỏ (ảnh hưởng hợp đồng công khai của harness), công bố thông báo ngắn ở tab Discussions của repo + X. Nếu không, mục CHANGELOG là đủ. | Discussions post (có điều kiện) |

**Tác động tới người dùng:** Người dùng đang pin phiên bản Claude Code cũ không bị ảnh hưởng. Người dùng dùng phiên bản mới nhất nhận patch trong tuần.

---

## Cam kết giám sát

Chúng tôi cam kết **SLA có thể quan sát** sau. Trễ SLA là cơ sở để mở issue với label `sla-breach`.

| Sự kiện | SLA | Cách đo |
|-------|-----|-------------|
| Anthropic công bố thay đổi Agent Teams / Managed Agents trong Changelog chính thức | Tài liệu này được cập nhật trong **72 giờ** | So sánh timestamp bài Changelog với dòng `Last updated` của file này |
| CI hàng đêm phát hiện compat break | Mở hotfix branch trong **24 giờ** | Timestamp lần chạy GitHub Actions so với timestamp tạo branch |
| Claude Code stable release mới (minor hoặc major) | Thêm dòng vào `docs/compatibility-matrix.md` trong **7 ngày** | Diff compatibility matrix |

**Nguồn chúng tôi chủ động giám sát:**

- Release notes Claude Code — theo dõi qua RSS của [Anthropic Engineering blog](https://www.anthropic.com/engineering)
- GitHub Releases của `anthropics/claude-code` (tag nightly)
- Kênh `#claude-code` Discord của Anthropic (tín hiệu cộng đồng)

---

## FAQ cho người dùng cấp doanh nghiệp

### Câu 1. Chúng tôi ở ngành bị quản lý (tài chính, y tế, công vụ) và không thể bật flag `EXPERIMENTAL` ở production. Làm sao áp dụng harness?

**Nguyên nhân:** Nhiều khung tuân thủ (SOC 2 Type II, ISO 27001, K-ISMS) không cho phép tính năng không ổn định / preview ở production.
**Hành động:** Dùng harness **chỉ ở thời điểm thiết kế**: chạy ở máy sandbox để scaffold file `.claude/agents/` và `.claude/skills/`, rồi commit các artifact đã sinh vào repo production. Claude Code production không bao giờ cần flag — chỉ runtime `TeamCreate` bị chặn bởi flag mới cần. Các skill đơn agent đã sinh tương thích đường GA.

### Câu 2. Nếu Agent Teams lên GA (Kịch bản A), code do harness sinh hiện tại của tôi có bị hỏng không?

**Nguyên nhân:** Trong lịch sử, lên GA của Claude Code Anthropic không gây breaking với artifact đã sinh; flag chỉ đơn giản là không còn bắt buộc.
**Hành động:** Người dùng cuối không cần làm gì. File `.claude/agents/*.md` và `.claude/skills/*` của bạn là Markdown thuần và vẫn hợp lệ. Bạn có thể `unset CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` ngay ngày GA. Chúng tôi sẽ công bố ghi chú migration trong 48 giờ (xem Kịch bản A).

### Câu 3. Có cam kết SLA bằng văn bản không? Nếu trễ thì sao?

**Nguyên nhân:** Doanh nghiệp cần một cam kết hợp đồng hoặc tối thiểu có thể quan sát được trước khi phê duyệt.
**Hành động:** Bảng SLA trên là **cam kết công khai** và được thực thi bằng: (a) một GitHub Action comment vào file này nếu dòng `Last updated` cũ hơn 72 giờ sau một sự kiện Changelog được phát hiện, (b) label issue `sla-breach` mà người dùng có thể gắn, (c) nghĩa vụ post-mortem trong `CONTRIBUTING.md` cho mọi lần trễ. Đây không phải SLA trả phí — đây là cam kết cộng đồng. Để có SLA trả phí, liên hệ maintainer (xem README repo).

---

**Tài liệu liên quan:**
- [`docs/quickstart.md`](./quickstart.md) — hướng dẫn cài đặt 5 phút
- [`docs/show-hn-launch-kit.md`](./show-hn-launch-kit.md) — bộ công cụ ra mắt công khai
- `docs/compatibility-matrix.md` *(đang chờ P-13)* — bảng phiên bản Claude Code × harness
