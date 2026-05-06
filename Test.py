import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="حاسبة لاقرانج", page_icon="📐", layout="centered")

st.title("📐 حاسبة استيفاء لاقرانج")
st.caption("Lagrange Interpolation — الطرق العددية § 2.2.1")

# ── نقاط البيانات ──────────────────────────────────────────
st.subheader("نقاط البيانات")

n = st.number_input("عدد النقاط", min_value=2, max_value=10, value=3, step=1)

cols = st.columns(2)
xs, ys = [], []

for i in range(n):
    with cols[0]:
        xs.append(st.number_input(f"x{i}", value=float(i + 1), key=f"x{i}", format="%g"))
    with cols[1]:
        ys.append(st.number_input(f"f(x{i})", value=float((i + 1) ** 3), key=f"y{i}", format="%g"))

# ── قيمة الاستيفاء ─────────────────────────────────────────
st.subheader("قيمة الاستيفاء")
x_val = st.number_input("أوجد f(x) عند x =", value=1.5, format="%g")

# ── الحساب ─────────────────────────────────────────────────
def lagrange(xs, ys, x):
    n = len(xs)
    result = 0.0
    steps = []
    for i in range(n):
        # حساب البسط والمقام بشكل منفصل لتجنب التعقيد
        num_list = [(x - xs[j]) for j in range(n) if j != i]
        den_list = [(xs[i] - xs[j]) for j in range(n) if j != i]
        
        num = np.prod(num_list)
        den = np.prod(den_list)
        
        Li = num / den
        term = ys[i] * Li
        result += term
        steps.append({"i": i, "Li": Li, "fi": ys[i], "term": term, "num": num, "den": den})
    return result, steps

if st.button("⚡ احسب", use_container_width=True, type="primary"):

    # تحقق من تكرار قيم x
    if len(set(xs)) != len(xs):
        st.error("⚠️ قيم x يجب أن تكون مختلفة لتجنب القسمة على صفر")
        st.stop()

    result, steps = lagrange(xs, ys, x_val)

    # النتيجة النهائية
    st.success(f"**f({x_val:g}) = {result:.6g}**")

    # عرض خطوات الحل
    with st.expander("📝 خطوات الحل", expanded=True):
        for s in steps:
            st.markdown(f"**L{s['i']}({x_val:g})**")
            st.code(
                f"L{s['i']} = {s['num']:.4g} / {s['den']:.4g} = {s['Li']:.6g}\n"
                f"f(x{s['i']}) × L{s['i']} = {s['fi']:g} × {s['Li']:.6g} = {s['term']:.6g}",
                language="text"
            )
        
        # تصحيح طريقة عرض المعادلة النهائية لتجنب أخطاء f-string
        terms_str = " + ".join([f"{s['term']:.4g}" for s in steps])
        st.markdown(f"**P({x_val:g}) = {terms_str} = `{result:.6g}`**")

    # ── الرسم البياني ──────────────────────────────────────────
    st.subheader("التمثيل البياني")
    mg = (max(xs) - min(xs)) * 0.35 or 1
    x_plot = np.linspace(min(xs) - mg, max(xs) + mg, 400)
    y_plot = [lagrange(xs, ys, xp)[0] for xp in x_plot]

    fig, ax = plt.subplots(figsize=(8, 4))
    # تخصيص المظهر ليناسب واجهة Streamlit المظلمة
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    
    ax.plot(x_plot, y_plot, color="#38bdf8", linewidth=2, label="P(x) Interpolation")
    ax.scatter(xs, ys, color="#818cf8", s=80, zorder=5, label="Data Points")
    ax.scatter([x_val], [result], color="#34d399", s=120, marker="*", zorder=6, label=f"Target f({x_val:g})")
    
    ax.tick_params(colors="#64748b")
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e293b")
        
    ax.legend(facecolor="#111827", edgecolor="#1e293b", labelcolor="#e2e8f0", fontsize=10)
    ax.grid(color="#1e293b", linestyle='--', linewidth=0.5)
    st.pyplot(fig)
