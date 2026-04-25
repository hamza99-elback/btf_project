import streamlit as st

from catalog import CATALOG
from pricing import get_bttf_reduction_rate, get_total_price

st.set_page_config(
    page_title="DVD Cart — Back to the Future",
    page_icon="📼",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Orbitron:wght@500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* === BTTF palette ===
   --bg-deep:   #0a0420  (deep night sky)
   --bg-panel:  #14082e  (twilight purple)
   --flame-red: #ff2a2a  (logo red)
   --flame-org: #ff7a00  (logo orange)
   --neon-cyan: #00e5ff  (flux capacitor blue)
   --neon-pink: #ff2bd6  (1985 sign pink)
   --cream:     #f4ecd8  (parchment text)
*/

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
}

.stApp {
    background:
        radial-gradient(ellipse at top, #1a0a3d 0%, #0a0420 55%, #050010 100%);
    color: #f4ecd8;
}

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.05em;
    color: #f4ecd8;
}

.title-block {
    border-left: 4px solid #ff7a00;
    padding-left: 16px;
    margin-bottom: 2rem;
    background: linear-gradient(90deg, rgba(255,122,0,0.08) 0%, transparent 60%);
    padding-top: 8px;
    padding-bottom: 8px;
    border-radius: 0 6px 6px 0;
}

.title-block h1 {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 2.8rem;
    margin: 0;
    line-height: 1;
    background: linear-gradient(180deg, #ffd76a 0%, #ff7a00 50%, #ff2a2a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 18px rgba(255,122,0,0.35);
    letter-spacing: 0.04em;
}

.title-block p {
    font-size: 0.72rem;
    color: #00e5ff;
    margin: 6px 0 0;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    text-shadow: 0 0 6px rgba(0,229,255,0.5);
}

.section-label {
    font-family: 'Orbitron', sans-serif;
    font-weight: 500;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #00e5ff;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0,229,255,0.25);
    padding-bottom: 6px;
    text-shadow: 0 0 6px rgba(0,229,255,0.45);
}

.film-card {
    background: linear-gradient(160deg, #1a0d3a 0%, #0f0626 100%);
    border: 1px solid #2d1858;
    border-radius: 6px;
    padding: 14px;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.film-card:hover {
    border-color: #ff7a00;
    box-shadow: 0 0 14px rgba(255,122,0,0.35);
}

.film-card.bttf {
    border-left: 3px solid #ff7a00;
    box-shadow: inset 2px 0 12px rgba(255,42,42,0.15);
}

.film-card.other {
    border-left: 3px solid #00e5ff;
}

.film-card .tag {
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #ff2bd6;
    margin-bottom: 6px;
    text-shadow: 0 0 4px rgba(255,43,214,0.5);
}

.film-card .name {
    font-size: 0.82rem;
    font-weight: 500;
    color: #f4ecd8;
    margin-bottom: 4px;
}

.film-card .price {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.78rem;
    color: #ffd76a;
    text-shadow: 0 0 5px rgba(255,122,0,0.5);
}

.summary-block {
    background: linear-gradient(180deg, #150933 0%, #0a0420 100%);
    border: 1px solid #2d1858;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin-top: 1rem;
    box-shadow: 0 0 18px rgba(0,229,255,0.08);
}

.empty-cart {
    color: #5a4a8a;
    font-size: 0.78rem;
    text-align: center;
    padding: 1rem 0;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-family: 'Orbitron', sans-serif;
}

div[data-testid="stButton"] button {
    background: linear-gradient(180deg, #ffd76a 0%, #ff7a00 55%, #ff2a2a 100%) !important;
    color: #0a0420 !important;
    border: none !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.12em !important;
    border-radius: 4px !important;
    width: 100%;
    padding: 0.5rem 1rem !important;
    box-shadow: 0 0 10px rgba(255,122,0,0.45);
    transition: box-shadow 0.2s, transform 0.1s;
}

div[data-testid="stButton"] button:hover {
    box-shadow: 0 0 18px rgba(255,42,42,0.7), 0 0 28px rgba(255,122,0,0.4) !important;
    transform: translateY(-1px);
}

div[data-testid="stButton"] button:active {
    transform: translateY(0);
}
</style>
""", unsafe_allow_html=True)

def _expand_cart(cart: dict) -> list:
    """Turn {film_name: qty} into a flat list of Film instances from CATALOG."""
    films = []
    for name, qty in cart.items():
        films.extend([CATALOG[name]] * qty)
    return films

def calculate_total(cart: dict) -> dict:
    films = _expand_cart(cart)
    bttf = [f for f in films if f.film_type == "bttf"]
    others = [f for f in films if f.film_type == "other"]

    bttf_subtotal_raw = sum(f.price for f in bttf)
    discount_rate = get_bttf_reduction_rate(bttf)
    bttf_discount_amount = bttf_subtotal_raw * discount_rate
    bttf_subtotal = bttf_subtotal_raw - bttf_discount_amount
    other_subtotal = sum(f.price for f in others)

    return {
        "bttf_subtotal_raw": bttf_subtotal_raw,
        "bttf_discount_rate": discount_rate,
        "bttf_discount_amount": bttf_discount_amount,
        "bttf_subtotal": bttf_subtotal,
        "other_subtotal": other_subtotal,
        "total": get_total_price(films),
    }

if "cart" not in st.session_state:
    st.session_state.cart = {}

st.markdown("""
<div class="title-block">
  <h1>DVD Cart</h1>
  <p>Back to the Future — DeLorean Video Rental · Hill Valley 1985</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Available films</div>', unsafe_allow_html=True)

cols = st.columns(len(CATALOG))
for i, (film_name, film) in enumerate(CATALOG.items()):
    with cols[i]:
        tag = "BTTF Saga" if film.film_type == "bttf" else "Other"
        card_class = "bttf" if film.film_type == "bttf" else "other"
        in_cart = film_name in st.session_state.cart

        st.markdown(f"""
        <div class="film-card {card_class}">
            <div class="tag">{tag}</div>
            <div class="name">{film_name}</div>
            <div class="price">{film.price:.0f} €</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("＋ Add", key=f"add_{film_name}"):
            st.session_state.cart[film_name] = st.session_state.cart.get(film_name, 0) + 1
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Your cart</div>', unsafe_allow_html=True)

if not st.session_state.cart:
    st.markdown('<div class="empty-cart">— cart is empty —</div>', unsafe_allow_html=True)
else:
    for film_name, qty in list(st.session_state.cart.items()):
        col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
        with col1:
            st.markdown(f"""
            <div style="font-size:0.82rem; color:#f4ecd8; padding: 6px 0;">
                {film_name}
                <span style="color:#00e5ff; font-size:0.7rem;"> × {qty}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("−", key=f"dec_{film_name}"):
                if st.session_state.cart[film_name] > 1:
                    st.session_state.cart[film_name] -= 1
                else:
                    del st.session_state.cart[film_name]
                st.rerun()
        with col3:
            if st.button("＋", key=f"inc_{film_name}"):
                st.session_state.cart[film_name] += 1
                st.rerun()
        with col4:
            if st.button("✕", key=f"del_{film_name}"):
                del st.session_state.cart[film_name]
                st.rerun()

    result = calculate_total(st.session_state.cart)
    bttf_count = sum(v for k, v in st.session_state.cart.items() if CATALOG[k].film_type == "bttf")
    discount_pct = int(result["bttf_discount_rate"] * 100)
    bttf_unit_price = next((CATALOG[k].price for k in st.session_state.cart if CATALOG[k].film_type == "bttf"), 15.0)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Order summary</div>', unsafe_allow_html=True)

    with st.container():
        if result["bttf_subtotal_raw"] > 0:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<span style='font-size:0.78rem;color:#a89cd9;font-family:IBM Plex Mono,monospace;'>BTTF ({bttf_count} × {bttf_unit_price:.0f} €)</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span style='font-size:0.78rem;color:#f4ecd8;font-family:IBM Plex Mono,monospace;float:right;'>{result['bttf_subtotal_raw']:.2f} €</span>", unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                discount_label = f"−{discount_pct}% flux discount" if discount_pct > 0 else "no discount"
                discount_color = "#00e5ff" if discount_pct > 0 else "#a89cd9"
                st.markdown(f"<span style='font-size:0.78rem;color:{discount_color};font-family:IBM Plex Mono,monospace;text-shadow:0 0 6px rgba(0,229,255,0.4);'>{discount_label}</span>", unsafe_allow_html=True)
            with col2:
                amount_str = f"−{result['bttf_discount_amount']:.2f} €" if discount_pct > 0 else "0.00 €"
                st.markdown(f"<span style='font-size:0.78rem;color:{discount_color};font-family:IBM Plex Mono,monospace;float:right;'>{amount_str}</span>", unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("<span style='font-size:0.78rem;color:#a89cd9;font-family:IBM Plex Mono,monospace;'>BTTF subtotal</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span style='font-size:0.78rem;color:#f4ecd8;font-family:IBM Plex Mono,monospace;float:right;'>{result['bttf_subtotal']:.2f} €</span>", unsafe_allow_html=True)

        if result["other_subtotal"] > 0:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("<span style='font-size:0.78rem;color:#a89cd9;font-family:IBM Plex Mono,monospace;'>Other films subtotal</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span style='font-size:0.78rem;color:#f4ecd8;font-family:IBM Plex Mono,monospace;float:right;'>{result['other_subtotal']:.2f} €</span>", unsafe_allow_html=True)

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,122,0,0.35);margin:10px 0;'>", unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("<span style='font-family:Orbitron,sans-serif;font-weight:700;font-size:1.15rem;letter-spacing:0.1em;color:#ff7a00;text-shadow:0 0 10px rgba(255,122,0,0.6);'>TOTAL</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span style='font-family:Orbitron,sans-serif;font-weight:700;font-size:1.15rem;letter-spacing:0.05em;color:#ffd76a;text-shadow:0 0 10px rgba(255,122,0,0.6);float:right;'>{result['total']:.2f} €</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Clear cart", key="clear"):
        st.session_state.cart = {}
        st.rerun()