# Toolkit — Từ Evidence Đến Build Slice

Dùng sau khi nhóm đã có evidence. Mục tiêu là chốt một build slice đủ nhỏ cho Day 06.

## 1. Gom evidence thành cụm

Gom theo **workflow/pain**, không gom theo tên feature.

- Cụm 1: "Ra lệnh hành động nhưng nhận về bức tường chữ" — User nhập lệnh chuyển tiền (Action Intent) nhưng hệ thống chỉ trả về văn bản hướng dẫn tĩnh (Static QA), bắt user tự nhớ data, tự thoát chat ra ngoài app làm lại.

- Cụm 2: "AI đoán bừa ý định khi câu lệnh mơ hồ" — User nhập lệnh có danh xưng chung chung ("chuyển tiền cho mẹ"), AI tự ý phân loại nhầm sang luồng ghi chép chi tiêu (Log Intent) thay vì luồng giao dịch, hoàn toàn không có cơ chế hỏi lại.

- Cụm 3: "Rào cản nhận thức quá lớn cho người già" — Người lớn tuổi mắt kém, sợ giao diện nhiều nút bấm phức tạp, coi trợ lý giọng nói là "cứu cánh" nhưng lại bị chặn lại bởi một đống chữ hướng dẫn.
## 2. Viết insight

Form:

```text
User là người dùng bận rộn và người già kém công nghệ không chỉ cần một chatbot biết đọc hiểu câu chữ (NLU đơn thuần).
Họ thật ra cần một trải nghiệm thực thi liền mạch (Frictionless Action) và sự tối giản tối đa về mặt thao tác,
vì bằng chứng thực tế (Self-use & User Observation) cho thấy việc AI trả về text hướng dẫn dài dòng hoặc đoán bừa ý định sang luồng ghi chép chi tiêu đang trực tiếp làm gãy luồng giao dịch, ép người dùng phải gánh thêm gánh nặng nhận thức và làm tăng tỷ lệ bỏ cuộc (Drop-off).
```


## 3. Viết opportunity

Form:

```text
Cơ hội là dùng AI để tăng cường (Augment) một hành động hẹp: Tự động hóa việc "dọn đường" giao dịch thông qua ReAct Agent và Function Calling để bóc tách thực thể số điện thoại/danh xưng, sau đó khởi chạy Deep-link điều hướng ngầm,
giúp user cắt giảm ít nhất 4 thao tác bấm tay phức tạp, mở thẳng giao diện chuyển tiền đã điền sẵn thông tin người nhận,
trong khi vẫn kiểm soát rủi ro tài chính (Failure/Risk) bằng cách để con người giữ quyền quyết định cuối cùng (nhập số tiền, xác thực bảo mật tài khoản).
```

## 4. Chọn build slice

Build slice tốt phải qua 5 câu hỏi:

| Câu hỏi | Đạt khi |Trạng thái|
|---|---|---|
| User cụ thể chưa? | Nói được ai dùng, trong bối cảnh nào. |ĐẠT: Người dùng gia đình, người già kém công nghệ, người bận rộn cần chuyển tiền nhanh thông qua câu lệnh tự nhiên.|
| Task đủ hẹp chưa? | Demo được trong 3-5 phút. |ĐẠT: Chỉ xử lý duy nhất một luồng: Nhận câu lệnh -> Trích xuất thông tin người nhận -> Bật giao diện nháp chuyển tiền.|
| AI decision rõ chưa? | AI gợi ý/tự làm một việc cụ thể. |ĐẠT: AI quyết định bóc tách số điện thoại (Regex) và chọn gọi Tool điều hướng (trigger_app_deep_link) hoặc gọi nút bấm gợi ý (Low-confidence).|
| Failure path rõ chưa? | Có một case AI không chắc hoặc sai để test. |ĐẠT: Case user nhập "chuyển tiền cho mẹ" (thiếu số điện thoại) hoặc nhập sai số, hệ thống phải kích hoạt nút bấm cứu trợ thay vì đoán bừa.|ĐẠT: Đã có ảnh chụp thực tế Moni chạy sai luồng và quan sát hành vi người già.|
| Có evidence không? | Có bằng chứng từ self-use/review/user/competitor. |

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?

| Tình huống | Quyết định |
|---|---|
| Evidence yếu, user mơ hồ | Dừng build sâu; quay lại research 20 phút. |
| Ý tưởng quá rộng | Giữ domain, cắt xuống một flow. |
| AI không cần thiết | Dùng rule/manual prototype; ghi rõ vì sao không dùng AI sâu. |
| Rủi ro cao | Chọn augmentation hoặc conditional automation. |
| Không demo được trong 1 ngày | Đưa phần lớn vào backlog, giữ một path nhỏ. |
- **Tình huống của nhóm**: Ý tưởng ban đầu của Moni là trợ lý tài chính rất rộng (phân tích chi tiêu, quản lý tài sản, hỏi đáp...). Luồng tài chính chuyển tiền lại có rủi ro cao.

- **Quyết định:** Giữ domain, cắt mạnh scope xuống một flow hẹp (Giảm scope) kết hợp thiết kế AI tăng cường (Augmentation). Loại bỏ hoàn toàn các tính năng phân tích chi tiêu vĩ mô trong ngày demo, chỉ tập trung xử lý luồng Intent-to-Action thông qua Deep-link để demo trọn vẹn 4 paths trong vòng 1 ngày.

## 6. Câu chốt cuối

Điền câu này trước khi rời lớp:

```text
Dựa trên bằng chứng Moni bị gãy trải nghiệm khi trả về text hướng dẫn hoặc nhận diện sai câu lệnh "chuyển tiền cho mẹ" sang luồng ghi chép chi tiêu,
nhóm sẽ build prototype slice: Luồng xử lý câu lệnh chuyển tiền thông minh tích hợp Function Calling và Deep-link Handoff,
cho người dùng bận rộn và người cao tuổi kém công nghệ,
để giải quyết pain: Người dùng bị kẹt, phải tự đọc chữ, tự nhớ số điện thoại và tự thoát chat bấm tay thủ công ngoài app,
bằng cách AI augment task: Tự động trích xuất thông tin người nhận để khởi tạo sẵn giao diện nháp giao dịch điền sẵn dữ liệu,
và sẽ test failure path khi user đưa vào câu lệnh mơ hồ thiếu số điện thoại ("chuyển tiền cho mẹ"), AI phải hiển thị danh sách nút bấm gợi ý (Low-confidence path) hoặc nút sửa sai trực quan (Failure recovery path) thay vì tự đoán bừa.
```

## 7. Backlog

Những thứ **không build trong Day 06**:

- Tính năng đọc và phân tích biểu đồ tổng chi tiêu hàng tháng (Dashboard).

- Tính năng tự động quét danh bạ thiết bị để đồng bộ hóa nâng cao.

- Hệ thống xác thực sinh trắc học (FaceID/Vân tay) thực tế bằng code (phần này sẽ dùng màn hình giả lập/mockup).

- Hệ thống kết nối trực tiếp với core banking/API chuyển mạch ngân hàng thật.

