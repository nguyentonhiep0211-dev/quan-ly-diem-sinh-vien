import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cau hinh trang web
st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="📚",
    layout="wide"
)

# Tieu de
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý và tra cứu điểm sinh viên")

# 1. Tao DataFrame - GIU NGUYEN DU LIEU CUA BAN
data = {
    "Ho_ten": [
        "Trinh Hoai Bang",
        "Beng cuti",
        "Beng Beng thui",
        "Khom bic(1)",
        "Khom bic(2)",
        "Khom bic(3)",
        "Khom bic(4)",
        "Cuc zang",
        "Khom bic(6)",
        "Khom bic(7)"
    ],
    "Chuyen_can": [9, 8, 10, 7, 8, 9, 6, 10, 7, 8],
    "Giua_ky":    [8, 7, 9, 6, 7, 8, 5, 9, 6, 7],
    "Cuoi_ky":    [9, 8, 8, 7, 6, 9, 5, 10, 7, 8]
}

df = pd.DataFrame(data)

# 2. Tinh diem tong ket
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
)

# 3. Xep loai sinh vien
def xep_loai(diem):
    if diem >= 8.5:
        return "Gioi"
    elif diem >= 7.0:
        return "Kha"
    elif diem >= 5.0:
        return "Trung binh"
    else:
        return "Yeu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Thong ke
diem_tb = df["Tong_ket"].mean()
diem_cao_nhat = df["Tong_ket"].max()
diem_thap_nhat = df["Tong_ket"].min()
so_sinh_vien_dat = (df["Tong_ket"] >= 5).sum()

st.subheader("Thống kê chung")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{diem_cao_nhat:.2f}")
c3.metric("Điểm thấp nhất", f"{diem_thap_nhat:.2f}")
c4.metric("Số sinh viên đạt", int(so_sinh_vien_dat))

st.write("### Sinh viên có điểm cao nhất")
st.dataframe(
    df[df["Tong_ket"] == diem_cao_nhat][["Ho_ten", "Tong_ket"]],
    hide_index=True,
    use_container_width=True
)

st.write("### Sinh viên có điểm thấp nhất")
st.dataframe(
    df[df["Tong_ket"] == diem_thap_nhat][["Ho_ten", "Tong_ket"]],
    hide_index=True,
    use_container_width=True
)

# 5. Hien thi bang diem
st.subheader("Bảng điểm 10 sinh viên")

bang_diem = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_diem.round({"Tổng kết": 2}),
    hide_index=True,
    use_container_width=True
)

# 6. Tra cuu tung sinh vien
st.subheader("Tra cứu sinh viên")

ten_sv = st.selectbox("Chọn sinh viên", df["Ho_ten"].tolist())
sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.write(f"**Họ tên:** {sv['Ho_ten']}")
st.write(f"**Chuyên cần:** {sv['Chuyen_can']}")
st.write(f"**Giữa kỳ:** {sv['Giua_ky']}")
st.write(f"**Cuối kỳ:** {sv['Cuoi_ky']}")
st.write(f"**Điểm tổng kết:** {sv['Tong_ket']:.2f}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# 7. Ve bieu do
st.subheader("Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.tick_params(axis="x", labelrotation=45)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 8. Thong tin nguoi tao
st.divider()
st.caption("Người tạo ứng dụng: Nguyễn Tôn Hiệp")
st.caption("MSSV: 038208022556")
