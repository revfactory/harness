# Agent Team Design Patterns

## Chế độ thực thi: Agent Team vs Subagent

Hiểu sự khác biệt cốt lõi giữa hai chế độ thực thi và chọn chế độ phù hợp.

### Agent Team — chế độ mặc định

Team leader tạo đội bằng `TeamCreate`, các thành viên chạy như các instance Claude Code độc lập. Thành viên giao tiếp trực tiếp bằng `SendMessage` và tự điều phối bằng danh sách công việc chung (`TaskCreate`/`TaskUpdate`).

```
[Leader] ←→ [Thành viên A] ←→ [Thành viên B]
  ↕          ↕          ↕
  └──── Danh sách công việc chung ────┘
```

**Công cụ cốt lõi:**
- `TeamCreate`: tạo đội + spawn thành viên
- `SendMessage({to: name})`: gửi message tới một thành viên cụ thể
- `SendMessage({to: "all"})`: broadcast (chi phí cao, dùng hạn chế)
- `TaskCreate`/`TaskUpdate`: quản lý danh sách công việc chung

**Đặc điểm:**
- Thành viên có thể trao đổi trực tiếp, phản biện, kiểm chứng lẫn nhau
- Trao đổi thông tin giữa thành viên không cần qua leader
- Tự điều phối bằng danh sách công việc chung (có thể tự yêu cầu công việc)
- Khi thành viên rảnh, tự động thông báo cho leader
- Có thể dùng chế độ phê duyệt kế hoạch để review trước các tác vụ rủi ro

**Hạn chế:**
- Mỗi phiên chỉ **kích hoạt** được một đội (nhưng có thể giải thể và tạo đội mới giữa các Phase)
- Không thể lồng đội (thành viên không thể tạo đội của riêng mình)
- Leader cố định (không chuyển giao được)
- Chi phí token cao

**Mẫu tái cấu trúc đội:**
Khi mỗi Phase cần tổ hợp chuyên gia khác nhau, lưu sản phẩm của đội trước ra file → dọn dẹp đội → tạo đội mới. Sản phẩm của đội trước được giữ trong `_workspace/`, nên đội mới có thể truy cập bằng Read.

### Subagent — chế độ nhẹ

Main agent tạo subagent bằng công cụ `Agent`. Subagent chỉ trả kết quả về main, không giao tiếp với nhau.

```
[Main] → [Sub A] → trả kết quả
      → [Sub B] → trả kết quả
      → [Sub C] → trả kết quả
```

**Công cụ cốt lõi:**
- `Agent(prompt, subagent_type, run_in_background)`: tạo subagent

**Đặc điểm:**
- Nhẹ và nhanh
- Kết quả được tóm tắt trả về ngữ cảnh main
- Tiết kiệm token

**Hạn chế:**
- Subagent không giao tiếp được với nhau
- Main phải đảm nhiệm toàn bộ điều phối
- Không thể phối hợp/phản biện theo thời gian thực

### Cây quyết định chọn chế độ

```
Có 2 agent trở lên không?
├── Có → Có cần giao tiếp giữa các agent không?
│         ├── Có → Agent Team (mặc định)
│         │         Kiểm chứng chéo, chia sẻ phát hiện, phản hồi thời gian thực nâng cao chất lượng.
│         │
│         └── Không → Subagent cũng được
│                  Chỉ cần truyền kết quả, như producer-reviewer, expert pool.
│
└── Không (1 agent) → Subagent
              Một agent đơn không cần tạo đội.
```

> **Nguyên tắc cốt lõi:** Agent team là mặc định. Khi chọn subagent, hãy tự hỏi "liệu giao tiếp giữa thành viên có thực sự không cần thiết không?"

---

## Các loại kiến trúc Agent Team

### 1. Pipeline
Luồng công việc tuần tự. Output của agent trước là input của agent sau.

```
[Phân tích] → [Thiết kế] → [Triển khai] → [Kiểm định]
```

**Phù hợp khi:** mỗi bước phụ thuộc mạnh vào sản phẩm của bước trước
**Ví dụ:** viết tiểu thuyết — thế giới quan → nhân vật → cốt truyện → viết → biên tập
**Lưu ý:** điểm nghẽn làm chậm toàn bộ pipeline. Thiết kế từng bước càng độc lập càng tốt.
**Phù hợp với team mode:** phụ thuộc tuần tự mạnh nên lợi ích của team mode hạn chế. Tuy nhiên nếu pipeline có đoạn song song, team mode vẫn có ích.

### 2. Fan-out/Fan-in
Xử lý song song rồi hợp nhất kết quả. Thực hiện đồng thời các công việc độc lập.

```
         ┌→ [Chuyên gia A] ─┐
[Phân phối] → ├→ [Chuyên gia B] ─┼→ [Hợp nhất]
         └→ [Chuyên gia C] ─┘
```

**Phù hợp khi:** cần phân tích từ nhiều góc độ/lĩnh vực khác nhau trên cùng một input
**Ví dụ:** nghiên cứu tổng hợp — điều tra đồng thời nguồn chính thức/truyền thông/cộng đồng/bối cảnh → tổng hợp báo cáo
**Lưu ý:** chất lượng bước hợp nhất quyết định chất lượng tổng thể.
**Phù hợp với team mode:** mẫu tự nhiên nhất của agent team. **Bắt buộc phải cấu hình bằng agent team.** Các thành viên chia sẻ phát hiện và phản biện lẫn nhau, phát hiện của một agent có thể điều chỉnh tức thời hướng điều tra của agent khác, giúp chất lượng vượt xa điều tra đơn lẻ.

### 3. Expert Pool
Gọi chọn lọc chuyên gia phù hợp theo tình huống.

```
[Router] → { Chuyên gia A | Chuyên gia B | Chuyên gia C }
```

**Phù hợp khi:** cần xử lý khác nhau theo loại input
**Ví dụ:** review code — chỉ gọi chuyên gia an ninh/hiệu năng/kiến trúc tương ứng với lĩnh vực liên quan
**Lưu ý:** độ chính xác phân loại của router là yếu tố cốt lõi.
**Phù hợp với team mode:** subagent phù hợp hơn. Vì chỉ gọi chuyên gia cần thiết nên đội thường trực là không cần thiết.

### 4. Producer-Reviewer
Agent sinh nội dung và agent kiểm duyệt hoạt động theo cặp.

```
[Sinh nội dung] → [Kiểm duyệt] → (nếu có vấn đề) → chạy lại [Sinh nội dung]
```

**Phù hợp khi:** chất lượng sản phẩm quan trọng và có tiêu chí kiểm định khách quan
**Ví dụ:** webtoon — artist sinh nội dung → reviewer kiểm tra → tạo lại panel có vấn đề
**Lưu ý:** phải đặt số lần thử lại tối đa (2~3 lần) để tránh vòng lặp vô hạn.
**Phù hợp với team mode:** agent team hữu ích. Trao đổi phản hồi thời gian thực giữa producer↔reviewer bằng SendMessage.

### 5. Supervisor
Agent trung tâm quản lý trạng thái công việc và phân phối động cho các agent cấp dưới.

```
         ┌→ [Worker A]
[Supervisor] ─┼→ [Worker B]    ← Supervisor xem trạng thái và phân phối động
         └→ [Worker C]
```

**Phù hợp khi:** khối lượng công việc thay đổi hoặc cần quyết định phân phối tại runtime
**Ví dụ:** migration code quy mô lớn — supervisor phân tích danh sách file và giao theo batch cho worker
**Khác với fan-out:** fan-out phân phối cố định trước, supervisor điều chỉnh động theo tiến độ
**Lưu ý:** đặt đơn vị ủy quyền đủ lớn để supervisor không trở thành điểm nghẽn.
**Phù hợp với team mode:** danh sách công việc chung của agent team khớp tự nhiên với mẫu supervisor. Đăng ký công việc bằng TaskCreate, thành viên tự yêu cầu.

### 6. Hierarchical Delegation
Agent cấp trên ủy quyền đệ quy cho agent cấp dưới. Phân rã vấn đề phức tạp theo từng bước.

```
[Tổng chỉ huy] → [Trưởng nhóm A] → [Nhân viên A1]
                  → [Nhân viên A2]
       → [Trưởng nhóm B] → [Nhân viên B1]
```

**Phù hợp khi:** vấn đề tự nhiên phân rã theo cấu trúc phân cấp
**Ví dụ:** phát triển app full-stack — tổng chỉ huy → trưởng nhóm frontend → (UI/logic/test) + trưởng nhóm backend → (API/DB/test)
**Lưu ý:** độ sâu từ 3 cấp trở lên gây trễ và mất ngữ cảnh lớn. Khuyến nghị tối đa 2 cấp.
**Phù hợp với team mode:** agent team không lồng được (thành viên không tạo đội riêng). Có thể triển khai cấp 1 bằng team, cấp 2 bằng subagent, hoặc làm phẳng thành một đội duy nhất.

## Mẫu kết hợp

Trong thực tế, mẫu kết hợp phổ biến hơn mẫu đơn lẻ:

| Mẫu kết hợp | Cấu trúc | Ví dụ |
|----------|------|------|
| **Fan-out + Producer-Reviewer** | Sinh song song rồi kiểm duyệt từng cái | Dịch đa ngôn ngữ — dịch song song 4 ngôn ngữ → mỗi bản được reviewer bản ngữ kiểm tra |
| **Pipeline + Fan-out** | Song song hóa một phần các bước tuần tự | Phân tích (tuần tự) → triển khai (song song) → test tích hợp (tuần tự) |
| **Supervisor + Expert Pool** | Supervisor gọi động chuyên gia | Xử lý yêu cầu khách hàng — supervisor phân loại yêu cầu rồi gán chuyên gia phù hợp |

### Chế độ thực thi trong mẫu kết hợp

**Mặc định dùng agent team cho mọi mẫu kết hợp.** Giao tiếp tích cực giữa thành viên là động lực cốt lõi cho chất lượng kết quả.

| Kịch bản | Chế độ khuyến nghị | Lý do |
|---------|----------|------|
| **Nghiên cứu + Phân tích** | Agent Team | Chia sẻ phát hiện giữa người điều tra, thảo luận trực tiếp về thông tin mâu thuẫn |
| **Thiết kế + Triển khai + Kiểm định** | Agent Team | Vòng lặp phản hồi giữa người thiết kế↔người triển khai↔người kiểm định |
| **Supervisor + Worker** | Agent Team | Phân phối động bằng danh sách công việc chung, chia sẻ tiến độ giữa worker |
| **Sinh nội dung + Kiểm duyệt** | Agent Team | Phản hồi thời gian thực giữa producer↔reviewer giảm thiểu làm lại |

> Chỉ xem xét trộn với subagent khi một agent đơn thực hiện công việc một lần, hoàn toàn cách biệt.

## Chọn loại agent

Khi gọi agent, chỉ định loại qua tham số `subagent_type` của công cụ Agent. Thành viên agent team cũng có thể dùng định nghĩa agent tùy biến.

### Loại built-in

| Loại | Quyền truy cập công cụ | Dùng phù hợp cho |
|------|----------|-----------|
| `general-purpose` | Toàn bộ (bao gồm WebSearch, WebFetch) | Điều tra web, công việc tổng quát |
| `Explore` | Chỉ đọc (không có Edit/Write) | Khám phá codebase, phân tích |
| `Plan` | Chỉ đọc (không có Edit/Write) | Thiết kế kiến trúc, lập kế hoạch |

### Loại tùy biến

Định nghĩa agent tại `.claude/agents/{name}.md` rồi gọi bằng `subagent_type: "{name}"`. Agent tùy biến có quyền truy cập toàn bộ công cụ.

### Tiêu chí chọn

| Tình huống | Khuyến nghị | Lý do |
|------|------|------|
| Vai trò phức tạp, tái sử dụng ở nhiều phiên | **Loại tùy biến** (`.claude/agents/`) | Quản lý persona và nguyên tắc làm việc dưới dạng file |
| Điều tra/thu thập đơn giản, prompt là đủ | **`general-purpose`** + prompt chi tiết | Không cần file agent, đưa chỉ thị vào prompt |
| Chỉ cần đọc code (phân tích/review) | **`Explore`** | Tránh vô tình sửa file |
| Chỉ cần thiết kế/lập kế hoạch | **`Plan`** | Tập trung vào phân tích, tránh thay đổi code |
| Công việc triển khai cần sửa file | **Loại tùy biến** | Truy cập toàn bộ công cụ + chỉ thị chuyên biệt |

**Nguyên tắc:** Mọi agent phải được định nghĩa bằng file `.claude/agents/{name}.md`. Dù dùng loại built-in vẫn phải tạo file định nghĩa agent để ghi rõ vai trò·nguyên tắc·giao thức. Phải tồn tại dưới dạng file để tái sử dụng ở phiên sau, và giao thức giao tiếp đội phải được ghi rõ để đảm bảo chất lượng phối hợp.

**Model:** Mọi agent dùng `model: "opus"`. Khi gọi công cụ Agent, phải luôn ghi rõ tham số `model: "opus"`.

## Cấu trúc định nghĩa agent

```markdown
---
name: agent-name
description: "Mô tả vai trò 1-2 câu. Liệt kê từ khóa trigger."
---

# Agent Name — tóm tắt vai trò một dòng

Bạn là chuyên gia [vai trò] trong [lĩnh vực].

## Vai trò cốt lõi
1. Vai trò 1
2. Vai trò 2

## Nguyên tắc làm việc
- Nguyên tắc 1
- Nguyên tắc 2

## Giao thức input/output
- Input: [nhận gì từ đâu]
- Output: [viết gì vào đâu]
- Định dạng: [format file, cấu trúc]

## Giao thức giao tiếp đội (chế độ agent team)
- Nhận message: [nhận message gì từ ai]
- Gửi message: [gửi message gì tới ai]
- Yêu cầu công việc: [yêu cầu loại công việc nào từ danh sách công việc chung]

## Xử lý lỗi
- [hành động khi thất bại]
- [hành động khi timeout]

## Phối hợp
- Quan hệ với các agent khác
```

## Tiêu chí tách agent

| Tiêu chí | Tách | Hợp |
|------|------|------|
| Tính chuyên môn | Lĩnh vực khác nhau → tách | Lĩnh vực chồng lấp → hợp |
| Tính song song | Có thể thực thi độc lập → tách | Phụ thuộc tuần tự → xem xét hợp |
| Ngữ cảnh | Gánh nặng ngữ cảnh lớn → tách | Nhẹ và nhanh → hợp |
| Tính tái sử dụng | Dùng được ở đội khác → tách | Chỉ dùng trong đội này → xem xét hợp |

## Thiết kế tái sử dụng agent

Trước khi tạo agent mới, kiểm tra trùng lặp với agent hiện có. Khi xây dựng harness lặp đi lặp lại, các agent có vai trò chồng lấp dễ tích tụ dưới tên khác nhau.

| Tình huống | Hành động |
|------|------|
| Agent hiện có đã hoàn toàn bao quát vai trò mới | Cấm tạo mới — tái sử dụng agent hiện có |
| Agent hiện có bao quát một phần và có thể tổng quát hóa | Tổng quát hóa agent hiện có để mở rộng |
| Phần bao quát chỉ là trùng hợp do đặc thù lĩnh vực | Tiến hành tạo mới — giữ là agent riêng biệt |
| Phạm vi vai trò hoàn toàn khác | Tiến hành tạo mới |

**Nguyên tắc:** một agent tập trung vào một vai trò duy nhất sẽ có khả năng tái sử dụng cao hơn và giảm trùng lặp. Nếu có 2 vai trò trở lên, hãy xem xét tách trước.

**Khi tổng quát hóa agent hiện có:** hành vi của orchestrator/cấu trúc đội phụ thuộc vào agent đó có thể thay đổi. Kiểm tra phụ thuộc trước khi mở rộng, và dùng dry-run sau khi tổng quát hóa để xác nhận hành vi cũ vẫn được giữ.

## Phân biệt Skill vs Agent

| Phân biệt | Skill | Agent |
|------|-------------|-----------------|
| Định nghĩa | Tri thức thủ tục + bundle công cụ | Persona chuyên gia + nguyên tắc hành vi |
| Vị trí | `.claude/skills/` | `.claude/agents/` |
| Trigger | Khớp từ khóa yêu cầu người dùng | Gọi rõ ràng bằng công cụ Agent |
| Kích thước | Nhỏ~lớn (quy trình) | Nhỏ (định nghĩa vai trò) |
| Mục đích | "làm như thế nào" | "ai làm" |

Skill là **hướng dẫn thủ tục** mà agent tham chiếu khi thực hiện công việc.
Agent là **định nghĩa vai trò chuyên gia** sử dụng skill.

## Cách liên kết Skill ↔ Agent

3 cách agent sử dụng skill:

| Cách | Triển khai | Phù hợp khi |
|------|------|-----------|
| **Gọi công cụ Skill** | Ghi rõ trong prompt agent `dùng công cụ Skill gọi /skill-name` | Skill là quy trình độc lập và người dùng có thể gọi được |
| **Inline trong prompt** | Đưa trực tiếp nội dung skill vào định nghĩa agent | Skill ngắn (dưới 50 dòng) và chỉ dùng riêng cho agent này |
| **Nạp reference** | Dùng `Read` để nạp file references/ của skill khi cần | Nội dung skill lớn và chỉ cần có điều kiện |

Khuyến nghị: tính tái sử dụng cao → dùng công cụ Skill; chuyên dụng → inline; dữ liệu lớn → nạp reference.
