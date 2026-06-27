# Template skill Orchestrator

Orchestrator là một skill cấp cao chuyên điều phối toàn đội. Cung cấp 3 template theo từng chế độ thực thi:

- **Template A: chế độ Agent Team (mặc định)** — lựa chọn ưu tiên hàng đầu khi 2 người trở lên phối hợp
- **Template B: chế độ Subagent (phương án thay thế)** — khi không cần giao tiếp đội
- **Template C: chế độ Hybrid** — trộn chế độ theo từng Phase

---

## Template A: Chế độ Agent Team (mặc định · ưu tiên hàng đầu)

**Chế độ mặc định được xem xét đầu tiên** khi 2 agent trở lên cần phối hợp. Tạo đội bằng `TeamCreate`, điều phối bằng danh sách công việc chung và `SendMessage`.

```markdown
---
name: {domain}-orchestrator
description: "Orchestrator điều phối đội agent {domain}. {từ khóa khởi chạy lần đầu}. Công việc tiếp theo: sửa kết quả {domain}, chạy lại một phần, cập nhật, bổ sung, chạy lại, yêu cầu cải thiện kết quả trước — đều phải dùng skill này."
---

# {Domain} Orchestrator

Skill tích hợp điều phối đội agent {domain} để tạo ra {sản phẩm cuối cùng}.

## Chế độ thực thi: Agent Team

## Cấu hình agent

| Thành viên | Loại agent | Vai trò | Skill | Output |
|------|-------------|------|------|------|
| {teammate-1} | {tùy biến hoặc built-in} | {vai trò} | {skill} | {output-file} |
| {teammate-2} | {tùy biến hoặc built-in} | {vai trò} | {skill} | {output-file} |
| ... | | | | |

## Quy trình

### Phase 0: Kiểm tra ngữ cảnh (hỗ trợ công việc tiếp theo)

Kiểm tra sự tồn tại của sản phẩm hiện có để quyết định chế độ thực thi:

1. Kiểm tra thư mục `_workspace/` có tồn tại không
2. Quyết định chế độ thực thi:
   - **`_workspace/` không tồn tại** → chạy lần đầu. Tiến hành Phase 1
   - **`_workspace/` tồn tại + người dùng yêu cầu sửa một phần** → chạy lại một phần. Chỉ gọi lại agent liên quan, chỉ ghi đè phần sản phẩm cần sửa
   - **`_workspace/` tồn tại + cung cấp input mới** → chạy mới. Chuyển `_workspace/` hiện có sang `_workspace_{YYYYMMDD_HHMMSS}/` rồi tiến hành Phase 1
3. Khi chạy lại một phần: đưa đường dẫn sản phẩm trước vào prompt của agent, chỉ thị agent đọc kết quả cũ và phản ánh phản hồi

### Phase 1: Chuẩn bị
1. Phân tích input của người dùng — {xác định cái gì}
2. Tạo `_workspace/` trong thư mục làm việc
   - **Chạy lần đầu**: tạo `_workspace/` mới
   - **Chạy mới**: chuyển `_workspace/` hiện có sang `_workspace_{YYYYMMDD_HHMMSS}/` rồi tạo lại `_workspace/` mới
3. Lưu dữ liệu input vào `_workspace/00_input/`

### Phase 2: Tạo đội

1. Tạo đội:
   ```
   TeamCreate(
     team_name: "{domain}-team",
     members: [
       { name: "{teammate-1}", agent_type: "{type}", model: "opus", prompt: "{mô tả vai trò và chỉ thị công việc}" },
       { name: "{teammate-2}", agent_type: "{type}", model: "opus", prompt: "{mô tả vai trò và chỉ thị công việc}" },
       ...
     ]
   )
   ```

2. Đăng ký công việc:
   ```
   TaskCreate(tasks: [
     { title: "{công việc 1}", description: "{chi tiết}", assignee: "{teammate-1}" },
     { title: "{công việc 2}", description: "{chi tiết}", assignee: "{teammate-2}" },
     { title: "{công việc 3}", description: "{chi tiết}", depends_on: ["{công việc 1}"] },
     ...
   ])
   ```

   > 5~6 công việc mỗi thành viên là hợp lý. Công việc có phụ thuộc dùng `depends_on`.

### Phase 3: {Công việc chính — ví dụ: điều tra/sinh nội dung/phân tích}

**Cách thực thi:** thành viên tự điều phối

Thành viên tự yêu cầu (claim) công việc từ danh sách công việc chung và thực hiện độc lập.
Leader giám sát tiến độ và can thiệp khi cần.

**Quy tắc giao tiếp giữa thành viên:**
- {teammate-1} truyền {thông tin gì} cho {teammate-2} qua SendMessage
- {teammate-2} lưu kết quả ra file và báo leader khi hoàn thành
- Nếu thành viên cần kết quả của thành viên khác, yêu cầu qua SendMessage

**Lưu sản phẩm:**

| Thành viên | Đường dẫn output |
|------|----------|
| {teammate-1} | `_workspace/{phase}_{teammate-1}_{artifact}.md` |
| {teammate-2} | `_workspace/{phase}_{teammate-2}_{artifact}.md` |

**Giám sát của leader:**
- Tự động nhận thông báo khi thành viên rảnh
- Khi một thành viên bị kẹt, chỉ thị hoặc phân công lại qua SendMessage
- Kiểm tra tiến độ tổng thể bằng TaskGet

### Phase 4: {Công việc tiếp theo — ví dụ: kiểm định/hợp nhất}
1. Chờ tất cả thành viên hoàn thành (kiểm tra trạng thái bằng TaskGet)
2. Thu thập sản phẩm của từng thành viên bằng Read
3. {logic hợp nhất/kiểm định}
4. Sinh sản phẩm cuối cùng: `{output-path}/{filename}`

### Phase 5: Dọn dẹp
1. Yêu cầu thành viên kết thúc (SendMessage)
2. Dọn dẹp đội (TeamDelete)
3. Giữ lại thư mục `_workspace/` (không xóa sản phẩm trung gian — dùng cho kiểm định/audit trail sau)
4. Báo cáo tóm tắt kết quả cho người dùng

> **Khi cần tái cấu trúc đội:** nếu mỗi Phase cần tổ hợp chuyên gia khác nhau, dọn dẹp đội hiện tại bằng TeamDelete rồi tạo đội mới cho Phase tiếp theo bằng TeamCreate. Sản phẩm của đội trước được giữ trong `_workspace/` nên đội mới có thể truy cập bằng Read.

## Luồng dữ liệu

```
[Leader] → TeamCreate → [teammate-1] ←SendMessage→ [teammate-2]
                          │                           │
                          ↓                           ↓
                    artifact-1.md              artifact-2.md
                          │                           │
                          └───────── Read ────────────┘
                                     ↓
                              [Leader: hợp nhất]
                                     ↓
                              Sản phẩm cuối cùng
```

## Xử lý lỗi

| Tình huống | Chiến lược |
|------|------|
| 1 thành viên thất bại/dừng | Leader phát hiện → kiểm tra trạng thái qua SendMessage → khởi động lại hoặc tạo thành viên thay thế |
| Quá nửa thành viên thất bại | Báo người dùng và xác nhận có tiếp tục không |
| Timeout | Dùng kết quả từng phần đã thu thập, kết thúc thành viên chưa xong |
| Xung đột dữ liệu giữa thành viên | Ghi rõ nguồn rồi giữ cả hai, không xóa |
| Trạng thái công việc bị trễ | Leader kiểm tra bằng TaskGet rồi cập nhật thủ công bằng TaskUpdate |

## Kịch bản kiểm thử

### Luồng bình thường
1. Người dùng cung cấp {input}
2. Phase 1 cho ra {kết quả phân tích}
3. Phase 2 tạo đội ({N} thành viên + {M} công việc)
4. Phase 3 các thành viên tự điều phối thực hiện công việc
5. Phase 4 hợp nhất sản phẩm để tạo kết quả cuối
6. Phase 5 dọn dẹp đội
7. Kết quả mong đợi: tạo ra `{output-path}/{filename}`

### Luồng lỗi
1. Phase 3, {teammate-2} dừng do lỗi
2. Leader nhận thông báo rảnh
3. Kiểm tra trạng thái qua SendMessage → thử khởi động lại
4. Nếu khởi động lại thất bại, phân công lại công việc của {teammate-2} cho {teammate-1}
5. Tiến hành Phase 4 với kết quả còn lại
6. Ghi rõ "thiếu một phần dữ liệu từ {teammate-2}" trong báo cáo cuối
```

---

## Template B: Chế độ Subagent (phương án thay thế)

Khi chi phí giao tiếp đội là không cần thiết. Gọi trực tiếp bằng công cụ `Agent` và thu thập kết quả qua giá trị trả về.

```markdown
---
name: {domain}-orchestrator
description: "Orchestrator điều phối agent {domain}. {từ khóa khởi chạy lần đầu}. Có kèm từ khóa công việc tiếp theo."
---

## Chế độ thực thi: Subagent

## Cấu hình agent

| Agent | subagent_type | Vai trò | Skill | Output |
|---------|--------------|------|------|------|
| {agent-1} | {built-in hoặc tùy biến} | {vai trò} | {skill} | {output-file} |
| {agent-2} | ... | ... | ... | ... |

## Quy trình

### Phase 0: Kiểm tra ngữ cảnh
(Giống Template A — phân nhánh theo sự tồn tại của `_workspace/`)

### Phase 1: Chuẩn bị
1. Phân tích input
2. Tạo `_workspace/` (khi chạy lần đầu, hoặc ngay sau khi chuyển `_workspace/` hiện có sang thư mục lưu trữ khi chạy mới)

### Phase 2: Thực thi song song
Gọi đồng thời N công cụ Agent trong một message:

| Agent | Input | Output | model | run_in_background |
|---------|------|------|-------|-------------------|
| {agent-1} | {nguồn} | `_workspace/{phase}_{agent}_{artifact}.md` | opus | true |
| {agent-2} | {nguồn} | `_workspace/{phase}_{agent}_{artifact}.md` | opus | true |

### Phase 3: Hợp nhất
1. Thu thập giá trị trả về của từng agent
2. Thu thập sản phẩm dạng file bằng Read
3. Áp dụng logic hợp nhất → sản phẩm cuối cùng

### Phase 4: Dọn dẹp
1. Giữ lại `_workspace/`
2. Báo cáo tóm tắt kết quả

## Xử lý lỗi
- 1 agent thất bại: thử lại 1 lần. Nếu vẫn thất bại, ghi rõ thiếu sót và tiếp tục
- Quá nửa thất bại: báo người dùng và xác nhận có tiếp tục không
- Timeout: dùng kết quả từng phần đã thu thập
```

---

## Template C: Chế độ Hybrid

Dùng chế độ thực thi khác nhau theo từng Phase. Ghi rõ `**Chế độ thực thi:** {Team | Sub}` ở đầu mỗi Phase.

```markdown
---
name: {domain}-orchestrator
description: "Orchestrator {domain} (hybrid). {từ khóa}. Có kèm từ khóa công việc tiếp theo."
---

## Chế độ thực thi: Hybrid

| Phase | Chế độ | Lý do |
|-------|------|------|
| Phase 2 (thu thập song song) | Subagent | thu thập tài liệu độc lập, không cần giao tiếp đội |
| Phase 3 (hợp nhất theo đồng thuận) | Agent Team | cần thảo luận·đồng thuận với dữ liệu mâu thuẫn |
| Phase 4 (kiểm định độc lập) | Subagent | 1 agent QA kiểm định khách quan |

## Quy trình

### Phase 2: Thu thập dữ liệu song song
**Chế độ thực thi:** Subagent

Gọi song song N agent bằng công cụ Agent trong một message (`run_in_background: true`).
Mỗi kết quả lưu vào `_workspace/02_{agent}_raw.md`.

### Phase 3: Hợp nhất theo đồng thuận
**Chế độ thực thi:** Agent Team

1. Tạo đội hợp nhất bằng `TeamCreate` (editor + fact-checker + synthesizer)
2. Phân công công việc bằng `TaskCreate` — tất cả Read file `_workspace/02_*` từ Phase 2
3. Thành viên thảo luận dữ liệu mâu thuẫn qua `SendMessage`, đưa ra phương án đồng thuận dựa trên file
4. Sinh bản hợp nhất cuối cùng `_workspace/03_integrated.md`
5. Dọn dẹp đội bằng `TeamDelete`

### Phase 4: Kiểm định độc lập
**Chế độ thực thi:** Subagent

1 subagent QA đơn nhận `_workspace/03_integrated.md` làm input và sinh báo cáo kiểm định.
```

**Quy tắc chuyển đổi hybrid:**
- Team → Sub: phải dọn dẹp đội bằng `TeamDelete` trước khi gọi công cụ Agent
- Sub → Team: truyền sản phẩm file của subagent cho thành viên đội qua đường dẫn Read
- Team → Team: dọn dẹp đội trước rồi `TeamCreate` mới (mỗi phiên chỉ kích hoạt được 1 đội)

---

## Nguyên tắc viết

1. **Ghi rõ chế độ thực thi trước tiên** — ghi rõ một trong "Agent Team" / "Subagent" / "Hybrid" ở đầu orchestrator. Nếu hybrid, bắt buộc có bảng chế độ theo từng Phase
2. **Chế độ team cần ghi cụ thể cách dùng TeamCreate/SendMessage/TaskCreate** — cấu hình đội, đăng ký công việc, quy tắc giao tiếp
3. **Chế độ sub cần ghi đầy đủ tham số công cụ Agent** — name, subagent_type, prompt, run_in_background, model
4. **Đường dẫn file phải tuyệt đối** — cấm đường dẫn tương đối, đường dẫn rõ ràng dựa trên `_workspace/`
5. **Ghi rõ phụ thuộc giữa các Phase** — Phase nào phụ thuộc vào kết quả Phase nào. Hybrid cần nhấn mạnh đặc biệt điểm chuyển đổi chế độ
6. **Xử lý lỗi cần thực tế** — không giả định "mọi thứ đều thành công"
7. **Bắt buộc có kịch bản kiểm thử** — ít nhất 1 luồng bình thường + 1 luồng lỗi

## Từ khóa công việc tiếp theo khi viết description

Description của orchestrator chỉ có từ khóa khởi chạy lần đầu là chưa đủ. Phải có các cách diễn đạt công việc tiếp theo sau:

- chạy lại/thực thi lại/cập nhật/sửa/bổ sung
- "chỉ chạy lại {phần} của {domain}"
- "dựa trên kết quả trước", "cải thiện kết quả"
- yêu cầu thông thường liên quan tới domain (ví dụ: với harness chiến lược launch thì "launch", "quảng bá", "trending", v.v.)

Nếu thiếu từ khóa tiếp theo, sau lần chạy đầu tiên harness thực chất trở thành dead code.

## Tham khảo orchestrator thực tế

Cấu trúc cơ bản của orchestrator theo mẫu fan-out/fan-in:
chuẩn bị → Phase 0 (kiểm tra ngữ cảnh) → TeamCreate + TaskCreate → N thành viên thực thi song song → Read + hợp nhất → dọn dẹp.
Xem ví dụ đội nghiên cứu tại `references/team-examples.md`.
