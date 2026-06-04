# Template — Thin SPEC Cuối Day 05

Thin SPEC không phải PRD đầy đủ. Đây là bản cam kết đủ rõ để sáng Day 06 nhóm build ngay.

## 1. Track, product/app và user

**Track:**  Personal Finance

**Product/app thật:**  Moni-MoMo

**User cụ thể:**  Người dùng bận rộn cần chuyển tiền nhanh và thế hệ cha mẹ/người lớn tuổi mắt kém, ngại thực hiện nhiều thao tác bấm tay phức tạp trên ứng dụng ngân hàng.

**Nhóm có phải user thật không? Nếu không, khác ở đâu?:** Các thành viên trẻ trong nhóm là user thật cho trường hợp "bận rộn/lười thao tác". Đối với nhóm user lớn tuổi, các thành viên không phải là user thật vì có sự khác biệt lớn về năng lực công nghệ (nhóm trẻ nhạy bén hơn, chịu được gánh nặng đọc chữ tốt hơn người già). 

## 2. Evidence summary

| Evidence                                                                                                                                                                                                    | Nguồn | User/pain nói lên điều gì?                                                                       | SPEC phải đổi gì? |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|--------------------------------------------------------------------------------------------------|---|
| Lệnh "Tôi muốn chuyển tiền tới momo 0xxxx" chỉ trả về text hướng dẫn dài dòng.| Tự trải nghiệm app (Self-use). | User bị kẹt, phải đọc wall-of-text, tự nhớ số điện thoại và tự thoát chat ra ngoài app để làm lại. | Cấm trả về text tĩnh. Đổi đầu ra thành định dạng JSON để gọi Tool điều hướng (Deep-link) thẳng vào màn hình chuyển tiền. |
| Lệnh "chuyển tiền cho mẹ" bị nhận diện sai sang luồng ghi chép chi tiêu.| Ảnh chụp thực tế màn hình chat Moni | AI tự đoán bừa ý định (Misclassification) khi câu lệnh mơ hồ, không có cơ chế hỏi lại làm user hoang mang sợ mất tiền.                | Thiết kế Low-confidence path. Bắt buộc hiển thị danh sách các nút bấm (Button gợi ý) để làm rõ danh tính người nhận. |
| Người cao tuổi không thể đọc các dòng chữ hướng dẫn nhỏ của trợ lý ảo | Quan sát/Phỏng vấn nhanh người lớn tuổi trong gia đình. | Rào cản nhận thức và thị giác quá lớn khiến họ mất niềm tin và từ bỏ sử dụng app.| Tối giản hóa giao diện. Chuyển dịch hoàn toàn sang mô hình tương tác bằng một chạm (One-tap action). |

## 3. Pain statement

```text
User là người dùng bận rộn và người cao tuổi kém công nghệ đang gặp khó ở bước thực hiện giao dịch chuyển tiền bằng câu lệnh tự nhiên,
vì hệ thống Moni hiện tại bị gãy ở tầng thực thi hành động (chỉ trả về văn bản hướng dẫn tĩnh hoặc tự ý đoán sai ý định của user sang luồng ghi chép chi tiêu khi câu lệnh mơ hồ),
dẫn tới hậu quả là người dùng bị kẹt trải nghiệm, buộc phải gánh thêm gánh nặng ghi nhớ thông tin, tự thoát khung chat để mò mẫm giao diện bấm tay lại từ đầu hoặc từ bỏ tính năng vì hoang mang.
Bằng chứng chính là ảnh chụp màn hình Moni trả lời sai hướng đi khi nhận lệnh "chuyển tiền cho mẹ" (image_f34f01.jpg) và bức tường chữ hướng dẫn ở file moni_scr.jpg.
```

## 4. Build slice

```text
Cho người dùng bận rộn và người già mắt kém đang thực hiện workflow chuyển tiền qua Moni,
prototype sẽ dùng AI để tăng cường (Augment) hành động hẹp: Tự động chạy mô hình ReAct bóc tách số điện thoại/danh xưng từ câu thoại, gọi API ngầm đối chiếu danh tính,
tạo ra giao diện nháp chuyển tiền điền sẵn thông tin người nhận thông qua việc kích hoạt Deep-link,
và xử lý luồng câu lệnh thiếu thông tin (Low-confidence) bằng cách hiển thị các nút bấm gợi ý tương tác nhanh thay vì đoán bừa.
```

## 5. Auto/Aug decision

Chọn một:

- [x] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [ ] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn:** Tác vụ chuyển tiền liên quan trực tiếp đến tài chính và có mức độ rủi ro rất cao. AI chỉ nên dừng lại ở việc chuẩn bị sẵn bản nháp giao diện (điền sẵn người nhận) để cắt giảm thao tác. Quyết định nhập số tiền và bấm nút xác nhận cuối cùng (bảo mật/FaceID) phải thuộc về con người để đảm bảo an toàn tuyệt đối. 

**Human role:** decider  

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| Happy | User nhập lệnh đầy đủ: "Chuyển tiền tới momo 0912345xxx". AI bóc đúng số, gọi API thấy hợp lệ, không hiện text hướng dẫn mà tự động gọi tool điều hướng mở thẳng màn hình chuyển tiền đã điền sẵn thông tin. |
| Low-confidence | User nhập lệnh mơ hồ: "Chuyển tiền cho mẹ". AI không chắc "mẹ" là ai. Hệ thống không được đoán bừa sang luồng ghi chép, mà phải hiển thị 2-3 nút bấm động chứa danh sách số điện thoại có nhãn "Mẹ" hoặc thường liên lạc gần đây để user chạm chọn. |
| Failure | Khi số điện thoại user nhập chưa đăng ký MoMo hoặc hệ thống lỗi. App hiển thị một thông báo lỗi trực quan rõ ràng kèm nút cứu trợ: [Nhập lại số điện thoại] hoặc [Quay lại chat] để user sửa sai ngay lập tức. |
| Correction | Khi user bấm chọn một nút gợi ý ở luồng Low-confidence, hành vi đính chính này được lưu lại vào Local Log/Cache của phiên làm việc giúp AI học ngữ cảnh (Context learning), nếu user gõ lại câu đó, hệ thống sẽ tự động map thẳng vào số điện thoại vừa sửa. |

## 7. Failure mode nguy hiểm nhất

```text
Nếu user nhập một câu lệnh chuyển tiền có chứa số điện thoại lỗi hoặc chưa kích hoạt ví,
AI có thể bóc tách thực thể sai hoặc hệ thống gặp lỗi logic đứng im,
hậu quả là user bị treo màn hình hoặc giao dịch bị chuyển sai đối tượng gây mất an toàn tài chính.
Prototype sẽ xử lý bằng cách tích hợp hộp thoại cảnh báo (Modal Fallback) hiển thị to rõ thông báo lỗi và cung cấp ngay nút bấm quay xe [Hủy bỏ giao dịch] để đưa user về vùng an toàn.

Owner kiểm thử path này là: Lý Hải Long.
```

## 8. Owner plan cho sáng Day 06

| Thành viên                   | Việc phụ trách | Bằng chứng cần có trong repo |
|------------------------------|---|---|
| Lý Hải Long                  | Research / evidence | 02-group-spec/evidence-pack-template.md |
| Lý Hải Long                  | SPEC | 02-group-spec/thin-spec-template.md |
| Lý Hải Long                  | Prototype |  |
| Nguyễn Đức Khang             | Test / failure path |  |
| Lê Quốc Anh, Nguyễn Đức Mạnh | Demo script / repo |  |
