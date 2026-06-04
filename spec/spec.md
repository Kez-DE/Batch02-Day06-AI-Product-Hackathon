# SPEC sản phẩm

Ở Day 5, mỗi nhóm đã viết một bản SPEC nhẹ. Đến Day 6, nhóm hoàn thiện bản này cho đủ để bắt tay vào build và mang đi demo — vẫn ngắn gọn, nhưng đủ để bảo vệ được những quyết định sản phẩm của mình.

Hãy hình dung SPEC như một lập luận, chứ không phải một danh sách tính năng. Nó cần trả lời rõ bốn câu hỏi: sản phẩm giải vấn đề gì và cho ai, AI tham gia quyết định điều gì, chuyện gì xảy ra khi AI trả lời sai, và những nhận định của nhóm dựa trên bằng chứng nào.

Viết SPEC vào `spec/spec.md`, có thể kèm slide demo (`spec/demo-slides.pdf`).

---

## 1. Bằng chứng

- Trường hợp lệnh đầy đủ: Khi nhập câu lệnh hành động cụ thể “Tôi muốn chuyển tiền tới momo 0xxxx”, Moni bị gãy ở tầng thực thi. Hệ thống chỉ trả về một "bức tường chữ" hướng dẫn các bước thực hiện thủ công (Bước 1: Chọn Chuyển tiền, Bước 2: Nhập số điện thoại...). Người dùng bị kẹt, phải tự đọc chữ, tự nhớ số điện thoại, và tự thoát khung chat ra ngoài màn hình chính để thao tác lại từ đầu.
![moni_scr.jpg](moni_scr.jpg)
- Trường hợp lệnh mơ hồ: Khi nhập câu lệnh mang tính gia đình “chuyển tiền cho mẹ”, Moni rơi vào trạng thái nhận diện sai hoàn toàn ý định (Misclassification). Thay vì kích hoạt luồng giao dịch, AI tự ý đoán bừa sang luồng Ghi chép chi tiêu và hỏi: “Vui lòng cho Moni biết số tiền bạn đã chuyển để mình ghi chú lại nhé!”.
![moni_scr_2.jpg](moni_scr_2.jpg)
## 2. Lát cắt để build
Cấu trúc lát cắt: Cho người dùng bận rộn và người già mắt kém thực hiện tác vụ ra lệnh chuyển tiền bằng một câu thoại tự nhiên, AI sẽ quyết định bóc tách thực thể số điện thoại/danh xưng (Entity Extraction) để gọi công cụ điều hướng ngầm (trigger_app_deep_link), trả về kết quả là Màn hình nháp giao dịch của Native App được điền sẵn 100% thông tin người nhận, chỉ đứng đợi người dùng nhập số tiền.
## 3. AI Product Canvas

Canvas là một trang giúp sản phẩm không trôi ngược về "một demo cho vui". Nhóm trả lời lần lượt bốn ô:

| Ô | Câu hỏi cần trả lời                                                                                                                                                                                                                                                                                                                                                                                                                     |
|---|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Value** — Giá trị | **Đối tượng**: Người dùng bận rộn và người cao tuổi mắt kém.<br>**Nỗi đau**: Bị kẹt trong "bức tường chữ" hướng dẫn, ngại nhớ số tài khoản và mò mẫm giao diện nhiều bước.<br>**AI giải quyết:** Chuyển dịch từ Hỏi-đáp thông tin (Static QA) sang Thực thi tác vụ (Action-driven), cắt giảm 4 thao tác bấm tay bằng cơ chế tự điều hướng thông minh.                                                                                   |
| **Trust** — Niềm tin | **Cách nhận biết lỗi:** Người dùng nhìn thấy tên người nhận hiển thị to rõ trên giao diện nháp bị sai, hoặc AI hiện cảnh báo số điện thoại chưa kích hoạt ví.<br>**Cơ chế sửa sai:** User có thể nhập lại ngay trên màn hình                                                                                                                                                                                                            |
| **Feasibility** — Tính khả thi | **Chi phí & Độ trễ:** Ứng dụng chạy mô hình ReAct hẹp bóc tách Regex ngay tại Local, chi phí gọi API tối thiểu, độ trễ xử lý dữ liệu dưới 1 giây (đảm bảo trải nghiệm tức thì).<br>**Dữ liệu đầu vào:**<br> - Dữ liệu người dùng giả lập <br>- Dữ liệu danh bạ người dùng giả lập<br>**Ngưỡng dừng lại:** Nếu API kiểm tra số tài khoản của MoMo phản hồi chậm > 3 giây, hệ thống tự động ngắt và chuyển về màn hình chat thông thường. |
| **Tín hiệu học** | Khi người dùng đính chính lại thông tin bằng cách chọn các nút gợi ý, hành vi này được ghi nhận trực tiếp vào Local Log/Cache của phiên làm việc. Đây là tín hiệu Context-learning giúp AI tự động ghi nhớ mối quan hệ Alias (ví dụ: gán cứng câu lệnh "cho mẹ" vào SĐT vừa chọn) cho các lần giao dịch tiếp theo mà không cần training lại core model.|

## 4. Tăng năng lực hay tự động hóa
- Quyết định sản phẩm: Nhóm lựa chọn mức độ AI Tăng cường (Augmentation).

- Lý do: Chuyển tiền là tác vụ liên quan đến tài chính, có rủi ro rất cao và hậu quả nặng nề nếu xảy ra sai sót. Vì vậy, AI chỉ được phép tự động hóa ở phần "dọn đường hành động" (bóc tách dữ liệu, đối chiếu danh tính và khởi tạo màn hình nháp).

- Quyền quyết định của con người: Con người (User) bắt buộc phải giữ vai trò là người duyệt cuối (Decider): đối chiếu lại tên người nhận và thực hiện bước xác thực bảo mật (FaceID/Mật khẩu) để tiền đi ra khỏi tài khoản.
## 5. Bốn đường đi của trải nghiệm

Một tính năng AI không chỉ có đường thuận. Nhóm cần thiết kế cho cả bốn tình huống mà người dùng có thể gặp:

| Đường đi | Câu hỏi | Ví dụ cách xử lý |
|----------|---------|------------------|
| **Đường thuận** | AI đúng và tự tin — người dùng thấy gì? |  User nhập lệnh đầy đủ: "Chuyển tiền tới momo 0912345xxx". AI bóc đúng số, gọi API thấy hợp lệ, không hiện text hướng dẫn mà tự động gọi tool điều hướng mở thẳng màn hình chuyển tiền đã điền sẵn thông tin. |
| **Khi AI không chắc** | AI lưỡng lự — có hỏi lại không? | User nhập lệnh mơ hồ: "Chuyển tiền cho mẹ". AI không chắc "mẹ" là ai. Hệ thống không được đoán bừa sang luồng ghi chép, mà phải hiển thị 2-3 nút bấm động chứa danh sách số điện thoại có nhãn "Mẹ" hoặc thường liên lạc gần đây để user chạm chọn. |
| **Khi AI sai** | Kết quả sai — người dùng gỡ ra thế nào? | Khi số điện thoại user nhập chưa đăng ký MoMo hoặc hệ thống lỗi. App hiển thị một thông báo lỗi trực quan rõ ràng|
| **Khi người dùng sửa** | Người dùng chỉnh lại — dữ liệu đi về đâu? | Khi user bấm chọn một nút gợi ý ở luồng Low-confidence, hành vi đính chính này được lưu lại vào Local Log/Cache của phiên làm việc|

## 6. Những kiểu lỗi đáng lo nhất
Nếu user nhập một câu lệnh chuyển tiền có chứa số điện thoại lỗi hoặc chưa kích hoạt ví,
AI có thể bóc tách thực thể sai hoặc hệ thống gặp lỗi logic đứng im,
hậu quả là user bị treo màn hình hoặc giao dịch bị chuyển sai đối tượng gây mất an toàn tài chính.
Prototype sẽ xử lý bằng cách tích hợp hộp thoại cảnh báo (Modal Fallback) hiển thị to rõ thông báo lỗi và cung cấp ngay nút bấm quay xe [Hủy bỏ giao dịch] để đưa user về vùng an toàn.

## 7. Kế hoạch kiểm thử và bằng chứng demo
Đầu vào đường thuận (Happy Path Test): Câu lệnh chứa số điện thoại rõ ràng: "Tôi muốn chuyển tiền tới momo 0936768999". Kết quả mong đợi: Figma tự động nhảy sang màn hình giao dịch điền sẵn tên "Mỹ Gia Hiếu".

Đầu vào gây nhiễu (Low-confidence Test): Câu lệnh chỉ chứa danh xưng: "Chuyển tiền cho mẹ". Kết quả mong đợi: Khung chat hiện 2 nút bấm phân biệt rõ ràng nhãn "Mẹ" (Phạm Mỹ Khánh - 0327383750) và "Mẹ vợ" (Tạ Thanh Tú - 0837307556) để test khả năng phục hồi của AI.
## 8. Phân công

| Thành viên                   | Việc phụ trách | Bằng chứng cần có trong repo |
|------------------------------|---|---|
| Lý Hải Long                  | Research / evidence | 02-group-spec/evidence-pack-template.md |
| Lý Hải Long                  | SPEC | 02-group-spec/thin-spec-template.md |
| Lý Hải Long                  | Prototype |  |
| Nguyễn Đức Khang             | Test / failure path |  |
| Lê Quốc Anh, Nguyễn Đức Mạnh | Demo script / repo |  |
