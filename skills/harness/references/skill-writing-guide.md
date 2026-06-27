# Hướng dẫn viết Skill

Hướng dẫn viết chi tiết để nâng cao chất lượng skill được sinh ra từ harness. Là reference bổ trợ cho Phase 4 của SKILL.md.

---

## Mục lục

1. [Mẫu viết Description](#1-mẫu-viết-description)
2. [Phong cách viết phần thân](#2-phong-cách-viết-phần-thân)
3. [Mẫu định nghĩa định dạng output](#3-mẫu-định-nghĩa-định-dạng-output)
4. [Mẫu viết ví dụ](#4-mẫu-viết-ví-dụ)
5. [Mẫu Progressive Disclosure](#5-mẫu-progressive-disclosure)
6. [Tiêu chí quyết định bundling script](#6-tiêu-chí-quyết-định-bundling-script)
7. [Chuẩn data schema](#7-chuẩn-data-schema)
8. [Những thứ không đưa vào skill](#8-những-thứ-không-đưa-vào-skill)
9. [Thiết kế tái sử dụng skill](#9-thiết-kế-tái-sử-dụng-skill)

---

## 1. Mẫu viết Description

Description là cơ chế trigger duy nhất của skill. Claude chỉ nhìn name + description trong danh sách `available_skills` để quyết định có dùng skill hay không.

### Hiểu cơ chế trigger

Claude có xu hướng không gọi skill cho công việc đơn giản mà nó có thể tự xử lý bằng công cụ cơ bản. Yêu cầu đơn giản như "đọc PDF này giúp tôi" có thể không trigger dù description hoàn hảo. Công việc càng phức tạp, nhiều bước, chuyên biệt thì xác suất trigger skill càng cao.

### Nguyên tắc viết

1. Mô tả đầy đủ cả **việc skill làm** + **tình huống trigger cụ thể**
2. Ghi rõ điều kiện biên để phân biệt với các trường hợp tương tự nhưng không nên trigger
3. Viết hơi "pushy" — để bù lại xu hướng đánh giá trigger bảo thủ của Claude

### Ví dụ tốt

```yaml
description: "Thực hiện mọi công việc PDF: đọc file PDF, trích xuất văn bản/bảng,
  hợp nhất, tách, xoay, đóng/mở watermark, mã hóa/giải mã, OCR. Khi nhắc đến
  file .pdf hoặc yêu cầu sản phẩm PDF, phải dùng skill này. Đặc biệt hữu ích
  khi cần chuyển đổi/biên tập/phân tích, không chỉ đơn thuần 'đọc' PDF."
```

```yaml
description: "Mọi công việc spreadsheet bao gồm thêm cột, tính công thức, định
  dạng, biểu đồ, làm sạch dữ liệu cho file excel/CSV/TSV. Khi người dùng nhắc
  đến file spreadsheet — dù chỉ nói thoáng qua ('cái xlsx trong thư mục
  download') — phải dùng skill này."
```

### Ví dụ tồi

- `"Skill xử lý dữ liệu"` — quá mơ hồ, không rõ file/công việc nào
- `"Công việc liên quan PDF"` — không liệt kê hành động cụ thể, không mô tả tình huống trigger

---

## 2. Phong cách viết phần thân

### Nguyên tắc Why-First

LLM hiểu lý do thì sẽ phán đoán đúng cả trong trường hợp biên. Truyền đạt ngữ cảnh hiệu quả hơn quy tắc áp đặt.

**Ví dụ tồi:**
```markdown
ALWAYS use pdfplumber for table extraction. NEVER use PyPDF2 for tables.
```

**Ví dụ tốt:**
```markdown
Dùng pdfplumber để trích xuất bảng. PyPDF2 chuyên về trích xuất văn bản nên
không giữ được cấu trúc hàng/cột của bảng. pdfplumber nhận diện ranh giới
cell và trả về dữ liệu có cấu trúc.
```

### Nguyên tắc tổng quát hóa

Khi phát hiện vấn đề từ phản hồi hoặc kết quả kiểm thử, hãy **tổng quát hóa ở mức nguyên lý** thay vì sửa hẹp chỉ đúng với một ví dụ cụ thể.

**Sửa overfitting:**
```markdown
Nếu có cột "Doanh thu Q4" thì chuyển cột đó thành số.
```

**Sửa tổng quát hóa:**
```markdown
Nếu tên cột có từ khóa ngụ ý số liệu như "doanh thu", "số tiền", "số lượng",
hãy chuyển cột đó thành kiểu số. Nếu chuyển đổi thất bại, giữ giá trị gốc.
```

### Tông ra lệnh

Dùng "thực hiện...", "phải..." thay vì "có thể...", "sẽ...". Skill là một bản chỉ thị.

### Tiết kiệm ngữ cảnh

Cửa sổ ngữ cảnh là tài sản chung. Tự hỏi mỗi câu có đáng với chi phí token không:
- "Claude đã biết điều này chưa?" → xóa
- "Không có giải thích này Claude có sai không?" → giữ
- "Một ví dụ cụ thể có hiệu quả hơn giải thích dài không?" → thay bằng ví dụ

---

## 3. Mẫu định nghĩa định dạng output

Dùng khi định dạng sản phẩm là quan trọng:

```markdown
## Cấu trúc báo cáo
Tuân theo chính xác template sau:

# [Tiêu đề]
## Tóm tắt
## Phát hiện chính
## Khuyến nghị
```

Định nghĩa định dạng nên ngắn gọn, hiệu quả hơn khi có kèm ví dụ thực tế.

---

## 4. Mẫu viết ví dụ

Ví dụ hiệu quả hơn giải thích dài:

```markdown
## Định dạng commit message

**Ví dụ 1:**
Input: thêm xác thực người dùng dựa trên JWT token
Output: feat(auth): JWT 기반 인증 구현

**Ví dụ 2:**
Input: sửa lỗi nút hiện mật khẩu không hoạt động ở trang đăng nhập
Output: fix(login): sửa nút toggle hiện mật khẩu
```

---

## 5. Mẫu Progressive Disclosure

### Mẫu 1: Tách theo lĩnh vực

```
bigquery-skill/
├── SKILL.md (tổng quan + hướng dẫn chọn lĩnh vực)
└── references/
    ├── finance.md (doanh thu, chỉ số billing)
    ├── sales.md (cơ hội, pipeline)
    └── product.md (sử dụng API, tính năng)
```

Khi người dùng hỏi về doanh thu, chỉ nạp finance.md.

### Mẫu 2: Chi tiết có điều kiện

```markdown
# Xử lý DOCX

## Tạo văn bản
Tạo văn bản mới bằng docx-js. → xem [DOCX-JS.md](references/docx-js.md).

## Sửa văn bản
Sửa đơn giản thì sửa trực tiếp XML.
**Nếu cần theo dõi thay đổi (track changes)**: xem [REDLINING.md](references/redlining.md)
```

### Mẫu 3: Cấu trúc file reference lớn

File reference từ 300 dòng trở lên cần có mục lục ở đầu:

```markdown
# API Reference

## Mục lục
1. [Xác thực](#xác-thực)
2. [Danh sách endpoint](#danh-sách-endpoint)
3. [Mã lỗi](#mã-lỗi)
4. [Rate limit](#rate-limit)

---

## Xác thực
...
```

---

## 6. Tiêu chí quyết định bundling script

Quan sát transcript của agent trong quá trình kiểm thử. Nếu thấy các mẫu sau, đó là đối tượng cần bundling:

| Tín hiệu | Hành động |
|------|------|
| 3/3 lần test sinh cùng một helper script | Bundling vào `scripts/` |
| Mỗi lần đều chạy lại pip install/npm install giống nhau | Ghi rõ bước cài dependency vào skill |
| Lặp lại cùng một cách tiếp cận nhiều bước | Ghi vào phần thân skill thành quy trình chuẩn |
| Mỗi lần gặp lỗi tương tự rồi áp dụng cùng cách lách | Ghi vào skill vấn đề đã biết và cách giải quyết |

Script đã bundling phải luôn qua kiểm thử thực thi.

---

## 7. Chuẩn data schema

Dùng schema chuẩn để đảm bảo nhất quán khi trao đổi dữ liệu giữa các skill. Có thể dùng cho kiểm thử/đánh giá skill được sinh từ harness.

### eval_metadata.json

Metadata của từng test case:

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "Prompt công việc của người dùng",
  "assertions": [
    "Sản phẩm có chứa X",
    "File được tạo theo định dạng Y"
  ]
}
```

### grading.json

Kết quả chấm điểm dựa trên assertion:

```json
{
  "expectations": [
    {
      "text": "Sản phẩm có chứa 'Seoul'",
      "passed": true,
      "evidence": "Xác nhận 'trích xuất dữ liệu khu vực Seoul' ở bước thứ 3"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  }
}
```

**Lưu ý tên field:** dùng chính xác `text`, `passed`, `evidence` (cấm biến thể như `name`/`met`/`details`).

### timing.json

Đo thời gian thực thi/token:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

Lưu ngay `total_tokens` và `duration_ms` từ thông báo hoàn thành của subagent. Dữ liệu này chỉ truy cập được tại thời điểm thông báo, không thể khôi phục sau đó.

---

## 8. Những thứ không đưa vào skill

- Tài liệu phụ trợ như README.md, CHANGELOG.md, INSTALLATION_GUIDE.md
- Thông tin meta về quá trình tạo skill (kết quả test, lịch sử lặp lại)
- Hướng dẫn dành cho người dùng (skill là chỉ thị cho AI agent)
- Tri thức tổng quát mà Claude đã biết sẵn

---

## 9. Thiết kế tái sử dụng skill

Trước khi tạo skill mới, kiểm tra trùng lặp với skill hiện có. Khi xây dựng harness lặp đi lặp lại, các skill có chức năng chồng lấp dễ tích tụ dưới tên khác nhau.

| Tình huống | Hành động |
|------|------|
| Skill hiện có đã hoàn toàn bao quát chức năng mới | Cấm tạo mới — liên kết skill hiện có với agent |
| Skill hiện có bao quát một phần và có thể tổng quát hóa | Tổng quát hóa skill hiện có để mở rộng |
| Phần bao quát chỉ là trùng hợp do đặc thù lĩnh vực | Tiến hành tạo mới — giữ là skill riêng biệt |
| Phạm vi chức năng hoàn toàn khác | Tiến hành tạo mới |

**Nguyên tắc:** một skill tập trung vào một vai trò duy nhất sẽ có khả năng tái sử dụng cao hơn và giảm trùng lặp. Nếu có 2 vai trò trở lên, hãy xem xét tách trước.

### Tổng quát hóa đến đâu

Tổng quát hóa có thể vô hạn, nên dừng ở **phạm vi trách nhiệm dự kiến**. Giữ lại đặc thù lĩnh vực có chủ đích, chỉ loại bỏ phụ thuộc ngẫu nhiên.

Ví dụ: skill "PDF đánh giá rủi ro fintech"

| Bước | Kết quả |
|------|------|
| Loại bỏ phụ thuộc fintech | "PDF kết quả đánh giá" — nếu phạm vi trách nhiệm là báo cáo đánh giá thì dừng ở đây |
| Loại bỏ phụ thuộc đánh giá | "Định dạng PDF" — nếu đã tồn tại, đừng tạo skill riêng mà tái sử dụng |

Nếu phạm vi trách nhiệm là đặc thù có chủ đích "đánh giá rủi ro fintech", thì không tổng quát hóa mà giữ là skill riêng biệt.

Hành vi của agent phụ thuộc vào skill đó có thể thay đổi. Kiểm tra phụ thuộc trước khi mở rộng, và phản ánh phạm vi sử dụng mở rộng vào description.
