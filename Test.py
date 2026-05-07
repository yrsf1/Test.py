import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp # مكتبة للتعامل مع المعادلات الرمزية

st.set_page_config(page_title="حاسبة لاقرانج المتقدمة", page_icon="📐", layout="centered")

st.title("📐 حاسبة استيفاء لاقرانج")
st.caption("Lagrange Interpolation & Error Analysis —")

st.subheader("1️⃣ نقاط البيانات (Data Points)")
n = st.number_input("عدد النقاط المتوفرة", min_value=2, max_value=10, value=4, step=1)

cols = st.columns(2)
xs, ys = [], []

for i in range(n):
    with cols[0]:
        xs.append(st.number_input(f"x{i}", value=float(i + 1), key=f"x{i}", format="%g"))
    with cols[1]:
        ys.append(st.number_input(f"f(x{i})", value=float((i + 1) ** 3), key=f"y{i}", format="%g"))

st.subheader("2️⃣ إعدادات الحساب وتحليل الخطأ")
col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    x_val = st.number_input("أوجد f(x) عند x =", value=3.5, format="%g")
with col_calc2:
    # تعديل: إدخال الدالة بدلاً من القيمة اليدوية
    func_input = st.text_input("الدالة الأصلية (لحساب الخطأ)", value="x**3", help="مثال: x**3 أو np.sin(x)")

def lagrange(xs, ys, x_input):
    n_points = len(xs)
    result = 0.0
    steps = []
    for i in range(n_points):
        num_list = [(x_input - xs[j]) for j in range(n_points) if j != i]
        den_list = [(xs[i] - xs[j]) for j in range(n_points) if j != i]
        
        num = np.prod(num_list)
        den = np.prod(den_list)
        
        Li = num / den
        term = ys[i] * Li
        result += term
        steps.append({"i": i, "Li": Li, "fi": ys[i], "term": term, "num": num, "den": den})
    return result, steps

# دالة إضافية لاستخراج شكل المعادلة الرمزية
def get_polynomial_equation(xs, ys):
    x = sp.symbols('x')
    poly = 0
    for i in range(len(xs)):
        Li = 1
        for j in range(len(xs)):
            if i != j:
                Li *= (x - xs[j]) / (xs[i] - xs[j])
        poly += ys[i] * Li
    return sp.simplify(poly)

if st.button("احسب وحلل النتائج", use_container_width=True, type="primary"):

    if len(set(xs)) != len(xs):
        st.error("⚠️ خطأ رياضي: قيم x يجب أن تكون مختلفة تماماً عن بعضها.")
        st.stop()

    # حساب النتيجة التقريبية
    approx_result, steps = lagrange(xs, ys, x_val)
    
    # حساب القيمة الحقيقية تلقائياً بناءً على الدالة المدخلة
    try:
        actual_val = eval(func_input, {"x": x_val, "np": np, "math": np})
    except:
        st.warning("⚠️ لم يتمكن الكود من حساب القيمة الحقيقية، تأكد من كتابة الدالة بشكل صحيح (مثل x**3)")
        actual_val = 0

    # استخراج المعادلة الرمزية
    equation = get_polynomial_equation(xs, ys)

    st.subheader("تحليل الدقة والخطأ")
    
    abs_error = abs(actual_val - approx_result)
    rel_error = (abs_error / abs(actual_val)) * 100 if actual_val != 0 else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("التقريبية (Approximate)", f"{approx_result:.6g}")
    
    if actual_val != 0:
        m2.metric("الحقيقية (Actual)", f"{actual_val:g}")
        m3.metric("نسبة الخطأ (Error Rate)", f"{rel_error:.4f}%", delta=f"{abs_error:.4g}", delta_color="inverse")
    else:
        m2.info("لم تُدخل دالة صحيحة")

    # عرض المعادلة المستخرجة
    st.info("📝 **معادلة كثير الحدود المستخرجة:**")
    st.latex(f"P(x) = {sp.latex(equation)}")

    st.success(f"**النتيجة المستنتجة: f({x_val:g}) ≈ {approx_result:.6g}**")

    with st.expander("عرض خطوات الحل التفصيلية (Math Breakdown)", expanded=False):
        for s in steps:
            st.markdown(f"**حساب المعامل L{s['i']}({x_val:g})**")
            st.code(
                f"L{s['i']} = {s['num']:.4g} / {s['den']:.4g} = {s['Li']:.6g}\n"
                f"f(x{s['i']}) × L{s['i']} = {s['fi']:g} × {s['Li']:.6g} = {s['term']:.6g}",
                language="text"
            )
        
        terms_str = " + ".join([f"{s['term']:.4g}" for s in steps])
        st.markdown(f"**P({x_val:g}) = {terms_str} = `{approx_result:.6g}`**")

    st.subheader("📈 التمثيل البياني للمنحنى")
    
    margin = (max(xs) - min(xs)) * 0.4 or 1
    x_plot = np.linspace(min(xs) - margin, max(xs) + margin, 400)
    y_plot = [lagrange(xs, ys, xp)[0] for xp in x_plot]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#cad1de")
    ax.set_facecolor("#e9eef8")

    ax.plot(x_plot, y_plot, color="#38bdf8", linewidth=2.5, label="كثير حدود لاقرانج P(x)", alpha=0.9)
    ax.scatter(xs, ys, color="#818cf8", s=100, zorder=5, label="نقاط البيانات")
    
    ax.scatter([x_val], [approx_result], color="#34d399", s=200, marker="*", zorder=6, label=f"Approx: {approx_result:.4g}")
    
    if actual_val != 0:
        ax.scatter([x_val], [actual_val], color="#f87171", s=120, marker="x", zorder=7, label=f"Actual: {actual_val:g}")

    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#334155")
    ax.legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="#f8fafc")
    ax.grid(color="#334155", linestyle='--', alpha=0.4)
    
    st.pyplot(fig)
