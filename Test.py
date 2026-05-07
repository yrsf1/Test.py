import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# ── 1. إعداد الصفحة والتنسيق (Beige Theme) ──────────────────────
st.set_page_config(page_title="حاسبة لاقرانج المتقدمة", page_icon="📐", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #F5F5DC; }
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label { color: #2c3e50 !important; }
    .stNumberInput input, .stTextInput input { background-color: #ffffff !important; color: #2c3e50 !important; }
    .stExpander { background-color: #ffffff !important; border: 1px solid #dcdcdc !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📐 حاسبة استيفاء لاقرانج المارّة")
st.caption("Lagrange Interpolation: المعادلة الرمزية وتحليل الخطأ")

# ── 2. مدخلات البيانات ──────────────────────────────────────────
st.subheader("1️⃣ إدخال النقاط")
n = st.number_input("عدد النقاط", min_value=2, max_value=10, value=3, step=1)

cols = st.columns(2)
xs, ys = [], []

for i in range(n):
    with cols[0]:
        xs.append(st.number_input(f"x{i}", value=float(i), key=f"x{i}", format="%g"))
    with cols[1]:
        ys.append(st.number_input(f"f(x{i})", value=float(i**3), key=f"y{i}", format="%g"))

# ── 3. إعدادات الحساب والدالة الأصلية ──────────────────────────
st.subheader("2️⃣ إعدادات الحساب")
col_func1, col_func2 = st.columns(2)

with col_func1:
    x_target = st.number_input("احسب عند x =", value=1.5, format="%g")
with col_func2:
    func_str = st.text_input("صيغة الدالة الأصلية (لحساب الخطأ)", value="x**3", help="مثال: x**3 أو np.sin(x) أو np.exp(x)")

# ── 4. المحرك الرياضي وبناء المعادلة ──────────────────────────────
def get_lagrange_polynomial(xs, ys):
    x = sp.symbols('x')
    poly = 0
    n_points = len(xs)
    for i in range(n_points):
        # بناء معامل لاقرانج رمزياً
        L_i = 1
        for j in range(n_points):
            if i != j:
                L_i *= (x - xs[j]) / (xs[i] - xs[j])
        poly += ys[i] * L_i
    return sp.simplify(poly)

def calculate_lagrange(xs, ys, x_val):
    n_points = len(xs)
    result = 0.0
    steps = []
    for i in range(n_points):
        num_list = [(x_val - xs[j]) for j in range(n_points) if j != i]
        den_list = [(xs[i] - xs[j]) for j in range(n_points) if j != i]
        num, den = np.prod(num_list), np.prod(den_list)
        Li = num / den
        term = ys[i] * Li
        result += term
        steps.append({"i": i, "Li": Li, "fi": ys[i], "term": term, "num": num, "den": den})
    return result, steps

# ── 5. التنفيذ والعرض ──────────────────────────────────────────
if st.button("⚡ استخراج المعادلة والحساب", use_container_width=True, type="primary"):
    if len(set(xs)) != len(xs):
        st.error("⚠️ خطأ: قيم x يجب أن تكون مختلفة.")
        st.stop()

    # أ- حساب المعادلة الرمزية
    final_poly = get_lagrange_polynomial(xs, ys)
    
    # ب- الحساب العددي
    approx_val, steps = calculate_lagrange(xs, ys, x_target)
    
    # ج- حساب القيمة الحقيقية تلقائياً
    try:
        # تجهيز البيئة لـ eval لتشمل numpy
        actual_val = eval(func_str, {"x": x_target, "np": np, "math": np})
    except:
        actual_val = None

    # عرض المعادلة الرمزية
    st.subheader("📝 معادلة كثير الحدود P(x)")
    st.latex(f"P(x) = {sp.latex(final_poly)}")
    
    # تحليل النتائج
    st.subheader("📊 تحليل النتائج")
    m1, m2, m3 = st.columns(3)
    m1.metric("التقريبية (Approx)", f"{approx_val:.6g}")
    
    if actual_val is not None:
        abs_err = abs(actual_val - approx_val)
        rel_err = (abs_err / abs(actual_val)) * 100 if actual_val != 0 else 0
        m2.metric("الحقيقية (Actual)", f"{actual_val:.6g}")
        m3.metric("نسبة الخطأ (%)", f"{rel_err:.4f}%", delta=f"{abs_err:.4g}", delta_color="inverse")
    
    # خطوات الحل
    with st.expander("📝 خطوات التعويض التفصيلية"):
        for s in steps:
            st.code(f"L{s['i']} = {s['num']:.4g} / {s['den']:.4g} = {s['Li']:.6g}\nTerm{s['i']} = {s['fi']} * {s['Li']:.6g} = {s['term']:.6g}")

    # الرسم البياني
    st.subheader("📈 التمثيل البياني")
    margin = (max(xs) - min(xs)) * 0.4 or 1
    x_axis = np.linspace(min(xs) - margin, max(xs) + margin, 400)
    y_axis = [calculate_lagrange(xs, ys, val)[0] for val in x_axis]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#F5F5DC")
    ax.set_facecolor("#F5F5DC")
    ax.plot(x_axis, y_axis, label="P(x) Interpolation", color="#1a73e8", lw=2)
    ax.scatter(xs, ys, color="#512da8", zorder=5, label="Points")
    ax.scatter([x_target], [approx_val], color="#28a745", marker="*", s=200, label="Target")
    
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)
