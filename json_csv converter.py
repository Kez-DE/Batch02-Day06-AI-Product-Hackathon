import pandas as pd
json_in_path='./momo_bot/data/2000_moz.json'
csv_in_path='./momo_bot/data/phonebook.csv'
json_out_path='./momo_bot/data/phonebook.json'
csv_out_path='./momo_bot/data/2000_moz.csv'
def json_csv(json_path):
    df = pd.read_json(json_path)
    df['phone_number'] = df['phone_number'].astype(str)
    df.to_csv(csv_out_path, index=False, encoding="utf-8-sig",sep=';')
    print("Đã chuyển đổi thành công sang file CSV!")
    return df


def csv_json(csv_path, json_out_path):
    # 1. Đọc file CSV (Nhớ chỉ định đúng dấu phân cách sep=';' đã dùng ở bước trước)
    df = pd.read_csv(csv_path, sep=';')

    # 2. Làm sạch cột số điện thoại (Xóa bỏ ký tự ẩn '\t' nếu có để JSON đạt chuẩn)
    if 'phone_number' in df.columns:
        df['phone_number'] = df['phone_number'].astype(str).str.replace('\t', '', regex=False).str.strip()

        # Đảm bảo giữ đủ 10 chữ số có số 0 ở đầu trong chuỗi JSON
        df['phone_number'] = df['phone_number'].str.zfill(10)

    # 3. Xuất ra định dạng JSON Records, force_ascii=False để không bị lỗi font tiếng Việt (thành \u00e1...)
    df.to_json(json_out_path, orient='records', force_ascii=False, indent=4)

    print(f"Đã chuyển đổi thành công sang file JSON tại: {json_out_path}")
    return df
if __name__ == "__main__":
    csv_json(csv_in_path,json_out_path)
