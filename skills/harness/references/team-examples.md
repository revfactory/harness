# Agent Team Examples

---

## Ví dụ 1: Đội nghiên cứu (chế độ Agent Team)

### Kiến trúc đội: Fan-out/Fan-in
### Chế độ thực thi: Agent Team

```
[Leader/Orchestrator]
    ├── TeamCreate(research-team)
    ├── TaskCreate(4 công việc điều tra)
    ├── Thành viên tự điều phối (SendMessage)
    ├── Thu thập kết quả (Read)
    └── Sinh báo cáo tổng hợp
```

### Cấu hình agent

| Thành viên | Loại agent | Vai trò | Output |
|------|-------------|------|------|
| official-researcher | general-purpose | Tài liệu chính thức/blog | research_official.md |
| media-researcher | general-purpose | Truyền thông/đầu tư | research_media.md |
| community-researcher | general-purpose | Cộng đồng/SNS | research_community.md |
| background-researcher | general-purpose | Bối cảnh/cạnh tranh/học thuật | research_background.md |
| (Leader = Orchestrator) | — | Báo cáo tổng hợp | bao-cao-tong-hop.md |

> Agent nghiên cứu dùng loại built-in `general-purpose`, nhưng bắt buộc phải định nghĩa bằng file `.claude/agents/{name}.md`. File này ghi rõ vai trò·phạm vi điều tra·giao thức giao tiếp đội để đảm bảo tính tái sử dụng và chất lượng phối hợp.

### Quy trình Orchestrator (Agent Team)

```
Phase 1: Chuẩn bị
  - Phân tích input của người dùng (xác định chủ đề, chế độ điều tra)
  - Tạo _workspace/

Phase 2: Tạo đội
  - TeamCreate(team_name: "research-team", members: [
      { name: "official", prompt: "Điều tra kênh chính thức..." },
      { name: "media", prompt: "Điều tra xu hướng truyền thông/đầu tư..." },
      { name: "community", prompt: "Điều tra phản ứng cộng đồng..." },
      { name: "background", prompt: "Điều tra bối cảnh/môi trường cạnh tranh..." }
    ])
  - TaskCreate(tasks: [
      { title: "Điều tra kênh chính thức", assignee: "official" },
      { title: "Điều tra xu hướng truyền thông", assignee: "media" },
      { title: "Điều tra phản ứng cộng đồng", assignee: "community" },
      { title: "Điều tra môi trường bối cảnh", assignee: "background" }
    ])

Phase 3: Thực hiện điều tra
  - 4 thành viên điều tra độc lập
  - Khi có phát hiện thú vị, chia sẻ qua SendMessage giữa thành viên
    (ví dụ: media truyền tin tức đầu tư phát hiện được cho background)
  - Khi phát hiện thông tin mâu thuẫn, thảo luận trực tiếp giữa thành viên
  - Mỗi thành viên lưu file + báo leader khi hoàn thành

Phase 4: Hợp nhất
  - Leader Read 4 sản phẩm
  - Sinh báo cáo tổng hợp
  - Thông tin mâu thuẫn ghi kèm nguồn

Phase 5: Dọn dẹp
  - Yêu cầu thành viên kết thúc
  - Dọn dẹp đội
  - Giữ lại _workspace/ (dùng cho kiểm định/audit trail sau)
```

### Mẫu giao tiếp đội

```
official ──SendMessage──→ background  (chia sẻ thông báo chính thức liên quan)
media ────SendMessage──→ background  (chia sẻ thông tin đầu tư/sáp nhập)
community ─SendMessage──→ media      (thông tin liên quan media trong phản ứng cộng đồng)
Tất cả thành viên ──TaskUpdate──→ danh sách công việc chung  (cập nhật tiến độ)
Leader ←───── thông báo rảnh ──── thành viên hoàn thành   (tự động)
```

---

## Ví dụ 2: Đội viết tiểu thuyết SF (chế độ Agent Team)

### Kiến trúc đội: Pipeline + Fan-out
### Chế độ thực thi: Agent Team

```
Phase 1 (song song — Agent Team): worldbuilder + character-designer + plot-architect
  → Điều phối tính nhất quán qua SendMessage
Phase 2 (tuần tự): prose-stylist (viết)
Phase 3 (song song — Agent Team): science-consultant + continuity-manager (review)
  → Chia sẻ phát hiện qua SendMessage
Phase 4 (tuần tự): prose-stylist (sửa theo review)
```

### Cấu hình agent

| Thành viên | Loại agent | Vai trò | Skill |
|------|-------------|------|------|
| worldbuilder | tùy biến | Xây dựng thế giới quan | world-setting |
| character-designer | tùy biến | Thiết kế nhân vật | character-profile |
| plot-architect | tùy biến | Cấu trúc cốt truyện | outline |
| prose-stylist | tùy biến | Biên tập văn phong + viết | write-scene, review-chapter |
| science-consultant | tùy biến | Kiểm định khoa học | science-check |
| continuity-manager | tùy biến | Kiểm định tính nhất quán | consistency-check |

### File agent mẫu đầy đủ: `worldbuilder.md`

```markdown
---
name: worldbuilder
description: "Chuyên gia xây dựng thế giới quan cho tiểu thuyết SF. Thiết kế quy luật vật lý, cấu trúc xã hội, mức độ công nghệ, lịch sử."
---

# Worldbuilder — Chuyên gia thiết kế thế giới quan SF

Bạn là chuyên gia thiết kế thế giới quan cho tiểu thuyết SF. Dựa trên cơ sở khoa học nhưng mở rộng bằng trí tưởng tượng, bạn xây dựng nền tảng vật lý·xã hội·công nghệ của thế giới mà câu chuyện sẽ diễn ra.

## Vai trò cốt lõi
1. Định nghĩa quy luật vật lý và mức độ công nghệ của thế giới
2. Thiết kế cấu trúc xã hội, hệ thống chính trị, hệ thống kinh tế
3. Xây dựng bối cảnh lịch sử và cấu trúc xung đột hiện tại
4. Mô tả môi trường và không khí theo từng địa điểm

## Nguyên tắc làm việc
- Tính nhất quán nội tại là ưu tiên hàng đầu — không được có mâu thuẫn giữa các thiết lập
- Suy luận hiệu ứng lan tỏa của thế giới bằng câu hỏi nối tiếp "nếu có công nghệ này thì sao?"
- Thế giới quan phục vụ câu chuyện — tránh thiết lập quá mức gây cản trở cốt truyện

## Giao thức input/output
- Input: ý tưởng thế giới quan của người dùng, yêu cầu thể loại
- Output: `_workspace/01_worldbuilder_setting.md`
- Định dạng: markdown. Chia theo section (vật lý/xã hội/công nghệ/lịch sử/địa điểm)

## Giao thức giao tiếp đội
- Gửi tới character-designer: thông tin cấu trúc xã hội, hệ thống giai cấp, nhóm nghề nghiệp qua SendMessage
- Gửi tới plot-architect: cấu trúc xung đột chính của thế giới, yếu tố khủng hoảng qua SendMessage
- Nhận từ science-consultant: nhận phản hồi lỗi khoa học → sửa thiết lập
- Khi thay đổi thế giới quan, broadcast cho toàn bộ thành viên liên quan

## Xử lý lỗi
- Nếu ý tưởng mơ hồ, đề xuất 3 hướng và yêu cầu chọn
- Khi phát hiện lỗi khoa học, đề xuất kèm phương án thay thế

## Phối hợp
- Cung cấp thông tin cấu trúc xã hội cho character-designer
- Cung cấp thông tin cấu trúc xung đột cho plot-architect
- Sửa thiết lập theo phản hồi của science-consultant
```

### Quy trình đội chi tiết

```
Phase 1: TeamCreate(team_name: "novel-team", members: [worldbuilder, character-designer, plot-architect])
         TaskCreate([xây dựng thế giới quan, thiết kế nhân vật, cấu trúc cốt truyện])
         → Thành viên tự điều phối làm việc song song
         → worldbuilder hoàn thành cấu trúc xã hội → SendMessage cho character-designer
         → character-designer xong thiết lập nhân vật chính → SendMessage cho plot-architect

Phase 2: Dọn dẹp đội Phase 1 → gọi prose-stylist như subagent (viết đơn lẻ nên không cần đội)
         prose-stylist Read 3 sản phẩm trong _workspace/ để viết
         → Lưu kết quả vào _workspace/02_prose_draft.md

Phase 3: Tạo đội mới — TeamCreate(team_name: "review-team", members: [science-consultant, continuity-manager])
         (mỗi phiên chỉ kích hoạt 1 đội, nhưng vì đã dọn đội Phase 1 nên tạo đội mới được)
         → Hai reviewer kiểm tra draft, chia sẻ phát hiện lẫn nhau
         → science-consultant phát hiện lỗi vật lý thì cũng báo continuity-manager
         → Sau khi review xong, dọn dẹp đội

Phase 4: Gọi prose-stylist như subagent, sửa cuối cùng theo kết quả review
```

---

## Ví dụ 3: Đội sản xuất webtoon (chế độ Subagent)

### Kiến trúc đội: Producer-Reviewer
### Chế độ thực thi: Subagent

> Mẫu producer-reviewer chỉ có 2 agent, và truyền kết quả là trọng tâm chứ không phải giao tiếp, nên subagent phù hợp.

```
Phase 1: Agent(webtoon-artist) → sinh panel
Phase 2: Agent(webtoon-reviewer) → kiểm tra
Phase 3: Agent(webtoon-artist) → sinh lại panel có vấn đề (tối đa 2 lần)
```

### Cấu hình agent

| Agent | subagent_type | Vai trò | Skill |
|---------|--------------|------|------|
| webtoon-artist | tùy biến | Sinh ảnh panel | generate-webtoon |
| webtoon-reviewer | tùy biến | Kiểm tra chất lượng | review-webtoon, fix-webtoon-panel |

### File agent mẫu đầy đủ: `webtoon-reviewer.md`

```markdown
---
name: webtoon-reviewer
description: "Chuyên gia kiểm tra chất lượng panel webtoon. Đánh giá bố cục, tính nhất quán nhân vật, độ rõ của văn bản, dàn dựng."
---

# Webtoon Reviewer — Chuyên gia kiểm tra chất lượng webtoon

Bạn là chuyên gia kiểm tra chất lượng panel webtoon. Đánh giá panel dựa trên độ hoàn thiện hình ảnh, khả năng truyền tải câu chuyện, tính nhất quán nhân vật.

## Vai trò cốt lõi
1. Đánh giá bố cục và độ hoàn thiện hình ảnh của mỗi panel
2. Kiểm định tính nhất quán hình dáng nhân vật giữa các panel
3. Đánh giá độ rõ và vị trí của văn bản trong bong bóng lời thoại
4. Xem xét luồng dàn dựng và nhịp độ của toàn tập

## Nguyên tắc làm việc
- Phân loại rõ ràng theo 3 mức PASS/FIX/REDO
- FIX là khi có thể giải quyết bằng sửa một phần, REDO là cần tạo lại toàn bộ
- Đánh giá theo tiêu chí khách quan (tính nhất quán, độ rõ, bố cục), không theo sở thích chủ quan

## Giao thức input/output
- Input: các ảnh panel trong thư mục `_workspace/panels/`
- Output: `_workspace/review_report.md`
- Định dạng:
  ```
  ## Panel {N}
  - Phân loại: PASS | FIX | REDO
  - Lý do: [lý do cụ thể]
  - Chỉ thị sửa: [hướng sửa cụ thể nếu là FIX/REDO]
  ```

## Xử lý lỗi
- Nếu nạp ảnh thất bại, phân loại panel đó là REDO
- Panel vẫn là REDO sau 2 lần tạo lại thì xử lý PASS kèm cảnh báo

## Phối hợp
- Gửi chỉ thị sửa cho webtoon-artist (dựa trên file kết quả)
- Kiểm tra lại panel đã tạo lại (tối đa 2 lần lặp)
```

### Xử lý lỗi

```
Chính sách thử lại:
- Panel bị phân loại REDO → yêu cầu artist tạo lại (kèm chỉ thị sửa cụ thể)
- Sau tối đa 2 lần lặp, ép xử lý PASS
- Nếu trên 50% toàn bộ panel là REDO, đề xuất người dùng sửa prompt
```

---

## Ví dụ 4: Đội review code (chế độ Agent Team)

### Kiến trúc đội: Fan-out/Fan-in + Thảo luận
### Chế độ thực thi: Agent Team

> Review code là ví dụ điển hình cho thấy agent team phát huy hiệu quả. Các reviewer ở các góc nhìn khác nhau chia sẻ phát hiện và phản biện lẫn nhau, cho phép review sâu hơn.

```
[Leader] → TeamCreate(review-team)
    ├── security-reviewer: kiểm tra lỗ hổng an ninh
    ├── performance-reviewer: phân tích tác động hiệu năng
    └── test-reviewer: kiểm định độ phủ test
    → Các reviewer chia sẻ phát hiện lẫn nhau (SendMessage)
    → Leader hợp nhất kết quả
```

### Mẫu giao tiếp đội

```
security ──SendMessage──→ performance  ("Câu SQL này có thể bị injection, cần kiểm tra cả góc độ hiệu năng")
performance ──SendMessage──→ test      ("Phát hiện query N+1, kiểm tra giúp có test liên quan không")
test ────SendMessage──→ security      ("Module xác thực không có test, ý kiến về thứ tự ưu tiên từ góc độ an ninh?")
```

Cốt lõi: các reviewer giao tiếp trực tiếp **không qua leader**, giúp phát hiện nhanh các vấn đề liên ngành.

---

## Ví dụ 5: Mẫu Supervisor — Đội migration code (chế độ Agent Team)

### Kiến trúc đội: Supervisor
### Chế độ thực thi: Agent Team

```
[supervisor/Leader] → Phân tích danh sách file → Phân công batch
    ├→ [migrator-1] (batch A)
    ├→ [migrator-2] (batch B)
    └→ [migrator-3] (batch C)
    ← Nhận TaskUpdate → phân công batch thêm hoặc phân công lại
```

### Cấu hình agent

| Thành viên | Vai trò |
|------|------|
| (Leader = migration-supervisor) | Phân tích file, phân chia batch, quản lý tiến độ |
| migrator-1~3 | Thực hiện migration batch file được phân công |

### Logic phân phối động của Supervisor (tận dụng Agent Team)

```
1. Thu thập toàn bộ danh sách file đối tượng
2. Ước tính độ phức tạp (kích thước file, số import, phụ thuộc)
3. Đăng ký batch file là công việc bằng TaskCreate (kèm phụ thuộc)
4. Thành viên tự yêu cầu công việc (claim)
5. Khi thành viên báo hoàn thành bằng TaskUpdate:
   - Thành công → tự động yêu cầu công việc tiếp theo
   - Thất bại → leader kiểm tra nguyên nhân qua SendMessage → phân công lại hoặc gán cho thành viên khác
6. Hoàn thành toàn bộ công việc → leader chạy test tích hợp
```

Khác với fan-out: công việc không cố định trước mà được **phân công động tại runtime**. Tính năng tự yêu cầu (claim) của danh sách công việc chung khớp tự nhiên với mẫu supervisor.

---

## Tổng hợp mẫu sản phẩm đầu ra

### File định nghĩa agent
Vị trí: `project/.claude/agents/{agent-name}.md`
Section bắt buộc: vai trò cốt lõi, nguyên tắc làm việc, giao thức input/output, xử lý lỗi, phối hợp
Section bổ sung cho chế độ team: **Giao thức giao tiếp đội** (nhận/gửi message, phạm vi yêu cầu công việc)

### Cấu trúc file skill
Vị trí: `project/.claude/skills/{skill-name}/SKILL.md` (cấp dự án)
Hoặc: `~/.claude/skills/{skill-name}/SKILL.md` (cấp toàn cục)

### Skill tích hợp (Orchestrator)
Skill cấp cao điều phối toàn đội. Định nghĩa cấu hình agent và quy trình theo từng kịch bản.
Template: xem `references/orchestrator-template.md`.
**Bắt buộc ghi rõ chế độ thực thi** — Agent Team (mặc định) hoặc Subagent.
