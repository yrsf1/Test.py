import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعداد الصفحة لتظهر بشكل احترافي
st.set_page_config(page_title="حاسبة لاقرانج المتقدمة", page_icon="📐", layout="centered")

st.title("📐 حاسبة استيفاء لاقرانج")
st.caption("Lagrange Interpolation & Error Analysis — تصميم يوسف الشمري")

# ── 1. مدخلات نقاط البيانات ──────────────────────────────────────────
st.subheader("1️⃣ نقاط البيانات (Data Points)")
n = st.number_input("عدد النقاط المتوفرة", min_value=2, max_value=10, value=4, step=1)

cols = st.columns(2)
xs, ys = [], []

for i in range(n):
    with cols[0]:
        xs.append(st.number_input(f"x{i}", value=float(i + 1), key=f"x{i}", format="%g"))
    with cols[1]:
        # القيمة الافتراضية هنا هي مكعب العدد لتسهيل التجربة
        ys.append(st.number_input(f"f(x{i})", value=float((i + 1) ** 3), key=f"y{i}", format="%g"))

# ── 2. إعدادات الحساب والتحليل ──────────────────────────────────────
st.subheader("2️⃣ إعدادات الحساب وتحليل الخطأ")
col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    x_val = st.number_input("أوجد f(x) عند x =", value=3.5, format="%g")
with col_calc2:
    # القيمة الحقيقية اختيارية لمقارنة دقة الخوارزمية
    actual_val = st.number_input("القيمة الحقيقية (Actual Value)", value=42.875, format="%g", 
                                 help="أدخل القيمة الصحيحة تماماً للدالة (إن وجدت) لحساب نسبة الخطأ")

# ── 3. المحرك الرياضي لخوارزمية لاقرانج ──────────────────────────────
def lagrange(xs, ys, x):
    n_points = len(xs)
    result = 0.0
    steps = []
    for i in range(n_points):
        # حساب بسط ومقام معامل لاقرانج Li
        num_list = [(x - xs[j]) for j in range(n_points) if j != i]
        den_list = [(xs[i] - xs[j]) for j in range(n_points) if j != i]
        
        num = np.prod(num_list)
        den = np.prod(den_list)
        
        Li = num / den
        term = ys[i] * Li
        result += term
        
        # تخزين الخطوات للعرض لاحقاً
        steps.append({"i": i, "Li": Li, "fi": ys[i], "term": term, "num": num, "den": den})
    return result, steps

# ── 4. تنفيذ الحساب وعرض النتائج ────────────────────────────────────
if st.button("⚡ احسب وحلل النتائج", use_container_width=True, type="primary"):

    # التحقق من عدم تكرار قيم x لتجنب القسمة على صفر
    if len(set(xs)) != len(xs):
        st.error("⚠️ خطأ رياضي: قيم x يجب أن تكون مختلفة تماماً عن بعضها.")
        st.stop()

    approx_result, steps = lagrange(xs, ys, x_val)

    # 📊 عرض المقارنة والتحليل الإحصائي (المطلوب)
    st.subheader("📊 تحليل الدقة والخطأ")
    
    # حساب الأخطاء
    abs_error = abs(actual_val - approx_result)
    rel_error = (abs_error / abs(actual_val)) * 100 if actual_val != 0 else 0

    # عرض النتائج في بطاقات Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("التقريبية (Approximate)", f"{approx_result:.6g}")
    
    if actual_val != 0:
        m2.metric("الحقيقية (Actual)", f"{actual_val:g}")
        # عرض نسبة الخطأ مع مقدار الفرق المطلق
        m3.metric("نسبة الخطأ (Error Rate)", f"{rel_error:.4f}%", delta=f"{abs_error:.4g}", delta_color="inverse")
    else:
        m2.info("أدخل قيمة حقيقية لمشاهدة تحليل الخطأ")

    st.success(f"**النتيجة المستنتجة: f({x_val:g}) ≈ {approx_result:.6g}**")

    # 📝 عرض خطوات الحل بالتفصيل
    with st.expander("📝 عرض خطوات الحل التفصيلية (Math Breakdown)", expanded=False):
        for s in steps:
            st.markdown(f"**حساب المعامل L{s['i']}({x_val:g})**")
            st.code(
                f"L{s['i']} = {s['num']:.4g} / {s['den']:.4g} = {s['Li']:.6g}\n"
                f"f(x{s['i']}) × L{s['i']} = {s['fi']:g} × {s['Li']:.6g} = {s['term']:.6g}",
                language="text"
            )
        
        terms_str = " + ".join([f"{s['term']:.4g}" for s in steps])
        st.markdown(f"**P({x_val:g}) = {terms_str} = `{approx_result:.6g}`**")

    # ── 5. التمثيل البياني المطور ──────────────────────────────────────
    st.subheader("📈 التمثيل البياني للمنحنى")
    
    # تجهيز بيانات الرسم
    margin = (max(xs) - min(xs)) * 0.4 or 1
    x_plot = np.linspace(min(xs) - margin, max(xs) + margin, 400)
    y_plot = [lagrange(xs, ys, xp)[0] for xp in x_plot]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    
    # رسم المنحنى ونقاط الإدخال
    ax.plot(x_plot, y_plot, color="#38bdf8", linewidth=2.5, label="كثير حدود لاقرانج P(x)", alpha=0.9)
    ax.scatter(xs, ys, color="#818cf8", s=100, zorder=5, label="نقاط البيانات")
    
    # تمييز النقطة التقريبية بنجمة
    ax.scatter([x_val], [approx_result], color="#34d399", s=200, marker="*", zorder=6, label=f"Approx: {approx_result:.4g}")
    
    # تمييز النقطة الحقيقية (إن وجدت) بعلامة X للمقارنة
    if actual_val != 0:
        ax.scatter([x_val], [actual_val], color="#f87171", s=120, marker="x", zorder=7, label=f"Actual: {actual_val:g}")

    # تحسين مظهر المحاور والشبكة
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#334155")
    ax.legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="#f8fafc")
    ax.grid(color="#334155", linestyle='--', alpha=0.4)
    
    st.pyplot(fig)
