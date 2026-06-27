# Hướng dẫn kiểm thử & cải tiến lặp lại Skill

Phương pháp luận để kiểm định chất lượng và cải tiến lặp lại skill được sinh từ harness. Là reference bổ trợ cho Phase 6 của SKILL.md.

---

## Mục lục

1. [Tổng quan framework kiểm thử](#1-tổng-quan-framework-kiểm-thử)
2. [Cách viết prompt kiểm thử](#2-cách-viết-prompt-kiểm-thử)
3. [Kiểm thử thực thi: With-skill vs Baseline](#3-kiểm-thử-thực-thi-with-skill-vs-baseline)
4. [Đánh giá định lượng: chấm điểm dựa trên Assertion](#4-đánh-giá-định-lượng-chấm-điểm-dựa-trên-assertion)
5. [Sử dụng agent chuyên biệt](#5-sử-dụng-agent-chuyên-biệt)
6. [Vòng lặp cải tiến lặp lại](#6-vòng-lặp-cải-tiến-lặp-lại)
7. [Kiểm định trigger của Description](#7-kiểm-định-trigger-của-description)
8. [Cấu trúc workspace](#8-cấu-trúc-workspace)

---

## 1. Tổng quan framework kiểm thử

Kiểm định chất lượng skill là tổ hợp giữa **đánh giá định tính** và **đánh giá định lượng**.

| Loại đánh giá | Phương pháp | Skill phù hợp |
|----------|------|-----------|
| **Định tính** | Người dùng tự review sản phẩm | Chất lượng chủ quan như văn phong, thiết kế, sản phẩm sáng tạo |
| **Định lượng** | Chấm điểm tự động dựa trên assertion | Có thể kiểm định khách quan như tạo file, trích xuất dữ liệu, sinh code |

Vòng lặp cốt lõi: **viết → chạy test → đánh giá → cải tiến → test lại**

---

## 2. Cách viết prompt kiểm thử

### Nguyên tắc

Prompt kiểm thử phải là **câu cụ thể, tự nhiên giống người dùng thực sự sẽ nhập**. Prompt trừu tượng hoặc giả tạo có giá trị kiểm thử thấp.

### Ví dụ tồi

```
"Xử lý file PDF"
"Trích xuất dữ liệu"
"Tạo biểu đồ"
```

### Ví dụ tốt

```
"Trong file 'Q4_doanh_thu_final_v2.xlsx' ở thư mục download, dùng cột C
(doanh thu) và cột D (chi phí) để thêm cột tỷ suất lợi nhuận (%). Sau đó
sắp xếp giảm dần theo tỷ suất lợi nhuận."
```

```
"Trích xuất bảng ở trang 3 của PDF này và chuyển sang CSV. Header của bảng
có 2 dòng — dòng đầu là category, dòng hai mới là tên cột thực sự."
```

### Đa dạng hóa prompt

- Trộn tông **trang trọng / thân mật**
- Trộn ý định **rõ ràng / ngụ ý** (nói trực tiếp định dạng file vs phải suy luận từ ngữ cảnh)
- Trộn công việc **đơn giản / phức tạp**
- Một số có viết tắt, lỗi đánh máy, cách diễn đạt thân mật

### Độ phủ

Bắt đầu với 2~3 prompt, nhưng thiết kế để phủ:
- 1 use case cốt lõi
- 1 edge case
- (tùy chọn) 1 công việc phức hợp

---

## 3. Kiểm thử thực thi: With-skill vs Baseline

### 3-1. Cấu trúc thực thi so sánh

Với mỗi prompt kiểm thử, spawn **đồng thời** 2 subagent:

**Thực thi With-skill:**
```
Prompt: "{prompt kiểm thử}"
Đường dẫn skill: {đường dẫn skill}
Đường dẫn output: _workspace/iteration-N/eval-{id}/with_skill/outputs/
```

**Thực thi Baseline:**
```
Prompt: "{prompt kiểm thử}"  (giống nhau)
Skill: không có
Đường dẫn output: _workspace/iteration-N/eval-{id}/without_skill/outputs/
```

### 3-2. Chọn Baseline

| Tình huống | Baseline |
|------|----------|
| Tạo skill mới | Chạy cùng prompt nhưng không có skill |
| Cải thiện skill hiện có | Phiên bản skill trước khi sửa (giữ lại snapshot) |

### 3-3. Ghi lại dữ liệu timing

Lưu **ngay** `total_tokens` và `duration_ms` từ thông báo hoàn thành của subagent. Dữ liệu này chỉ truy cập được tại thời điểm thông báo, không thể khôi phục sau đó.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

---

## 4. Đánh giá định lượng: chấm điểm dựa trên Assertion

### 4-1. Viết Assertion

Nếu sản phẩm có thể kiểm định khách quan, định nghĩa assertion để chấm điểm tự động.

**Assertion tốt:**
- Có thể xác định đúng/sai một cách khách quan
- Tên mang tính mô tả, chỉ nhìn kết quả cũng rõ đang kiểm tra gì
- Kiểm định giá trị cốt lõi của skill

**Assertion tồi:**
- Luôn pass dù có skill hay không (ví dụ: "có tồn tại output")
- Cần phán đoán chủ quan (ví dụ: "viết tốt")

### 4-2. Kiểm định bằng code

Nếu assertion có thể kiểm định bằng code, viết thành script. Nhanh hơn, đáng tin hơn so với kiểm tra bằng mắt, và tái sử dụng được ở mỗi iteration.

### 4-3. Cẩn trọng với Non-discriminating assertion

Assertion "pass 100% ở cả hai cấu hình" không đo được giá trị khác biệt của skill. Khi phát hiện assertion như vậy, loại bỏ hoặc thay bằng assertion thử thách hơn.

### 4-4. Schema kết quả chấm điểm

```json
{
  "expectations": [
    {
      "text": "Đã thêm cột tỷ suất lợi nhuận",
      "passed": true,
      "evidence": "Xác nhận cột 'profit_margin_pct' ở cột E"
    },
    {
      "text": "Sắp xếp giảm dần theo tỷ suất lợi nhuận",
      "passed": false,
      "evidence": "Vẫn giữ thứ tự gốc, không sắp xếp"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.50
  }
}
```

---

## 5. Sử dụng agent chuyên biệt

Dùng agent đảm nhiệm vai trò chuyên biệt trong quá trình kiểm thử/đánh giá sẽ nâng cao chất lượng.

### 5-1. Grader (người chấm điểm)

Chấm điểm dựa trên assertion, trích xuất các claim có thể kiểm định từ sản phẩm để đối chiếu chéo.

**Vai trò:**
- Phán định pass/fail cho từng assertion + đưa bằng chứng
- Trích xuất và kiểm định các claim mang tính sự kiện từ sản phẩm
- Phản hồi về chất lượng của eval bản thân nó (đề xuất nếu assertion quá dễ hoặc mơ hồ)

### 5-2. Comparator (người so sánh blind)

Ẩn danh hóa hai sản phẩm thành A/B, phán định chất lượng mà không biết cái nào là kết quả dùng skill.

**Khi nào dùng:** khi muốn xác nhận nghiêm ngặt "phiên bản mới có thực sự tốt hơn?". Có thể bỏ qua trong cải tiến lặp lại thông thường.

**Tiêu chí phán định:**
- Nội dung: độ chính xác, độ hoàn thiện
- Cấu trúc: tổ chức, định dạng, khả năng sử dụng
- Điểm tổng hợp

### 5-3. Analyzer (người phân tích)

Phân tích pattern thống kê từ dữ liệu benchmark:
- Non-discriminating assertion (cả hai cấu hình đều pass → không có giá trị phân biệt)
- Eval có độ phân tán cao (kết quả khác nhau lớn giữa các lần chạy → không ổn định)
- Trade-off thời gian/token (skill nâng cao chất lượng nhưng cũng tăng chi phí)

---

## 6. Vòng lặp cải tiến lặp lại

### 6-1. Thu thập phản hồi

Cho người dùng xem sản phẩm và nhận phản hồi. Phản hồi trống được hiểu là "không có vấn đề".

### 6-2. Nguyên tắc cải tiến

1. **Tổng quát hóa phản hồi** — sửa hẹp chỉ đúng với ví dụ kiểm thử là overfitting. Sửa ở mức nguyên lý.
2. **Loại bỏ những gì không tạo giá trị** — đọc transcript, nếu skill đang khiến agent làm việc phi hiệu quả, xóa phần đó.
3. **Giải thích Why** — dù phản hồi của người dùng ngắn gọn, hiểu lý do nó quan trọng và phản ánh sự hiểu đó vào skill.
4. **Bundling công việc lặp lại** — nếu mọi lần kiểm thử đều sinh cùng helper script, bundling sẵn vào `scripts/`.

### 6-3. Quy trình lặp lại

```
1. Sửa skill
2. Chạy lại toàn bộ test case trong thư mục iteration-N+1/ mới
3. Trình bày kết quả cho người dùng (so sánh với iteration trước)
4. Thu thập phản hồi
5. Sửa lại → lặp lại
```

**Điều kiện kết thúc:**
- Người dùng hài lòng
- Tất cả phản hồi đều trống (mọi sản phẩm đều ổn)
- Không còn cải tiến đáng kể nào nữa

### 6-4. Mẫu nháp → review lại

Khi sửa skill, viết bản nháp rồi **đọc lại với góc nhìn mới** để cải tiến. Không cố viết hoàn hảo ngay lần đầu, hãy trải qua chu kỳ nháp-review.

---

## 7. Kiểm định trigger của Description

### 7-1. Viết truy vấn eval cho trigger

Viết 20 truy vấn eval — 10 should-trigger + 10 should-NOT-trigger.

**Tiêu chí chất lượng truy vấn:**
- Câu cụ thể, tự nhiên giống người dùng thực sự sẽ nhập
- Có chi tiết cụ thể như đường dẫn file, ngữ cảnh cá nhân, tên cột, tên công ty
- Trộn đa dạng về độ dài, tông, định dạng
- Tập trung vào **edge case** hơn là đáp án rõ ràng

**Truy vấn Should-trigger (8~10 câu):**
- Cùng ý định nhưng diễn đạt khác nhau (trang trọng/thân mật)
- Không nói rõ loại skill/file nhưng rõ ràng cần dùng
- Use case ít phổ biến
- Trường hợp cạnh tranh với skill khác nhưng skill này phải thắng

**Truy vấn Should-NOT-trigger (8~10 câu):**
- **Near-miss là cốt lõi** — truy vấn có từ khóa tương tự nhưng công cụ/skill khác phù hợp hơn
- Truy vấn rõ ràng không liên quan ("viết hàm Fibonacci") không có giá trị kiểm thử
- Lĩnh vực liền kề, diễn đạt mơ hồ, trùng từ khóa nhưng khác ngữ cảnh

### 7-2. Kiểm định xung đột với skill hiện có

Xác nhận description của skill mới không chồng lấp vùng trigger với skill hiện có:

1. Thu thập description của danh sách skill hiện có
2. Xác nhận truy vấn should-trigger của skill mới không vô tình trigger skill hiện có
3. Nếu phát hiện xung đột, ghi rõ hơn điều kiện biên trong description

### 7-3. Tự động tối ưu (tính năng nâng cao, tùy chọn)

Khi cần tối ưu description:

1. Chia 20 truy vấn eval thành Train (60%) / Test (40%)
2. Đo độ chính xác trigger với description hiện tại
3. Phân tích các case thất bại để sinh description cải tiến
4. Chọn description tốt nhất dựa trên Test set (không dựa trên Train set — tránh overfitting)
5. Lặp lại tối đa 5 lần

> Quy trình này thực hiện bằng script tự động dùng `claude -p`. Vì chi phí token cao, chỉ chạy ở bước cuối khi skill đã đủ ổn định.

---

## 8. Cấu trúc workspace

Cấu trúc thư mục để quản lý có hệ thống kết quả kiểm thử/đánh giá:

```
{skill-name}-workspace/
├── iteration-1/
│   ├── eval-descriptive-name-1/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/
│   │   │   ├── outputs/
│   │   │   ├── timing.json
│   │   │   └── grading.json
│   │   └── without_skill/
│   │       ├── outputs/
│   │       ├── timing.json
│   │       └── grading.json
│   ├── eval-descriptive-name-2/
│   │   └── ...
│   └── benchmark.json
├── iteration-2/
│   └── ...
└── evals/
    └── evals.json
```

**Quy tắc:**
- Tên thư mục eval dùng **tên mô tả**, không dùng số (ví dụ: `eval-multi-page-table-extraction`)
- Mỗi iteration được giữ trong thư mục riêng (cấm ghi đè iteration trước)
- Không xóa `_workspace/` — dùng cho kiểm định và audit trail sau này
