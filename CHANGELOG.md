# Changelog

Dự án này tuân theo [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Bước kiểm tra trùng lặp trước khi tạo agent/skill mới (Phase 3-0, Phase 4-0)
- Mục "Thiết kế tái sử dụng agent" trong `references/agent-design-patterns.md`
- §9 "Thiết kế tái sử dụng skill" trong `references/skill-writing-guide.md`

### Changed
- Bổ sung rõ 3-0/4-0 vào ma trận chọn Phase
- Thêm con trỏ tới bước kiểm tra tái sử dụng vào Phase 2-3
- Thêm 2 hạng mục kiểm tra tái sử dụng vào checklist đầu ra

---

## [1.2.1] - 2026-04-18

### Fixed

- **Đồng bộ tính nhất quán phiên bản** — Badge của README.md / README_KO.md / README_JA.md ghi `v1.0.1`, `.claude-plugin/marketplace.json` ghi `1.1.0`, `.claude-plugin/plugin.json` ghi `1.2.0` → lệch nhau ba chỗ → thống nhất tất cả về **v1.2.0** (theo plugin.json)
- **Chuẩn bị giải quyết tình trạng 0 tagged release** — Lập kế hoạch gắn tag truy hồi v1.0.0 / v1.0.1 / v1.1.0 / v1.2.0 (xem `_workspace/release/audit-2026-04-18.md` §4)

### Added

- **Tuyên bố định vị: "nhà máy harness" (harness factory)** — Đưa câu tự định nghĩa danh mục lên đầu README. Chiếm lĩnh danh mục với "nhà máy harness chuyên đúc agent + skill theo từng lĩnh vực" (tạo khác biệt so với các framework đơn agent/prompt)
- **CONTRIBUTING.md** — Hướng dẫn đóng góp và quy định SLA (phản hồi PR lần đầu trong 72h, phân loại Issue trong 48h). Giải quyết rào cản onboarding cộng đồng
- **Thư mục docs/** — Tạo không gian mới để di chuyển tài liệu dài hạn (kiến trúc, migration, danh mục pattern). Tránh README quá dài và tăng khả năng tìm kiếm
- **Chính sách phản hồi Issue #3** — Thêm template phản hồi chính thức và quy trình phân loại cho issue từ cộng đồng

### Changed

- Version trong `.claude-plugin/marketplace.json`: `1.1.0` → `1.2.0`
- Badge README (cả 3 bản EN/KO/JA): `Version-1.0.1` → `Version-1.2.0`
- **Viết lại description trong `.claude-plugin/plugin.json`** — `"Agent Team & Skill Architect — Meta-skill that designs..."` → `"The team-architecture factory for Claude Code — a meta-skill that turns a domain description into an agent team and the skills they use, with six pre-defined team-architecture patterns..."` (song ngữ EN+KO, phản ánh định vị L3 Meta-Factory)
- **Mở rộng keywords trong `.claude-plugin/plugin.json`** — từ 5 lên 17 (`harness-factory`, `team-architecture-factory`, `claude-code-plugin`, `agent-scaffolding`, `multi-agent`, thêm 6 keyword cho 6 mẫu kiến trúc)

## [1.2.0] - 2026-04-08

### Changed

- **Đơn giản hóa chính sách đăng ký CLAUDE.md (loại bỏ trùng lặp)** — Chuyển Phase 5-4 "đăng ký ngữ cảnh" thành "đăng ký con trỏ". Loại bỏ danh sách agent, danh sách skill, cấu trúc thư mục, chi tiết quy tắc thực thi khỏi CLAUDE.md, chỉ giữ lại **quy tắc trigger + lịch sử thay đổi**. Danh sách agent/skill được quản lý tập trung tại `.claude/agents/`, `.claude/skills/` và skill orchestrator
- **Xóa bước đồng bộ tạm thời ở Phase 3/4** — Loại bỏ chỉ thị đồng bộ tạm thời ở Phase 3/4 để giảm gánh nặng đồng bộ CLAUDE.md. Đăng ký con trỏ cuối cùng chỉ thực hiện một lần tại Phase 5-4
- **Định nghĩa lại nguyên tắc cốt lõi số 3** — "Đăng ký ngữ cảnh harness vào CLAUDE.md" → "Đăng ký con trỏ harness vào CLAUDE.md"
- **Xóa bảng phân chia vai trò CLAUDE.md vs orchestrator** — Không còn cần thiết do chính sách con trỏ đã đơn giản hóa

### Added

- **Phase 2-1: Chế độ thực thi lai (hybrid)** — Bổ sung mẫu lai trộn chế độ theo từng Phase, ngoài agent team / subagent. Quy định rõ các tổ hợp thường dùng (thu thập song song → hợp nhất đồng thuận, tạo team → kiểm định, tái cấu trúc team giữa các Phase)
- **Bảng so sánh chế độ thực thi Phase 2-1** — Cung cấp đặc điểm của 3 chế độ team/sub/hybrid và quy trình quyết định 3 bước
- **Mẫu orchestrator lai ở Phase 5-0** — Quy tắc ghi rõ chế độ thực thi ở đầu mỗi Phase khi cấu hình lai
- **Truyền dữ liệu dựa trên giá trị trả về ở Phase 5-1** — Thêm chiến lược truyền dữ liệu riêng cho chế độ subagent (bên cạnh message/task/file hiện có)
- **Tổ hợp khuyến nghị Phase 5-1 (sub/hybrid)** — Quy định rõ tổ hợp truyền dữ liệu khuyến nghị cho chế độ sub và hybrid, ngoài chế độ team

## [1.1.0] - 2026-04-05

### Added

- **Phase 0: Kiểm tra hiện trạng** — Khi trigger, kiểm tra trạng thái harness hiện có trước, sau đó định tuyến vào 1 trong 3 nhánh: xây mới / mở rộng harness có sẵn / vận hành-bảo trì
- **Ma trận chọn Phase cho mở rộng harness có sẵn** — Bảng quyết định chỉ rõ Phase cần thiết theo từng trường hợp thêm agent/thêm skill/đổi kiến trúc
- **Đồng bộ tạm thời CLAUDE.md ở Phase 3/4** — Cập nhật ngay vào CLAUDE.md sau khi tạo agent/skill (chịu được gián đoạn phiên làm việc)
- **Phase 5-4: Đăng ký ngữ cảnh harness vào CLAUDE.md** — Ghi lại cấu trúc đội agent, danh sách skill, quy tắc thực thi, cấu trúc thư mục, lịch sử thay đổi. Bao gồm bảng phân chia vai trò CLAUDE.md vs orchestrator
- **Phase 5-5: Hỗ trợ công việc tiếp theo** — Description của orchestrator phải có từ khóa tiếp nối, dùng bước kiểm tra ngữ cảnh ở Phase 0 để tự phân biệt giữa khởi tạo/chạy lại một phần/chạy mới
- **Đường mở rộng orchestrator ở Phase 5** — Hướng dẫn sửa orchestrator có sẵn thay vì tạo mới khi mở rộng
- **Phase 7: Cơ chế tiến hóa harness** — Thu thập phản hồi sau khi thực thi → ánh xạ loại phản hồi sang đối tượng cần sửa → ghi lịch sử thay đổi → trigger tiến hóa tự động
- **Phase 7-5: Quy trình vận hành/bảo trì** — 4 bước: kiểm tra hiện trạng → sửa từng phần → đồng bộ CLAUDE.md → xác minh thay đổi
- **Trigger vận hành/bảo trì trong description** — Từ khóa 'kiểm tra harness', 'audit harness', 'hiện trạng harness', 'đồng bộ agent/skill'
- **Tăng cường checklist đầu ra** — Thêm hạng mục hoàn tất đồng bộ CLAUDE.md, ghi lịch sử thay đổi, kiểm tra ngữ cảnh Phase 0
- Thêm Phase 0 (kiểm tra ngữ cảnh) vào template orchestrator — áp dụng cho cả chế độ agent team và subagent
- Thêm mẫu từ khóa công việc tiếp theo vào template description của orchestrator

### Changed

- Mở rộng nguyên tắc cốt lõi từ 2 lên 4 (thêm đăng ký CLAUDE.md, hệ thống tiến hóa)
- **Thống nhất "nhật ký tiến hóa" → "lịch sử thay đổi"** — Đồng nhất tên và schema (4 cột: ngày/nội dung thay đổi/đối tượng/lý do) trên toàn bộ section
- **Phase 1 Step 3** — Đổi sang phân tích xung đột dựa trên kết quả kiểm tra Phase 0 (loại bỏ trùng lặp)
- **Code block template CLAUDE.md ở 5-4** — Sửa lỗi vỡ render lồng nhau (3 backtick → 4 backtick)
- **Mở rộng bảng phân chia vai trò** — Thêm dòng danh sách skill, cấu trúc thư mục, lịch sử thay đổi
- **Template orchestrator** — Thêm bước kiểm tra ngữ cảnh Phase 0, hướng dẫn từ khóa công việc tiếp theo

## [1.0.1] - 2026-03-28

### Changed

- Loại bỏ nội dung trùng lặp giữa SKILL.md ↔ references (330 dòng → 285 dòng)
  - Phase 2-1: Bảng so sánh/bullet chế độ thực thi → nguyên tắc cốt lõi + con trỏ tới agent-design-patterns.md
  - Phase 2-3: Bullet tiêu chí tách agent → tổng hợp 4 trục + con trỏ tới agent-design-patterns.md
  - Phase 3: Code block template định nghĩa agent → liệt kê section bắt buộc + con trỏ references
  - Phase 5-2: Bảng xử lý lỗi 5 dòng → nguyên tắc cốt lõi + con trỏ tới orchestrator-template.md

## [1.0.0] - 2026-03-27

### Added

- Meta-skill cấu hình harness dựa trên quy trình 6 Phase
- 6 mẫu kiến trúc agent (pipeline, fan-out/fan-in, expert pool, producer-reviewer, supervisor, hierarchical delegation)
- Hỗ trợ chế độ thực thi agent team / subagent
- Hướng dẫn sinh skill dựa trên Progressive Disclosure
- Template orchestrator (chế độ agent team + chế độ subagent)
- Hướng dẫn tích hợp agent QA (dựa trên 7 case bug thực tế từ dự án thật)
- Phương pháp kiểm thử/đánh giá skill (so sánh With-skill vs Without-skill)
- 5 ví dụ cấu hình đội thực chiến (nghiên cứu, tiểu thuyết, webtoon, code review, migration)
