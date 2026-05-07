import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="حاسبة لاقرانج المتقدمة", page_icon="📐", layout="centered")

st.title("📐 حاسبة استيفاء لاقرانج")
st.caption("Lagrange Interpolation & Error Analysis — الإصدار المطور")

# ── 1. إدخال نقاط البيانات ──────────────────────────────────────────
st.subheader("1️⃣ نقاط البيانات (Data Points)")
n = st.number_input("عدد النقاط", min_value=2, max_value=10, value=4, step=1)

cols = st.columns(2)
xs, ys = [], []

for i in range(n):
    with cols[0]:
        xs.append(st.number_input(f"x{i}", value=float(i + 1), key=f"x{i}", format="%g"))
    with cols[1]:
        # القيمة الافتراضية هنا هي مكعب العدد لتسهيل التجربة
        ys.append(st.number_input(f"f(x{i})", value=float((i + 1) ** 3), key=f"y{i}", format="%g"))

# ── 2. إعدادات الحساب وتحليل الخطأ ──────────────────────────────────────
st.subheader("2️⃣ إعدادات الحساب وتحليل الخطأ")
col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    x_val = st.number_input("أوجد f(x) عند x =", value=3.5, format="%g")
with col_calc2:
    # القيمة الحقيقية لحساب دقة الخوارزمية
    actual_val = st.number_input("القيمة الحقيقية (Actual Value)", value=0.0, format="%g", 
                                 help="أدخل القيمة الصحيحة للدالة لحساب نسبة الخطأ")

# ── 3. خوارزمية لاقرانج (المحرك الرياضي) ──────────────────────────────
def lagrange(xs, ys, x):
    n_points = len(xs)
    result = 0.0
    steps = []
    for i in range(n_points):
        # تطبيق قانون معامل لاقرانج Li(x)
        num_list = [(x - xs[j]) for j in range(n_points) if j != i]
        den_list = [(xs[i] - xs[j]) for j in range(n_points) if j != i]
        
        num = np.prod(num_list)
        den = np.prod(den_list)
        
        Li = num / den
        term = ys[i] * Li
        result += term
        
        # تخزين الخطوات للعرض
        steps.append({"i": i, "Li": Li, "fi": ys[i], "term": term, "num": num, "den": den})
    return result, steps

# ── 4. تنفيذ الحساب وعرض النتائج ────────────────────────────────────
if st.button("⚡ احسب وحلل النتائج", use_container_width=True, type="primary"):

    # التحقق من تكرار قيم x (تجنب القسمة على صفر)
    if len(set(xs)) != len(xs):
        st.error("⚠️ خطأ: قيم x يجب أن تكون مختلفة تماماً.")
        st.stop()

    approx_result, steps = lagrange(xs, ys, x_val)

    # 📊 عرض تحليل الدقة والخطأ (Metrics)
    st.subheader("📊 تحليل النتائج")
    
    # حساب الأخطاء
    abs_error = abs(actual_val - approx_result)
    rel_error = (abs_error / abs(actual_val)) * 100 if actual_val != 0 else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("التقريبية (Approx)", f"{approx_result:.6g}")
    
    if actual_val != 0:
        m2.metric("الحقيقية (Actual)", f"{actual_val:g}")
        m3.metric("نسبة الخطأ (%)", f"{rel_error:.4f}%", delta=f"{abs_error:.4g}", delta_color="inverse")
    else:
        m2.info("أدخل قيمة حقيقية لحساب الخطأ")

    st.success(f"**النتيجة التقريبية: f({x_val:g}) ≈ {approx_result:.6g}**")

    # 📝 خطوات الحل بالتفصيل
    with st.expander("📝 خطوات الحل الرياضية", expanded=False):
        for s in steps:
            st.markdown(f"**حساب المعامل L{s['i']}({x_val:g})**")
            st.code(
                f"L{s['i']} = {s['num']:.4g} / {s['den']:.4g} = {s['Li']:.6g}\n"
                f"f(x{s['i']}) × L{s['i']} = {s['fi']:g} × {s['Li']:.6g} = {s['term']:.6g}",
                language="text"
            )
        
        terms_str = " + ".join([f"{s['term']:.4g}" for s in steps])
        st.markdown(f"**P({x_val:g}) = {terms_str} = `{approx_result:.6g}`**")

    # ── 5. التمثيل البياني (بالخلفية البيضاء) ──────────────────────────
    st.subheader("📈 التمثيل البياني")
    
    margin = (max(xs) - min(xs)) * 0.4 or 1
    x_plot = np.linspace(min(xs) - margin, max(xs) + margin, 400)
    y_plot = [lagrange(xs, ys, xp)[0] for xp in x_plot]

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # ضبط الخلفية لتكون بيضاء بالكامل
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    
    # رسم المنحنى ونقاط البيانات بألوان واضحة على الخلفية البيضاء
    ax.plot(x_plot, y_plot, color="#007bff", linewidth=2.5, label="منحنى لاقرانج P(x)")
    ax.scatter(xs, ys, color="#5a2d81", s=100, zorder=5, label="نقاط البيانات")
    
    # تمييز النقطة المستخرجة والحقيقية
    ax.scatter([x_val], [approx_result], color="#28a745", s=200, marker="*", zorder=6, label=f"Approx: {approx_result:.4g}")
    if actual_val != 0:
        ax.scatter([x_val], [actual_val], color="#dc3545", s=120, marker="x", zorder=7, label=f"Actual: {actual_val:g}")

    # تحسين مظهر المحاور لتناسب الخلفية البيضاء
    ax.tick_params(colors="#333333", labelsize=10)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    
    ax.legend(facecolor="white", edgecolor="#333333", labelcolor="black")
    ax.grid(color="#dddddd", linestyle='--', alpha=0.7)
    
    # عرض الرسم في Streamlit
    st.pyplot(fig)
