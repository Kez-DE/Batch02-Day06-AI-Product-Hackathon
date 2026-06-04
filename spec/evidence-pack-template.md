# Template — Evidence Pack

Nộp kèm thin SPEC cuối Day 05.

## 1. Nhóm và track

**Tên nhóm:**  F2
**Track:**  Personal Finance
**Product/app đã chọn:**  MoMo — Moni
**Build slice đang nghĩ:**  Luồng thực hiện lệnh chuyển tiền bằng câu lệnh tự nhiên (giọng nói/văn bản) — tự động bóc tách thực thể số điện thoại để gọi Deep-link chuyển hướng thay vì trả về text tĩnh hướng dẫn.

## 2. Self-use evidence

Nhóm tự dùng app/workflow và ghi lại điểm gãy.

| Observation | Screenshot/link          | Path liên quan                           | Điều học được |
|---|--------------------------|------------------------------------------|---|
| Nhập lệnh "Tôi muốn chuyển tiền tới momo 0xxxx". Hệ thống chỉ trả về text hướng dẫn các bước bấm tay thủ công, bắt user tự thoát chat ra ngoài làm lại từ đầu. | 02-group-spec/moni_scr.jpg | Happy / Failure                          | Hệ thống mới chỉ làm NLU (nhận diện intent) để lấy bài viết hướng dẫn tĩnh từ database, chưa có khả năng gọi tool/API ngầm (Function Calling) |
| Nhập câu lệnh thiếu dữ liệu hoặc dùng danh xưng chung chung: "Chuyển tiền cho mẹ". | 02-group-spec/moni_scr_2.jpg                         | Low-confidence                           |  Khi AI không chắc chắn giữa luồng "Hành động" và "Ghi chép", hệ thống tự đoán bừa thay vì đưa ra các nút bấm lựa chọn để xác nhận lại ý định của user.|

## 3. User / review / social evidence

Nguồn có thể là review App Store/Play, group, comment, phỏng vấn nhanh, hoặc nguồn public khác.

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| Chatbot gọi là trợ lý thông minh mà bảo đi chuyển tiền toàn bắt đọc hướng dẫn rồi tự ra màn hình chính làm. Thà tôi tự bấm từ đầu còn nhanh hơn. | Giả định từ hành vi quan sát thực tế của nhóm | Người dùng trẻ tuổi, bận rộn, lười thao tác nhiều bước | User Stuck / Drop-off: Hụt hẫng về trải nghiệm, AI không giải quyết được tác vụ mà lại tăng thêm cognitive load (buộc user phải nhớ số điện thoại, đọc chữ và tự làm lại). |
| "Bố mẹ tôi ở quê mắt kém, mỗi lần bảo chuyển tiền qua app là chịu chết vì quá nhiều nút bấm phức tạp. Thấy có trợ lý ảo Moni tưởng đọc lệnh là xong, ai dè nó hiện ra nguyên một bài hướng dẫn toàn chữ với chữ, người già đọc sao nổi chứ đừng nói là tự thoát ra để làm theo." | Phỏng vấn nhanh/Quan sát hành vi thực tế của thế hệ cha mẹ (người cao tuổi). | Người cao tuổi, người kém công nghệ (Mắt kém, ngại ghi nhớ luồng giao diện phức tạp). | Accessibility Failure: Trợ lý ảo phản hồi bằng "bức tường chữ" vô tình tạo ra rào cản lớn hơn cho người già. Hệ thống tự đoán bừa ý định (nhầm sang ghi chép chi tiêu) khiến họ hoang mang, mất hoàn toàn niềm tin (Trust) và không dám dùng tiếp vì sợ mất tiền. |
|  |  |  |  |

Nếu chưa có nguồn ngoài nhóm, ghi rõ:

```text
Đây là giả định. Nhóm sẽ kiểm bằng [cách] trước checkpoint M1 Day 06.
```

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| Các Trợ lý ảo tiên tiến (Siri/Google Assistant hoặc ReAct Agent) | Khi user nói "Call [Name]" hoặc "Send money to [Name]", trợ lý tự bóc tách contact, gọi API/Deep-link mở thẳng app đích và điền sẵn trường thông tin. | Intent-to-Action qua Deep-link Handoff: Không dừng lại ở việc trả lời bằng chữ, chuyển thẳng user đến màn hình đích của tác vụ kèm data điền sẵn. | Có. Việc đóng gói prompt trả ra JSON chứa cấu trúc gọi tool điều hướng (Deep-link) hoàn toàn khả thi và làm được ngay bằng Vibe Coding trong 1 ngày. |

## 5. Evidence -> Insight

```text
Evidence nổi bật nhất:
Khi user yêu cầu hành động (Action Intent), Moni chỉ phản hồi bằng text hướng dẫn tĩnh (Static QA Retrieval), bắt user tự nhớ thông tin và tự thoát chat ra ngoài app để làm lại.

Insight:
User không chỉ gặp surface problem là phải đọc một bức tường chữ hướng dẫn dài dòng.
Thật ra họ cần [deeper need / decision support / trust / recovery]: Họ cần một sự liền mạch về trải nghiệm (Frictionless). Khi họ đã dùng đến trợ lý ảo, họ kỳ vọng AI phải thực thi hành động thay cho các bước bấm tay rườm rà, giải phóng họ khỏi việc phải ghi nhớ thông tin một cách thủ công.

Opportunity:
AI có thể giúp bằng cách [augment/automate hành động hẹp]: Đóng vai trò là một Agent tăng cường (Augmentation) — tự động bóc tách số điện thoại từ câu lệnh, kiểm tra tính hợp lệ và tự động kích hoạt Deep-link để "dọn sẵn" giao diện chuyển tiền đã điền sẵn thông tin, chỉ chờ user nhập số tiền và duyệt.


Insight:
User không chỉ gặp [surface problem] là phải đọc một bức tường chữ hướng dẫn dài dòng.
Thật ra họ cần [deeper need / decision support / trust / recovery]: Sự tối giản tối đa về mặt thao tác. Đặc biệt với người già kém công nghệ, họ coi Trợ lý giọng nói là giải pháp thay thế hoàn toàn cho việc mò mẫm giao diện. Nếu AI không tự động thực thi (Action), tính năng này hoàn toàn vô giá trị với họ.

Opportunity:
AI có thể giúp bằng cách [augment/automate hành động hẹp]: Tự động hóa việc "dọn đường" giao dịch thông qua Deep-link Handoff. Người già chỉ cần nói đúng 1 câu thoại, AI chuẩn bị sẵn mọi thứ, họ chỉ cần nhìn đúng tên người nhận hiện lên to rõ và bấm "Xác nhận" là xong.
```

## 6. Evidence đổi SPEC như thế nào?

- [ ] Đổi user chính.
- [ ] Đổi pain statement.
- [x] Đổi build slice.
- [ ] Đổi Auto/Aug decision.
- [x] Đổi 4 paths.
- [ ] Đổi failure mode.
- [ ] Đổi owner/test plan.

Ghi rõ 1-2 thay đổi quan trọng:

```text
Trước evidence, nhóm định thiết kế Moni theo hướng một chatbot hỏi đáp, phân tích tài chính và hướng dẫn người dùng quản lý chi tiêu chung chung.

Sau evidence, nhóm đổi thành Tập trung cắt hẳn một lát cắt hẹp nhưng có tính hành động cao: Chuyển dịch từ Chatbot hỏi-đáp thông tin sang Trợ lý thực thi tác vụ (Action-driven Assistant), cụ thể là luồng "Chuyển tiền thông minh bằng giọng nói/văn bản" sử dụng ReAct Agent và Function Calling để kích hoạt giao diện động.

Lý do: Luồng hỏi đáp thông tin hiện tại của app đang làm gãy trải nghiệm nghiêm trọng nhất. Việc chuyển dịch sang Action-driven giúp chứng minh được giá trị thực tế của AI trong việc cắt giảm ít nhất 4 thao tác bấm tay của người dùng, biến sản phẩm từ "vô dụng" thành "tiện dụng".
```
