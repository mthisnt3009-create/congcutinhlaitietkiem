import streamlit as st

st.set_page_config(
    page_title="Ứng Dụng Tính Lãi Tiết Kiệm", page_icon="💰", layout="centered"
)

st.title("💰 Ứng Dụng Tính Lãi Tiết Kiệm Ngân Hàng")
st.write(
    "Nhập các thông tin bên dưới để tính toán số tiền lãi và tổng số tiền nhận được khi gửi tiết kiệm."
)

# --- KHU VỰC NHẬP LIỆU (SIDEBAR HOẶC FORM CHÍNH) ---
st.header("1. Nhập thông tin gửi tiết kiệm")

col1, col2 = st.columns(2)

with col1:
    # Số tiền gửi (VND)
    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=1_000_000,
        value=500_000_000,
        step=1_000_000,
        format="%d",
    )

    # Kỳ hạn gửi
    term_months = st.number_input(
        "Kỳ hạn gửi (tháng)", min_value=1, value=12, step=1
    )

with col2:
    # Lãi suất (%/năm hoặc %/tháng, ở đây mặc định chọn %/năm và quy đổi, hoặc nhập trực tiếp %/năm)
    interest_rate_annual = (
        st.number_input(
            "Lãi suất (%/năm)",
            min_value=0.1,
            max_value=50.0,
            value=6.0,
            step=0.1,
        )
        / 100
    )

    # Hình thức nhận lãi
    payment_method = st.selectbox(
        "Hình thức nhận lãi",
        options=["Cuối kỳ", "Hàng tháng", "Hàng quý"],
        index=0,
    )

# --- XỬ LÝ TÍNH TOÁN ---
if st.button("Tính toán", type="primary"):
    # Lãi suất hàng tháng
    monthly_rate = interest_rate_annual / 12

    periodic_interest = 0.0  # Tiền lãi định kỳ (nếu nhận hàng tháng/quý)
    total_interest = 0.0  # Tổng tiền lãi
    total_amount = 0.0  # Tổng số tiền gốc và lãi

    if payment_method == "Cuối kỳ":
        # Giả định gửi tiết kiệm thông thường cuối kỳ áp dụng lãi suất đơn/hoặc kép tùy chọn,
        # chuẩn ngân hàng thường tính lãi kép hoặc lãi đơn theo số ngày thực tế, nhưng phổ biến cơ bản là lãi đơn hoặc kép tích lũy.
        # Ở đây ta tính theo lãi đơn tích lũy cuối kỳ: Tổng lãi = Gốc * (Lãi suất/năm / 12) * số tháng
        total_interest = principal * monthly_rate * term_months
        periodic_interest = (
            total_interest  # Lãi nhận một lần toàn bộ cuối kỳ
        )
        total_amount = principal + total_interest

    elif payment_method == "Hàng tháng":
        # Tiền lãi nhận đều mỗi tháng
        periodic_interest = principal * monthly_rate
        total_interest = periodic_interest * term_months
        total_amount = principal  # Gốc giữ nguyên, nhận lãi đều hàng tháng

    elif payment_method == "Hàng quý":
        # 1 quý = 3 tháng
        periodic_interest = principal * monthly_rate * 3
        # Số quý (làm tròn hoặc tính chuẩn theo số tháng)
        number_of_quarters = term_months / 3
        total_interest = periodic_interest * number_of_quarters
        total_amount = principal  # Gốc giữ nguyên

    # --- HIỂN THỊ KẾT QUẢ ---
    st.divider()
    st.header("2. Kết quả tính toán")

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.metric(
            label="Tiền lãi định kỳ",
            value=f"{periodic_interest:,.0f} VNĐ",
            help="Số tiền lãi nhận được mỗi kỳ (tháng/quý) hoặc tổng lãi cuối kỳ.",
        )

    with res_col2:
        st.metric(
            label="Tổng tiền lãi",
            value=f"{total_interest:,.0f} VNĐ",
            help="Tổng số tiền lãi nhận được trong suốt kỳ hạn.",
        )

    with res_col3:
        st.metric(
            label="Tổng gốc và lãi",
            value=f"{total_amount:,.0f} VNĐ",
            help="Tổng số tiền nhận được khi đáo hạn (bao gồm cả gốc nếu nhận cuối kỳ).",
        )

    # Bảng chi tiết tóm tắt
    st.subheader("Chi tiết thông tin")
    st.write(
        f"- **Số tiền gửi ban đầu:** {principal:,.2f} VNĐ\n"
        f"- **Kỳ hạn:** {term_months} tháng\n"
        f"- **Lãi suất:** {interest_rate_annual*100:.2f} %/năm\n"
        f"- **Hình thức nhận lãi:** {payment_method}"
    )
