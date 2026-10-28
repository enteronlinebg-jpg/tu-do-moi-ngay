# Tủ Đồ Mỗi Ngày – kho chung Claude + Muse (KENH-03)

Muse: **luôn lấy khuôn và quy chuẩn mới nhất từ kho này trước mỗi lô.** Không tự sửa số đo trong `khuon/lb.html`.

## Thư mục
| Đường dẫn | Nội dung |
|---|---|
| `khuon/lb.html` | Khuôn dựng 1080x1920, 31s (1,6 + 5×5,4 + 2,4). **Bố cục v2 – vùng an toàn Reels** (28/10/2026) |
| `khuon/rec.py`, `khuon/cut.py` | Render từng khung → ffmpeg; tách nền rembg + cắt theo alpha |
| `quy-chuan/TIEU-CHUAN-TY-LE.txt` | Tỷ lệ đo từ video tham chiếu + **mục 6 vùng an toàn (ưu tiên cao nhất)** |
| `quy-chuan/QUY-TAC-DA-DANG-VA-SAN-PHAM.txt` | Đa dạng màu/giày, sản phẩm cấm, chuẩn links.csv & loi-doc.json |
| `quy-chuan/BAN-CHOT-THOI-TRANG.txt` | Bản chốt quy trình gốc (22/10). Số đo vị trí trong mục 1 đã được thay bằng bố cục v2 |
| `kho/KHO-SP-KENH03.csv` | Kho sản phẩm (nhom, itemid, ten_sp, gia, …). Muse chỉ dùng itemid → ghi `{SP:itemid}` |
| `cong-cu/` | Công cụ của Claude: làm thumbnail, vá lỗ tách nền, viết bình luận ghim theo từng cách |

## Bố cục v2 (khung 1080x1920)
| Thành phần | Vị trí |
|---|---|
| Chữ "Phối…/Phong cách…" | y 290–390, x 65–940, tối đa 2 dòng |
| Món chính | x 40–460, y 400–770 |
| Món phối | x 40–460, y 790–1110 |
| Giày | x 60–440, y 1120–1240 (**không xuống dưới 1248**) |
| Người mẫu | x 450–940, y 300–1820 (đầu ~300, chỉ phần chân vào vùng dưới) |
| Màn kết | logo + câu hỏi + nút link trong y 400–1150 |

Vùng Reels che: trên 270px, dưới 672px, mép trái/phải 65px, cột nút phải x>940 (y 900–1750).

## Đã làm (không lặp món chính)
006–053: blazer đen, chân váy xếp ly trắng, cardigan be, jean ống rộng, sơ mi trắng, chân váy jean, áo phao trần trám, áo dạ caro, len nút vàng, blazer SALALU, váy dạ xếp ly, jean trắng, cardigan len tăm, blazer 2 lớp, cardigan A24, HAVANA, len Miho, kaki ống rộng, cardigan dài, váy kaki, quần tây, jean retro, len Miho Studio, áo tay lỡ, blazer công sở, cardigan SEOULIFE, cardigan gân tăm, váy xòe bồng, jean MIAA, kaki Nhật, măng tô dạ dài, khoác da mềm, dạ tweed, gile viền kẻ, hoodie ChillPop, set nỉ, dạ ép lửng đỏ đô, măng tô cổ bẻ, bomber dù, gile ngọc trai, váy xòe dài, quần nỉ, dạ A.817, dạ ForgirlStudio hồng, mangto vest ngắn, gile có mũ, set váy cardigan, hoodie boxy.
