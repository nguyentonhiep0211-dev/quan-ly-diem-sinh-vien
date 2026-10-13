import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# 1. CAU HINH TRANG WEB
# ========================================
st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="📚",
    layout="wide"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý và thống kê điểm của sinh viên.")

# ========================================
# 2. TAO DATAFRAME
# ========================================
data = {
    "Ho_ten": [
        "Nguyen Van An",
        "Tran Thi Binh",
        "Le Van Cuong",
        "Pham Thi Dung",
        "Hoang Van Em",
        "Vo Thi Giang",
        "Dang Van Hung",
        "Bui Thi Lan",
        "Do Van Minh",
        "Ngo Thi Nhung"
    ],
    "Chuyen_can": [9, 8, 10, 7, 8, 9, 6, 10, 7, 8],
    "Giua_ky": [8, 7, 9, 6, 7, 8, 5, 9, 6, 7],
    "Cuoi_ky": [9, 8, 8, 7, 6, 9, 5, 10, 7, 8]
}

df = pd.DataFrame(data)

# ========================================
# 3. TINH DIEM TONG KET
# ========================================
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
)

# ========================================
# 4. XEP LOAI SINH VIEN
# ========================================
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# ========================================
# 5. THONG KE
# ========================================
diem_tb = df["Tong_ket"].mean()
diem_max = df["Tong_ket"].max()
diem_min = df["Tong_ket"].min()
so_sinh_vien_dat = (df["Tong_ket"] >= 5).sum()

st.subheader("Thống kê chung")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Điểm trung bình", f"{diem_tb:.2f}")
col2.metric("Điểm cao nhất", f"{diem_max:.2f}")
col3.metric("Điểm thấp nhất", f"{diem_min:.2f}")
col4.metric("Số sinh viên đạt", f"{so_sinh_vien_dat}/10")

st.write(
    "**Sinh viên có điểm cao nhất:**",
    ", ".join(df.loc[df["Tong_ket"] == diem_max, "Ho_ten"])
)

st.write(
    "**Sinh viên có điểm thấp nhất:**",
    ", ".join(df.loc[df["Tong_ket"] == diem_min, "Ho_ten"])
)

# ========================================
# 6. HIEN THI BANG DIEM
# ========================================
st.subheader("Bảng điểm sinh viên")

bang_hien_thi = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_hien_thi.round(2),
    use_container_width=True,
    hide_index=True
)

# ========================================
# 7. CHON SINH VIEN VA XEM DIEM
# ========================================
st.subheader("Tra cứu điểm sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.write(f"### Thông tin của {ten_sv}")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
c2.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
c3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
c4.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
c5.metric("Xếp loại", sv["Xep_loai"])

# ========================================
# 8. VE BIEU DO COT
# ========================================
st.subheader("Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(df["Ho_ten"], df["Tong_ket"])

ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ========================================
# 9. THONG TIN NGUOI TAO
# ========================================
st.divider()

st.caption("Người tạo ứng dụng: [Điền họ tên của bạn]")
st.caption("MSSV: [Điền mã số sinh viên của bạn]")
