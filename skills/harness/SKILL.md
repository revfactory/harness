---
name: harness
description: "Cấu hình harness. Định nghĩa các agent chuyên biệt, và sinh ra các skill mà các agent đó sẽ sử dụng — đây là một meta-skill. Sử dụng khi: (1) yêu cầu '하네스 구성해줘', '하네스 구축해줘' (하네스 trong tiếng Hàn) hoặc 'xây dựng harness', 'thiết lập harness'; (2) yêu cầu '하네스 설계', '하네스 엔지니어링' hoặc 'thiết kế harness', 'kỹ thuật harness'; (3) khi xây dựng hệ thống tự động hóa dựa trên harness cho một lĩnh vực/dự án mới; (4) khi cấu hình lại hoặc mở rộng cấu hình harness hiện có; (5) khi có yêu cầu vận hành/bảo trì harness hiện có như '하네스 점검', '하네스 감사', '하네스 현황', '에이전트/스킬 동기화' hoặc 'kiểm tra harness', 'audit harness', 'hiện trạng harness', 'đồng bộ agent/skill'."
---

# Harness — Agent Team & Skill Architect

Meta-skill chuyên cấu hình harness phù hợp với lĩnh vực/dự án, định nghĩa vai trò của từng agent, và sinh ra các skill mà agent sẽ sử dụng.

**Nguyên tắc cốt lõi:**
1. Sinh ra định nghĩa agent (`.claude/agents/`) và skill (`.claude/skills/`).
2. **Sử dụng agent team là chế độ thực thi mặc định.**
3. **Đăng ký con trỏ harness vào CLAUDE.md.** — Chỉ ghi lại con trỏ tối thiểu (quy tắc trigger + lịch sử thay đổi) để skill orchestrator được trigger ở phiên làm việc mới.
4. **Harness không phải là vật cố định mà là hệ thống tiến hóa.** — Sau mỗi lần thực thi, phản ánh phản hồi và liên tục cập nhật agent, skill, CLAUDE.md.

## Quy trình

### Phase 0: Kiểm tra hiện trạng

Khi skill harness được trigger, việc đầu tiên là kiểm tra hiện trạng harness hiện có.

1. Đọc `project/.claude/agents/`, `project/.claude/skills/`, `project/CLAUDE.md`
2. Phân nhánh chế độ thực thi theo hiện trạng:
   - **Xây mới**: thư mục agent/skill không tồn tại hoặc trống → thực thi toàn bộ từ Phase 1
   - **Mở rộng harness có sẵn**: đã có harness và yêu cầu thêm agent/skill mới → chỉ thực thi các Phase cần thiết theo ma trận chọn Phase dưới đây
   - **Vận hành/bảo trì**: yêu cầu audit·sửa·đồng bộ harness hiện có → chuyển sang quy trình vận hành/bảo trì ở Phase 7-5

   **Ma trận chọn Phase khi mở rộng harness có sẵn:**
   | Loại thay đổi | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
   |----------|---------|---------|---------|---------|---------|---------|
   | Thêm agent | Bỏ qua (dùng kết quả Phase 0) | Chỉ quyết định bố trí | Bắt buộc (gồm 3-0) | Khi cần skill riêng (gồm 4-0) | Sửa orchestrator | Bắt buộc |
   | Thêm/sửa skill | Bỏ qua | Bỏ qua | Bỏ qua | Bắt buộc (gồm 4-0) | Khi thay đổi liên kết | Bắt buộc |
   | Đổi kiến trúc | Bỏ qua | Bắt buộc | Chỉ agent bị ảnh hưởng (gồm 3-0) | Chỉ skill bị ảnh hưởng (gồm 4-0) | Bắt buộc | Bắt buộc |
3. Đối chiếu danh sách agent/skill hiện có với nội dung ghi trong CLAUDE.md để phát hiện sai lệch (drift)
4. Báo cáo tóm tắt kết quả kiểm tra cho người dùng và xác nhận kế hoạch thực thi

### Phase 1: Phân tích lĩnh vực
1. Xác định lĩnh vực/dự án từ yêu cầu người dùng
2. Xác định loại công việc cốt lõi (sinh nội dung, kiểm định, biên tập, phân tích, v.v.)
3. Phân tích xung đột/trùng lặp với agent/skill hiện có, dựa trên kết quả kiểm tra ở Phase 0
4. Khám phá codebase của dự án — xác định tech stack, mô hình dữ liệu, module chính
5. **Nhận diện trình độ người dùng** — dựa vào ngữ cảnh hội thoại (thuật ngữ dùng, mức độ câu hỏi) để xác định trình độ kỹ thuật, và điều chỉnh tông giao tiếp tương ứng. Với người dùng ít kinh nghiệm coding, không dùng các thuật ngữ như "assertion", "JSON schema" mà không giải thích.

### Phase 2: Thiết kế kiến trúc đội

#### 2-1. Chọn chế độ thực thi

**Agent team là mặc định ưu tiên hàng đầu.** Khi 2 agent trở lên cần phối hợp, luôn xem xét agent team trước. Các thành viên tự điều phối thông qua giao tiếp trực tiếp (SendMessage) và danh sách công việc chung (TaskCreate), việc chia sẻ phát hiện, thảo luận xung đột, bổ sung thiếu sót giúp nâng cao chất lượng kết quả.

| Chế độ | Khi nào dùng | Đặc điểm |
|------|----------|----------|
| **Agent Team** (mặc định) | 2 người trở lên phối hợp, cần điều phối/trao đổi phản hồi theo thời gian thực, tham chiếu chéo sản phẩm trung gian | Tự điều phối bằng `TeamCreate` + `SendMessage` + `TaskCreate` |
| **Subagent** (phương án thay thế) | Công việc của một agent đơn, chỉ cần trả kết quả về main, khi chi phí giao tiếp đội là quá mức | Gọi trực tiếp công cụ `Agent`, chạy song song với `run_in_background` |
| **Hybrid** | Khi đặc điểm khác nhau theo từng Phase — ví dụ: thu thập song song (sub) → hợp nhất theo đồng thuận (team) | Trộn team/sub theo từng Phase |

**Trình tự ra quyết định:**
1. Đầu tiên xem xét có thể thiết kế bằng agent team không — 2 người trở lên thì là mặc định
2. Chỉ chọn subagent khi giao tiếp đội về cấu trúc là không cần thiết (chỉ truyền kết quả) và chi phí đội lớn hơn lợi ích
3. Nếu đặc điểm các Phase khác biệt rõ ràng, xem xét hybrid — ghi rõ chế độ thực thi của từng Phase trong orchestrator

> Bảng so sánh chi tiết và cây quyết định theo mẫu, xem mục "Chế độ thực thi" trong `references/agent-design-patterns.md`.

#### 2-2. Chọn mẫu kiến trúc

1. Phân rã công việc thành các lĩnh vực chuyên biệt
2. Quyết định cấu trúc đội agent (xem mẫu kiến trúc tại `references/agent-design-patterns.md`)
   - **Pipeline**: công việc phụ thuộc tuần tự
   - **Fan-out/Fan-in**: công việc song song độc lập
   - **Expert Pool**: gọi chọn lọc theo tình huống
   - **Producer-Reviewer**: sinh nội dung rồi kiểm tra chất lượng
   - **Supervisor**: agent trung tâm quản lý trạng thái và phân phối động
   - **Hierarchical Delegation**: agent cấp trên ủy quyền đệ quy cho cấp dưới

#### 2-3. Tiêu chí tách agent

Đánh giá theo 4 trục: tính chuyên môn, tính song song, ngữ cảnh, tính tái sử dụng. Bảng tiêu chí chi tiết xem mục "Tiêu chí tách agent" trong `references/agent-design-patterns.md`. Việc kiểm tra trùng lặp/tái sử dụng với agent hiện có được xử lý ở Phase 3-0.

### Phase 3: Sinh định nghĩa agent

#### 3-0. Kiểm tra trùng lặp với agent hiện có

Trước khi tạo agent mới, kiểm tra xem có trùng với agent hiện có trong `project/.claude/agents/` không. Khi xây dựng harness lặp đi lặp lại, các agent có vai trò chồng lấp dễ tích tụ dưới các tên khác nhau.

> Tiêu chí phân loại trùng lặp và thiết kế tái sử dụng, xem mục "Thiết kế tái sử dụng agent" trong `references/agent-design-patterns.md`.

**Mọi agent phải được định nghĩa bằng file `project/.claude/agents/{name}.md`.** Cấm đưa vai trò trực tiếp vào prompt của công cụ Agent mà không có file định nghĩa agent. Lý do:
- Định nghĩa agent phải tồn tại dưới dạng file để tái sử dụng ở phiên làm việc sau
- Giao thức giao tiếp đội phải được ghi rõ để đảm bảo chất lượng phối hợp giữa các agent
- Giá trị cốt lõi của harness là sự tách biệt giữa agent (ai làm) và skill (làm như thế nào)

Dù dùng các loại built-in (`general-purpose`, `Explore`, `Plan`), vẫn phải tạo file định nghĩa agent. Loại built-in được chỉ định qua tham số `subagent_type` của công cụ Agent, còn file định nghĩa agent chứa vai trò, nguyên tắc, giao thức.

**Cấu hình model:** Mọi agent dùng `model: "opus"`. Khi gọi công cụ Agent, phải luôn ghi rõ tham số `model: "opus"`. Chất lượng của harness gắn liền trực tiếp với khả năng suy luận của agent, và opus đảm bảo chất lượng cao nhất.

**Tái cấu trúc đội:** Mỗi phiên chỉ kích hoạt được một agent team, nhưng có thể giải thể đội và tạo đội mới giữa các Phase. Như mẫu pipeline, khi mỗi Phase cần một tổ hợp chuyên gia khác nhau, hãy lưu sản phẩm của đội trước ra file, dọn dẹp đội, rồi tạo đội mới.

Định nghĩa từng agent tại `project/.claude/agents/{name}.md`. Section bắt buộc: vai trò cốt lõi, nguyên tắc làm việc, giao thức input/output, xử lý lỗi, phối hợp. Ở chế độ agent team, thêm section `## Giao thức giao tiếp đội` để ghi rõ đối tượng nhận/gửi message và phạm vi yêu cầu công việc.

> Template định nghĩa và file mẫu đầy đủ, xem mục "Cấu trúc định nghĩa agent" trong `references/agent-design-patterns.md` + `references/team-examples.md`.

**Yêu cầu bắt buộc khi có agent QA:**
- Agent QA dùng loại `general-purpose` (`Explore` chỉ đọc, không thể chạy script kiểm định)
- Cốt lõi của QA không phải là "xác nhận tồn tại" mà là **"đối chiếu chéo điểm biên"** — đọc đồng thời response API và hook frontend để so sánh shape
- QA không chạy 1 lần sau khi hoàn thiện toàn bộ, mà chạy **dần dần ngay sau khi từng module hoàn thành** (incremental QA)
- Hướng dẫn chi tiết: xem `references/qa-agent-guide.md`

### Phase 4: Sinh skill

Sinh skill mà mỗi agent sẽ dùng tại `project/.claude/skills/{name}/SKILL.md`. Hướng dẫn viết chi tiết xem `references/skill-writing-guide.md`.

#### 4-0. Kiểm tra trùng lặp với skill hiện có

Trước khi tạo skill mới, kiểm tra xem có trùng với skill hiện có trong `project/.claude/skills/` không. Khi xây dựng harness lặp đi lặp lại, các skill có chức năng chồng lấp dễ tích tụ dưới các tên khác nhau.

> Tiêu chí phân loại trùng lặp và mẫu tổng quát hóa, xem mục "Thiết kế tái sử dụng skill" trong `references/skill-writing-guide.md`.

#### 4-1. Cấu trúc skill

```
skill-name/
├── SKILL.md (bắt buộc)
│   ├── YAML frontmatter (name, description bắt buộc)
│   └── Phần thân Markdown
└── Bundled Resources (tùy chọn)
    ├── scripts/    - code thực thi cho công việc lặp lại/tất định
    ├── references/ - tài liệu tham chiếu nạp có điều kiện
    └── assets/     - file dùng trong đầu ra (template, ảnh, v.v.)
```

#### 4-2. Viết Description — chủ động dẫn dắt trigger

Description là cơ chế trigger duy nhất của skill. Claude có xu hướng đánh giá trigger một cách bảo thủ, vì vậy hãy viết description theo hướng **chủ động ("pushy")**.

**Ví dụ tồi:** `"Skill xử lý file PDF"`
**Ví dụ tốt:** `"Thực hiện mọi công việc PDF: đọc file PDF, trích xuất văn bản/bảng, hợp nhất, tách, xoay, đóng watermark, mã hóa, OCR. Khi nhắc đến file .pdf hoặc yêu cầu sản phẩm PDF, phải dùng skill này."`

Cốt lõi: mô tả đầy đủ cả việc skill làm + tình huống trigger cụ thể, viết sao để phân biệt rõ với các trường hợp tương tự nhưng không nên trigger.

#### 4-3. Nguyên tắc viết phần thân

| Nguyên tắc | Mô tả |
|------|------|
| **Giải thích Why** | Thay vì chỉ thị áp đặt như "ALWAYS/NEVER", hãy truyền đạt lý do tại sao phải làm như vậy. Khi LLM hiểu lý do, nó sẽ phán đoán đúng cả trong trường hợp biên (edge case). |
| **Giữ gọn nhẹ (Lean)** | Cửa sổ ngữ cảnh là tài sản chung. Phần thân SKILL.md nên hướng tới dưới 500 dòng, xóa hoặc chuyển sang references/ những nội dung không tạo giá trị. |
| **Tổng quát hóa** | Thay vì quy tắc hẹp chỉ đúng với ví dụ cụ thể, hãy giải thích nguyên lý để áp dụng được cho nhiều input khác nhau. Cấm overfitting. |
| **Bundling code lặp lại** | Nếu phát hiện script mà các agent thường viết lại trong quá trình test, hãy bundling sẵn vào `scripts/`. |
| **Viết theo lối ra lệnh** | Dùng tông ra lệnh/chỉ thị như "thực hiện...", "phải...". |

#### 4-4. Progressive Disclosure (công khai thông tin theo từng bước)

Skill quản lý ngữ cảnh bằng hệ thống nạp 3 cấp độ:

| Cấp độ | Thời điểm nạp | Mục tiêu kích thước |
|------|----------|----------|
| **Metadata** (name + description) | Luôn tồn tại trong ngữ cảnh | ~100 từ |
| **Phần thân SKILL.md** | Khi skill được trigger | <500 dòng |
| **references/** | Chỉ khi cần | Không giới hạn (script chạy được mà không cần nạp) |

**Quy tắc quản lý kích thước:**
- Khi SKILL.md gần 500 dòng, tách nội dung chi tiết sang references/, và để lại con trỏ "khi nào đọc file này" trong phần thân
- File reference từ 300 dòng trở lên cần có **mục lục (ToC)** ở đầu
- Nếu có biến thể theo từng lĩnh vực/framework, tách theo lĩnh vực dưới references/ để chỉ nạp file liên quan

```
cloud-deploy/
├── SKILL.md (quy trình + hướng dẫn chọn)
└── references/
    ├── aws.md    ← chỉ nạp khi chọn AWS
    ├── gcp.md
    └── azure.md
```

#### 4-5. Nguyên tắc liên kết skill-agent

- 1 agent ↔ 1~N skill (1:1 hoặc 1:nhiều)
- Có thể có skill được nhiều agent dùng chung
- Skill chứa "làm như thế nào", agent chứa "ai làm"

> Mẫu viết chi tiết, ví dụ, chuẩn data schema, xem `references/skill-writing-guide.md`.

### Phase 5: Tích hợp và điều phối

Orchestrator là một dạng đặc biệt của skill, kết nối các agent và skill riêng lẻ thành một quy trình duy nhất để điều phối toàn đội. Nếu các skill riêng lẻ sinh ra ở Phase 4 định nghĩa "mỗi agent làm gì và làm như thế nào", thì orchestrator định nghĩa "ai phối hợp với ai, khi nào, theo thứ tự nào". Template cụ thể xem `references/orchestrator-template.md`.

**Sửa orchestrator khi mở rộng harness có sẵn:** Khi mở rộng harness có sẵn (không phải xây mới), sửa orchestrator hiện có thay vì tạo mới. Khi thêm agent, phản ánh agent mới vào cấu trúc đội · phân công công việc · luồng dữ liệu, và thêm từ khóa trigger liên quan đến agent mới vào description.

Mẫu orchestrator thay đổi theo chế độ thực thi đã chọn ở Phase 2-1:

#### 5-0. Mẫu orchestrator (theo từng chế độ)

**Mẫu Agent Team (mặc định):**
Orchestrator tạo đội bằng `TeamCreate`, phân công công việc bằng `TaskCreate`. Các thành viên giao tiếp trực tiếp bằng `SendMessage` và tự điều phối. Leader (orchestrator) giám sát tiến độ và tổng hợp kết quả.

```
[Orchestrator/Leader]
    ├── TeamCreate(team_name, members)
    ├── TaskCreate(tasks with dependencies)
    ├── Các thành viên tự điều phối (SendMessage)
    ├── Thu thập và tổng hợp kết quả
    └── Dọn dẹp đội
```

**Mẫu Subagent (phương án thay thế):**
Orchestrator gọi trực tiếp subagent bằng công cụ `Agent`. Thực thi song song dùng `run_in_background: true`, kết quả chỉ trả về cho main. Dùng khi không cần giao tiếp đội và muốn giảm chi phí.

```
[Orchestrator]
    ├── Agent(agent-1, run_in_background=true)
    ├── Agent(agent-2, run_in_background=true)
    ├── Chờ và thu thập kết quả
    └── Sinh sản phẩm tổng hợp
```

**Mẫu Hybrid:**
Trộn chế độ khác nhau theo từng Phase. Tổ hợp thường dùng:
- **Thu thập song song (sub) → hợp nhất theo đồng thuận (team)**: Phase 2 dùng subagent thu thập tài liệu độc lập song song → Phase 3 tạo đội để thảo luận và hợp nhất theo đồng thuận
- **Tạo đội (team) → kiểm định (sub)**: Phase 2 đội tạo bản nháp → Phase 3 một subagent đơn kiểm định độc lập
- **Tái cấu trúc đội giữa các Phase**: mỗi Phase `TeamDelete` rồi `TeamCreate` mới, chèn lệnh gọi subagent vào giữa

Khi chọn hybrid, ghi rõ chế độ thực thi của Phase đó ở đầu mỗi section Phase trong orchestrator (ví dụ: `**Chế độ thực thi:** Agent Team`).

#### 5-1. Giao thức truyền dữ liệu

Ghi rõ cách truyền dữ liệu giữa các agent trong orchestrator:

| Chiến lược | Cách thức | Chế độ áp dụng | Phù hợp khi |
|------|------|----------|-----------|
| **Dựa trên message** | Giao tiếp trực tiếp giữa thành viên bằng `SendMessage` | Team | Điều phối theo thời gian thực, trao đổi phản hồi, truyền trạng thái nhẹ |
| **Dựa trên task** | Chia sẻ trạng thái công việc bằng `TaskCreate`/`TaskUpdate` | Team | Theo dõi tiến độ, quản lý quan hệ phụ thuộc, tự yêu cầu công việc |
| **Dựa trên file** | Ghi và đọc file tại đường dẫn đã thống nhất | Team + Sub | Dữ liệu lớn, sản phẩm có cấu trúc, cần audit trail |
| **Dựa trên giá trị trả về** | Message trả về của công cụ `Agent` | Sub | Main thu thập trực tiếp kết quả từ subagent |

**Tổ hợp khuyến nghị (chế độ team):** dựa trên task (điều phối) + dựa trên file (sản phẩm) + dựa trên message (giao tiếp thời gian thực)
**Tổ hợp khuyến nghị (chế độ sub):** dựa trên giá trị trả về (thu thập kết quả) + dựa trên file (sản phẩm lớn)
**Hybrid:** áp dụng tổ hợp phù hợp theo chế độ thực thi của từng Phase

Quy tắc khi truyền dựa trên file:
- Tạo thư mục `_workspace/` dưới thư mục làm việc để lưu sản phẩm trung gian
- Quy ước tên file: `{phase}_{agent}_{artifact}.{ext}` (ví dụ: `01_analyst_requirements.md`)
- Chỉ xuất sản phẩm cuối cùng ra đường dẫn người dùng chỉ định, giữ lại file trung gian (`_workspace/`) (dùng cho kiểm định/audit trail sau này)

#### 5-2. Xử lý lỗi

Đưa chính sách xử lý lỗi vào orchestrator. Nguyên tắc cốt lõi: thử lại 1 lần, nếu vẫn lỗi thì tiếp tục mà không có kết quả đó (ghi rõ thiếu sót trong báo cáo), dữ liệu mâu thuẫn không xóa mà ghi kèm nguồn.

> Bảng chiến lược theo từng loại lỗi và chi tiết triển khai, xem mục "Xử lý lỗi" trong `references/orchestrator-template.md`.

#### 5-3. Hướng dẫn kích thước đội

| Quy mô công việc | Số thành viên khuyến nghị | Số công việc/thành viên |
|----------|------------|--------------|
| Nhỏ (5~10 công việc) | 2~3 người | 3~5 |
| Trung (10~20 công việc) | 3~5 người | 4~6 |
| Lớn (20+ công việc) | 5~7 người | 4~5 |

> Càng nhiều thành viên, chi phí điều phối càng lớn. 3 thành viên tập trung tốt hơn 5 thành viên phân tán.

#### 5-4. Đăng ký con trỏ harness vào CLAUDE.md

Sau khi hoàn tất cấu hình harness, đăng ký con trỏ tối thiểu vào `CLAUDE.md` của dự án. Vì CLAUDE.md được nạp ở mọi phiên mới, chỉ cần ghi sự tồn tại của harness và quy tắc trigger, skill orchestrator sẽ xử lý phần còn lại.

**Template CLAUDE.md:**

````markdown
## Harness: {Tên lĩnh vực}

**Mục tiêu:** {mục tiêu cốt lõi của harness, một dòng}

**Trigger:** Khi có yêu cầu liên quan đến {lĩnh vực}, dùng skill `{orchestrator-skill-name}`. Câu hỏi đơn giản có thể trả lời trực tiếp.

**Lịch sử thay đổi:**
| Ngày | Nội dung thay đổi | Đối tượng | Lý do |
|------|----------|------|------|
| {YYYY-MM-DD} | Cấu hình ban đầu | Toàn bộ | - |
````

**Những gì KHÔNG đưa vào CLAUDE.md:** danh sách agent, danh sách skill, cấu trúc thư mục, chi tiết quy tắc thực thi. Lý do: danh sách agent/skill được quản lý bởi skill orchestrator và `.claude/agents/`, `.claude/skills/`, nên đưa vào CLAUDE.md là trùng lặp. Cấu trúc thư mục có thể kiểm tra trực tiếp trên hệ thống file. CLAUDE.md chỉ chứa **con trỏ (quy tắc trigger) + lịch sử thay đổi**.

#### 5-5. Hỗ trợ công việc tiếp theo

Orchestrator không chỉ xử lý lần thực thi đầu tiên mà còn phải xử lý các công việc tiếp theo. Đảm bảo 3 điều sau:

**1. Description của orchestrator phải có từ khóa công việc tiếp theo:**
Chỉ từ khóa khởi tạo ban đầu sẽ không trigger được yêu cầu tiếp theo. Các cách diễn đạt cần có trong description:
- "chạy lại", "thực thi lại", "cập nhật", "sửa", "bổ sung"
- "chỉ chạy lại {công việc con} của {lĩnh vực}"
- "dựa trên kết quả trước", "cải thiện kết quả"

**2. Thêm bước kiểm tra ngữ cảnh vào Phase 1 của orchestrator:**
Khi bắt đầu quy trình, kiểm tra sự tồn tại của sản phẩm hiện có để quyết định chế độ thực thi:
- `_workspace/` tồn tại + người dùng yêu cầu sửa một phần → **Chạy lại một phần** (chỉ gọi lại agent liên quan)
- `_workspace/` tồn tại + người dùng cung cấp input mới → **Chạy mới** (chuyển `_workspace/` hiện có thành `_workspace_prev/`)
- `_workspace/` không tồn tại → **Chạy lần đầu**

**3. Đưa hướng dẫn gọi lại vào định nghĩa agent:**
Ghi rõ trong file `.md` của từng agent "hành vi khi đã có sản phẩm trước":
- Nếu file kết quả trước tồn tại, đọc và phản ánh điểm cần cải thiện
- Nếu có phản hồi từ người dùng, chỉ sửa phần liên quan

> Xem section "Phase 0: Kiểm tra ngữ cảnh" trong template orchestrator: `references/orchestrator-template.md`

### Phase 6: Kiểm định và kiểm thử

Kiểm định harness đã sinh ra. Phương pháp kiểm thử chi tiết xem `references/skill-testing-guide.md`.

#### 6-1. Kiểm định cấu trúc

- Xác nhận mọi file agent ở đúng vị trí
- Kiểm định frontmatter (name, description) của skill
- Kiểm tra tính nhất quán của tham chiếu giữa các agent
- Xác nhận không có command nào được sinh ra

#### 6-2. Kiểm định theo chế độ thực thi

- **Agent Team**: kiểm tra đường giao tiếp giữa thành viên, quan hệ phụ thuộc công việc, độ phù hợp kích thước đội
- **Subagent**: kiểm tra kết nối input/output của từng agent, cấu hình `run_in_background`, logic thu thập giá trị trả về
- **Hybrid**: kiểm tra chế độ thực thi của từng Phase đã được ghi rõ trong orchestrator chưa, và việc truyền dữ liệu không bị đứt ở biên Phase (khi chuyển từ team → sub, sản phẩm của team có được nối với input của sub không)

#### 6-3. Kiểm thử thực thi skill

Thực hiện kiểm thử thực thi thực tế cho mỗi skill đã sinh:

1. **Viết prompt kiểm thử** — viết 2~3 prompt kiểm thử thực tế cho mỗi skill. Viết bằng câu cụ thể, tự nhiên giống người dùng thực sẽ nhập.

2. **So sánh With-skill vs Without-skill** — nếu có thể, chạy song song lượt có skill và lượt không có skill để xác nhận giá trị gia tăng của skill. Spawn 2 agent cho mỗi trường hợp:
   - **With-skill**: đọc skill và thực hiện công việc
   - **Without-skill (baseline)**: thực hiện cùng prompt nhưng không có skill

3. **Đánh giá kết quả** — đánh giá chất lượng sản phẩm cả định tính (review người dùng) và định lượng (dựa trên assertion). Nếu sản phẩm có thể kiểm định khách quan (tạo file, trích xuất dữ liệu, v.v.) hãy định nghĩa assertion; nếu chủ quan (văn phong, thiết kế) thì dựa vào phản hồi người dùng.

4. **Vòng lặp cải tiến lặp lại** — nếu phát hiện vấn đề trong kết quả kiểm thử:
   - **Tổng quát hóa** phản hồi rồi sửa skill (cấm sửa hẹp chỉ đúng với một ví dụ cụ thể)
   - Kiểm thử lại sau khi sửa
   - Lặp lại đến khi người dùng hài lòng hoặc không còn cải thiện đáng kể nào

5. **Bundling pattern lặp lại** — nếu phát hiện code mà các agent thường viết chung trong quá trình kiểm thử (ví dụ: cùng tạo một helper script giống nhau trong mọi test), hãy bundling sẵn code đó vào `scripts/`.

#### 6-4. Kiểm định trigger

Kiểm định description của từng skill có trigger đúng không:

1. **Truy vấn should-trigger** (8~10 câu) — các cách diễn đạt khác nhau cần trigger skill (trang trọng/thân mật, rõ ràng/ngụ ý)
2. **Truy vấn should-NOT-trigger** (8~10 câu) — các truy vấn "near-miss" có từ khóa tương tự nhưng phù hợp với công cụ/skill khác, không phải skill này

**Cốt lõi khi viết near-miss:** truy vấn rõ ràng không liên quan như "viết hàm Fibonacci" không có giá trị kiểm thử. Truy vấn có **biên mơ hồ** như "trích xuất biểu đồ trong file Excel này thành PNG" (skill xlsx vs chuyển đổi ảnh) mới là case kiểm thử tốt.

Cũng kiểm tra xung đột trigger với skill hiện có ở bước này.

#### 6-5. Kiểm thử dry-run

- Xem lại thứ tự Phase của skill orchestrator có hợp lý không
- Xác nhận đường truyền dữ liệu không có khoảng trống (dead link)
- Xác nhận input của mọi agent khớp với output của Phase trước
- Xác nhận đường dẫn fallback cho từng kịch bản lỗi có thể thực thi được

#### 6-6. Viết kịch bản kiểm thử

- Thêm section `## Kịch bản kiểm thử` vào skill orchestrator
- Mô tả 1 luồng bình thường + ít nhất 1 luồng lỗi

### Phase 7: Tiến hóa harness

Harness không phải là sản phẩm tĩnh tạo một lần rồi xong. Đó là một hệ thống liên tục tiến hóa theo phản hồi của người dùng.

#### 7-1. Thu thập phản hồi sau thực thi

Sau mỗi lần thực thi harness, hỏi người dùng phản hồi:
- "Có phần nào trong kết quả cần cải thiện không?"
- "Bạn có muốn thay đổi gì về cấu hình đội agent hoặc quy trình không?"

Nếu không có phản hồi thì bỏ qua. Không ép buộc, nhưng phải luôn tạo cơ hội.

#### 7-2. Đường dẫn phản ánh phản hồi

Đối tượng cần sửa khác nhau theo loại phản hồi:

| Loại phản hồi | Đối tượng sửa | Ví dụ |
|-----------|----------|------|
| Chất lượng sản phẩm | Skill của agent liên quan | "Phân tích quá hời hợt" → thêm tiêu chí độ sâu vào skill |
| Vai trò agent | File định nghĩa agent `.md` | "Cần review an ninh nữa" → thêm agent mới |
| Thứ tự quy trình | Skill orchestrator | "Cần kiểm định trước" → đổi thứ tự Phase |
| Cấu trúc đội | Orchestrator + agent | "Hai cái này nên hợp lại" → hợp nhất agent |
| Thiếu trigger | Description của skill | "Diễn đạt này không hoạt động" → mở rộng description |

#### 7-3. Lịch sử thay đổi

Mọi thay đổi được ghi vào bảng **Lịch sử thay đổi** trong CLAUDE.md (cùng bảng với section "Lịch sử thay đổi" trong template Phase 5-4):

```markdown
**Lịch sử thay đổi:**
| Ngày | Nội dung thay đổi | Đối tượng | Lý do |
|------|----------|------|------|
| 2026-04-05 | Cấu hình ban đầu | Toàn bộ | - |
| 2026-04-07 | Thêm agent QA | agents/qa.md | Phản hồi thiếu kiểm định chất lượng sản phẩm |
| 2026-04-10 | Thêm hướng dẫn tông văn | skills/content-creator | Phản hồi "quá cứng nhắc" |
```

Lịch sử này giúp theo dõi harness đã tiến hóa theo hướng nào và ngăn chặn thoái lui (regression).

#### 7-4. Trigger tiến hóa

Không chỉ khi người dùng yêu cầu rõ ràng "sửa harness", mà cũng đề xuất tiến hóa trong các trường hợp sau:
- Khi cùng loại phản hồi lặp lại 2 lần trở lên
- Khi phát hiện mẫu agent thất bại lặp lại
- Khi quan sát thấy người dùng bỏ qua orchestrator để làm thủ công

#### 7-5. Quy trình vận hành/bảo trì

Thực hiện có hệ thống việc kiểm tra · sửa · đồng bộ harness hiện có. Theo quy trình này khi vào nhánh "vận hành/bảo trì" từ Phase 0.

**Bước 1: Kiểm tra hiện trạng**
- So sánh danh sách file `.claude/agents/` với cấu hình agent trong skill orchestrator → tạo danh sách sai lệch
- So sánh danh sách thư mục `.claude/skills/` với cấu hình skill trong skill orchestrator → tạo danh sách sai lệch
- Báo cáo kết quả kiểm tra cho người dùng

**Bước 2: Thêm/sửa dần dần**
- Thực hiện thêm/sửa/xóa agent, thêm/sửa/xóa skill theo yêu cầu người dùng
- Mỗi lần một thay đổi, thực hiện Bước 3 (đồng bộ) ngay sau mỗi thay đổi

**Bước 3: Cập nhật lịch sử thay đổi CLAUDE.md**
- Ghi ngày, nội dung thay đổi, đối tượng, lý do vào bảng lịch sử thay đổi

**Bước 4: Xác minh thay đổi**
- Kiểm định cấu trúc agent/skill đã sửa (theo tiêu chí Phase 6-1)
- Nếu phạm vi sửa ảnh hưởng tới trigger, kiểm định trigger (theo tiêu chí Phase 6-4)
- Khi thay đổi lớn (đổi kiến trúc, thêm/xóa từ 3 agent trở lên), thực hiện cả Phase 6-3 (kiểm thử thực thi), 6-5 (dry-run)
- Xác nhận cuối cùng CLAUDE.md khớp với file thực tế

## Checklist sản phẩm đầu ra

Sau khi hoàn thành, kiểm tra:

- [ ] `project/.claude/agents/` — **bắt buộc sinh file định nghĩa agent** (dù dùng loại built-in vẫn phải tạo file)
- [ ] `project/.claude/skills/` — các file skill (SKILL.md + references/)
- [ ] 1 skill orchestrator (bao gồm luồng dữ liệu + xử lý lỗi + kịch bản kiểm thử)
- [ ] Ghi rõ chế độ thực thi (chọn trong Agent Team / Subagent / Hybrid, nếu hybrid ghi rõ chế độ theo từng Phase)
- [ ] Mọi lệnh gọi Agent đều ghi rõ tham số `model: "opus"`
- [ ] Đã kiểm tra trùng lặp với agent hiện có trước khi tạo agent mới (Phase 3-0)
- [ ] Đã kiểm tra trùng lặp với skill hiện có trước khi tạo skill mới (Phase 4-0)
- [ ] `.claude/commands/` — không sinh ra gì cả
- [ ] Không xung đột với agent/skill hiện có
- [ ] Description của skill được viết chủ động ("pushy") — **có kèm từ khóa công việc tiếp theo**
- [ ] Phần thân SKILL.md dưới 500 dòng, vượt quá thì tách sang references/
- [ ] Đã kiểm thử thực thi với 2~3 prompt kiểm thử
- [ ] Đã hoàn thành kiểm định trigger (should-trigger + should-NOT-trigger)
- [ ] **Đã đăng ký con trỏ harness vào CLAUDE.md** (quy tắc trigger + lịch sử thay đổi)
- [ ] **Đã ghi thêm/xóa/sửa agent/skill vào lịch sử thay đổi CLAUDE.md**
- [ ] **Orchestrator Phase 1 có bước kiểm tra ngữ cảnh** (phân biệt chạy lần đầu/tiếp theo/chạy lại một phần)

## Tham khảo

- Mẫu harness: `references/agent-design-patterns.md`
- Ví dụ harness hiện có (gồm file mẫu đầy đủ): `references/team-examples.md`
- Template orchestrator: `references/orchestrator-template.md`
- **Hướng dẫn viết skill**: `references/skill-writing-guide.md` — mẫu viết, ví dụ, chuẩn data schema
- **Hướng dẫn kiểm thử skill**: `references/skill-testing-guide.md` — phương pháp kiểm thử/đánh giá/cải tiến lặp lại
- **Hướng dẫn agent QA**: `references/qa-agent-guide.md` — tham khảo khi đưa agent QA vào build harness. Bao gồm phương pháp kiểm định tính nhất quán tích hợp, mẫu bug ở điểm biên, template định nghĩa agent QA. Dựa trên 7 case bug thực tế phát hiện trong dự án thật.
