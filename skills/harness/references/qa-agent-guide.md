# Hướng dẫn thiết kế agent QA

Hướng dẫn tham khảo khi đưa agent QA vào build harness. Dựa trên các mẫu bug phát hiện trong dự án thực tế (SatangSlide) và phân tích nguyên nhân gốc rễ, cung cấp phương pháp kiểm định giúp bắt được hệ thống các lỗi mà QA dễ bỏ sót.

---

## Mục lục

1. Các mẫu lỗi mà agent QA bỏ sót
2. Kiểm định tính nhất quán tích hợp (Integration Coherence Verification)
3. Nguyên tắc thiết kế agent QA
4. Template checklist kiểm định
5. Template định nghĩa agent QA

---

## 1. Các mẫu lỗi mà agent QA bỏ sót

### 1-1. Sai lệch ở điểm biên (Boundary Mismatch)

Lỗi phổ biến nhất. Hai component đều được triển khai "đúng" riêng lẻ, nhưng hợp đồng giao tiếp bị lệch tại điểm kết nối.

| Điểm biên | Ví dụ sai lệch | Lý do bị bỏ sót |
|--------|-----------|-----------|
| API response → hook frontend | API trả `{ projects: [...] }`, hook kỳ vọng `SlideProject[]` | Mỗi bên kiểm định riêng đều ổn, không có đối chiếu chéo |
| Tên field API response → định nghĩa type | API dùng `thumbnailUrl` (camelCase), type dùng `thumbnail_url` (snake_case) | Cast bằng generic TypeScript khiến compiler không bắt được |
| Đường dẫn file → href link | Page nằm ở `/dashboard/create` nhưng link chỉ định `/create` | Không đối chiếu chéo cấu trúc file với href |
| Map chuyển trạng thái → cập nhật status thực tế | Map định nghĩa `generating_template → template_approved`, code thiếu chuyển trạng thái này | Chỉ xác nhận map tồn tại, không truy theo toàn bộ code cập nhật |
| API endpoint → hook frontend | API tồn tại nhưng không có hook tương ứng (không bị gọi) | Không map 1:1 giữa danh sách API và danh sách hook |
| Response ngay lập tức → kết quả bất đồng bộ | API trả ngay `{ status }`, frontend truy cập `data.failedIndices` | Chỉ kiểm tra type, không phân biệt response đồng bộ/bất đồng bộ |

### 1-2. Vì sao review code tĩnh không bắt được

- **Hạn chế của generic TypeScript**: `fetchJson<SlideProject[]>()` — dù response thực tế là `{ projects: [...] }`, compile vẫn pass
- **`npm run build` pass ≠ hoạt động đúng**: khi dùng type casting, `any`, generic, build vẫn thành công nhưng runtime thất bại
- **Khác biệt giữa kiểm định tồn tại vs kiểm định kết nối**: "API có tồn tại không?" và "response của API có khớp với kỳ vọng của bên gọi không?" là hai loại kiểm định hoàn toàn khác

---

## 2. Kiểm định tính nhất quán tích hợp (Integration Coherence Verification)

Các vùng **kiểm định đối chiếu chéo** bắt buộc phải có trong agent QA.

### 2-1. Đối chiếu chéo type API response ↔ hook frontend

**Phương pháp**: so sánh điểm gọi `NextResponse.json()` trong mỗi API route với tham số type của `fetchJson<T>` trong hook tương ứng.

```
Bước kiểm định:
1. Trích xuất shape của object truyền vào NextResponse.json() trong API route
2. Kiểm tra type T trong fetchJson<T> của hook tương ứng
3. So sánh shape và T có khớp không
4. Kiểm tra có wrapping không (nếu API trả { data: [...] }, hook có lấy .data ra không)
```

**Mẫu cần đặc biệt lưu ý:**
- API phân trang: `{ items: [], total, page }` vs frontend kỳ vọng array
- Sai lệch giữa field DB dạng snake_case → API response dạng camelCase → định nghĩa type frontend
- Khác biệt shape giữa response ngay lập tức (202 Accepted) và kết quả cuối cùng

### 2-2. Map đường dẫn file ↔ đường dẫn link/router

**Phương pháp**: trích xuất URL path của các file page dưới `src/app/`, đối chiếu với mọi giá trị `href`, `router.push()`, `redirect()` trong code.

```
Bước kiểm định:
1. Trích xuất pattern URL từ đường dẫn file page.tsx dưới src/app/
   - (group) → loại bỏ khỏi URL
   - [param] → dynamic segment
2. Thu thập mọi giá trị href=, router.push(, redirect( trong code
3. Kiểm tra mỗi link có khớp với đường dẫn page thực tế tồn tại không
4. Lưu ý tiền tố URL của page bên trong route group (ví dụ: dưới dashboard/)
```

### 2-3. Theo dõi tính đầy đủ của chuyển trạng thái

**Phương pháp**: trích xuất mọi lệnh cập nhật `status:` trong code và đối chiếu với map chuyển trạng thái.

```
Bước kiểm định:
1. Trích xuất danh sách chuyển trạng thái được phép từ map (STATE_TRANSITIONS)
2. Tìm pattern .update({ status: "..." }) trong mọi API route
3. Kiểm tra mỗi chuyển trạng thái có được định nghĩa trong map không
4. Xác định chuyển trạng thái nào được định nghĩa trong map nhưng không được thực thi trong code (chuyển trạng thái chết)
5. Đặc biệt: kiểm tra chuyển từ trạng thái trung gian (ví dụ generating_template) sang trạng thái cuối (template_approved) có bị thiếu không
```

### 2-4. Map 1:1 API endpoint ↔ hook frontend

**Phương pháp**: liệt kê toàn bộ API route và hook frontend để kiểm tra có khớp cặp không.

```
Bước kiểm định:
1. Trích xuất danh sách endpoint theo HTTP method từ route.ts dưới src/app/api/
2. Trích xuất danh sách URL được gọi fetch từ use*.ts dưới src/hooks/
3. Xác định API endpoint nào không được hook nào gọi → đánh dấu "không sử dụng"
4. Phán đoán "không sử dụng" là có chủ ý (như API quản trị) hay không (thiếu lệnh gọi)
```

---

## 3. Nguyên tắc thiết kế agent QA

### 3-1. Dùng loại general-purpose, không dùng Explore

Nếu agent QA dùng loại `Explore` thì chỉ đọc được. Nhưng QA hiệu quả cần:
- Tìm pattern bằng Grep (trích xuất mọi `NextResponse.json()`)
- Đối chiếu tự động bằng chạy script (API shape vs hook type)
- Có thể sửa khi cần

**Khuyến nghị**: đặt loại `general-purpose`, nhưng ghi rõ trong định nghĩa agent giao thức "kiểm định → báo cáo → yêu cầu sửa".

### 3-2. Checklist ưu tiên "đối chiếu chéo" hơn "xác nhận tồn tại"

| Checklist yếu | Checklist mạnh |
|---------------|---------------|
| API endpoint có tồn tại không? | Shape response của API endpoint khớp với type của hook tương ứng không? |
| Map chuyển trạng thái có được định nghĩa không? | Mọi code cập nhật status có khớp với chuyển trạng thái trong map không? |
| File page có tồn tại không? | Mọi link trong code có chỉ tới page thực tế tồn tại không? |
| Có dùng TypeScript strict mode không? | Có an toàn type nào bị qua mặt bởi generic casting không? |

### 3-3. Nguyên tắc "đọc cả hai bên đồng thời"

Để bắt được bug ở điểm biên, QA không thể chỉ đọc một bên. Bắt buộc phải:
- Đọc API route **và** hook tương ứng **cùng nhau**
- Đọc map chuyển trạng thái **và** code cập nhật thực tế **cùng nhau**
- Đọc cấu trúc file **và** đường dẫn link **cùng nhau**

Ghi rõ nguyên tắc này trong định nghĩa agent.

### 3-4. QA chạy ngay sau khi từng module hoàn thành, không phải sau khi build

Nếu orchestrator chỉ đặt QA ở "Phase 4: sau khi hoàn thiện toàn bộ":
- Bug tích tụ làm tăng chi phí sửa
- Sai lệch điểm biên ban đầu lan sang các module sau

**Mẫu khuyến nghị**: ngay khi mỗi API backend hoàn thành, thực hiện kiểm định đối chiếu chéo giữa API đó và hook tương ứng (incremental QA).

---

## 4. Template checklist kiểm định

Checklist kiểm định tính nhất quán tích hợp dành cho web app, đưa vào định nghĩa agent QA.

```markdown
### Kiểm định tính nhất quán tích hợp (web app)

#### Kết nối API ↔ Frontend
- [ ] Shape response của mọi API route khớp với type generic của hook tương ứng
- [ ] Response được wrap ({ items: [...] }) có được hook unwrap không
- [ ] Chuyển đổi snake_case ↔ camelCase được áp dụng nhất quán
- [ ] Frontend phân biệt được shape của response ngay lập tức (202) và kết quả cuối cùng
- [ ] Mọi API endpoint đều có hook frontend tương ứng và thực sự được gọi

#### Tính nhất quán routing
- [ ] Mọi giá trị href/router.push trong code khớp với đường dẫn file page thực tế
- [ ] Kiểm định đường dẫn có tính đến việc route group ((group)) bị loại khỏi URL
- [ ] Dynamic segment ([id]) được điền đúng tham số

#### Tính nhất quán state machine
- [ ] Mọi chuyển trạng thái đã định nghĩa đều được thực thi trong code (không có chuyển trạng thái chết)
- [ ] Mọi lệnh cập nhật status trong code đều được định nghĩa trong map chuyển trạng thái (không có chuyển trạng thái trái phép)
- [ ] Không thiếu chuyển từ trạng thái trung gian sang trạng thái cuối
- [ ] Nhánh dựa trên trạng thái ở frontend (if status === "X") có giá trị X thực sự đạt được

#### Tính nhất quán luồng dữ liệu
- [ ] Map giữa tên field schema DB và tên field response API nhất quán
- [ ] Tên field trong định nghĩa type frontend khớp với response API
- [ ] Xử lý null/undefined cho field optional nhất quán ở cả hai bên
```

---

## 5. Template định nghĩa agent QA

Các section cốt lõi cần đưa vào agent QA của build harness.

```markdown
---
name: qa-inspector
description: "Chuyên gia kiểm định QA. Kiểm định việc tuân thủ spec, tính nhất quán tích hợp, chất lượng thiết kế."
---

# QA Inspector

## Vai trò cốt lõi
Kiểm định chất lượng triển khai so với spec và **tính nhất quán tích hợp giữa các module**.

## Thứ tự ưu tiên kiểm định

1. **Tính nhất quán tích hợp** (cao nhất) — sai lệch điểm biên là nguyên nhân chính gây lỗi runtime
2. **Tuân thủ spec chức năng** — API/state machine/mô hình dữ liệu
3. **Chất lượng thiết kế** — màu sắc/typography/responsive
4. **Chất lượng code** — code không dùng, quy ước đặt tên

## Phương pháp kiểm định: "đọc cả hai bên đồng thời"

Kiểm định điểm biên bắt buộc phải **mở đồng thời cả hai bên code** để so sánh:

| Đối tượng kiểm định | Bên trái (producer) | Bên phải (consumer) |
|----------|-------------|---------------|
| Shape API response | NextResponse.json() trong route.ts | fetchJson<T> trong hooks/ |
| Routing | đường dẫn file page trong src/app/ | giá trị href, router.push |
| Chuyển trạng thái | map STATE_TRANSITIONS | code .update({ status }) |
| DB → API → UI | tên cột bảng | field response API → định nghĩa type |

## Giao thức giao tiếp đội

- Khi phát hiện, ngay lập tức yêu cầu agent liên quan sửa cụ thể (file:line + cách sửa)
- Vấn đề ở điểm biên phải thông báo cho **cả hai** agent liên quan
- Gửi leader: báo cáo kiểm định (phân loại rõ pass/fail/chưa kiểm định)
```

---

## Case thực tế: bug phát hiện tại SatangSlide

Toàn bộ nội dung của hướng dẫn này được rút ra từ các bug thực tế dưới đây:

| Bug | Điểm biên | Nguyên nhân |
|------|--------|------|
| `projects?.filter is not a function` | API→hook | API trả `{projects:[]}`, hook kỳ vọng array |
| Mọi link dashboard 404 | đường dẫn file→href | thiếu tiền tố `/dashboard/` |
| Ảnh theme không hiện | API→component | `thumbnailUrl` vs `thumbnail_url` |
| Chọn theme không lưu | API→hook | API select-theme tồn tại nhưng không có hook |
| Trang tạo treo vô hạn | chuyển trạng thái→code | thiếu code chuyển sang `template_approved` |
| Crash `data.failedIndices` | response ngay→frontend | truy cập kết quả background trong response ngay lập tức |
| Xem slide sau khi hoàn thành 404 | đường dẫn file→href | `/projects/` → `/dashboard/projects/` |
