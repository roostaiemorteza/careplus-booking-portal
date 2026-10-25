import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import urllib.parse
from datetime import datetime, date

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="CarePlus Pro | Luxury Medical & Aesthetics Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Ultra-Luxury Dark Theme & Glassmorphism Styling (Matches Concept Art)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Dark Luxury Background */
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #070d19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    
    /* Top Hero Showcase */
    .dark-hero {
        background: radial-gradient(circle at top right, rgba(14, 165, 233, 0.15), transparent 50%),
                    linear-gradient(135deg, #111c35 0%, #0d1527 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 40px;
        border-radius: 28px;
        position: relative;
        overflow: hidden;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    .dark-hero h1 {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 30%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }
    .dark-hero p {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 650px;
        line-height: 1.7;
    }
    
    /* Glowing Circular CTA Badge */
    .glow-circle-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, #0284c7 0%, #034f75 100%);
        box-shadow: 0 0 35px rgba(2, 132, 199, 0.6), inset 0 0 15px rgba(255, 255, 255, 0.3);
        border: 2px solid #38bdf8;
        color: white;
        text-align: center;
        font-weight: 700;
        font-size: 0.95rem;
        line-height: 1.3;
        margin: auto;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .glow-circle-btn:hover {
        transform: scale(1.05);
    }
    
    /* Card Glassmorphism */
    .glass-card {
        background: rgba(18, 27, 49, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 20px 35px rgba(2, 132, 199, 0.2);
    }
    .glass-card-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .glass-card-body {
        padding: 22px;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .card-doc {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 12px;
    }
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    .card-price {
        font-size: 1.35rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .badge-neon {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* KPI Glass Cards */
    .kpi-dark {
        background: rgba(18, 27, 49, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 22px;
        text-align: center;
    }
    .kpi-dark-num {
        font-size: 2.2rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 5px 0;
    }
    .kpi-dark-title {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
    }
    
    /* Stepper Header for Booking */
    .stepper-box {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background: rgba(18, 27, 49, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 15px;
        border-radius: 16px;
        margin-bottom: 25px;
    }
    .step-active {
        color: #38bdf8;
        font-weight: 700;
    }
    .step-inactive {
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Dynamic State: Treatments & Booking Database
# ---------------------------------------------------------
if "treatments_db" not in st.session_state:
    st.session_state.treatments_db = [
        {
            "id": "dental",
            "name": "Hollywood Smile / Dental (Diş Estetiği)",
            "doctors": "Dr. Ayşe Kaya, Dr. Burak Yılmaz",
            "price": 1200,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=800&q=80",
            "duration": "5 Days VIP Package",
            "tag": "Top Pick"
        },
        {
            "id": "hair",
            "name": "Sapphire FUE Hair Transplant (Saç Ekimi)",
            "doctors": "Dr. Can Çelik, Dr. Kerem Arslan",
            "price": 1800,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=800&q=80",
            "duration": "3 Days Package + Hotel",
            "tag": "All-Inclusive"
        },
        {
            "id": "aesthetics",
            "name": "Medical Aesthetics, Botox & Fillers",
            "doctors": "Dr. Elif Demir",
            "price": 450,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1512290900672-1f5bebb23cb2?auto=format&fit=crop&w=800&q=80",
            "duration": "Same Day Procedure",
            "tag": "Express"
        },
        {
            "id": "checkup",
            "name": "Executive VIP Health Check-Up",
            "doctors": "Prof. Dr. Mehmet Özkan",
            "price": 650,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80",
            "duration": "1 Full Day Diagnostic",
            "tag": "Comprehensive"
        }
    ]

if "bookings_db" not in st.session_state:
    st.session_state.bookings_db = pd.DataFrame([
        {
            "Booking ID": "CP-7011",
            "Date": "2026-10-27",
            "Time": "10:00",
            "Patient Name": "Alexander Miller",
            "Phone": "+44 7911 123456",
            "Country": "United Kingdom",
            "Treatment": "Sapphire FUE Hair Transplant (Saç Ekimi)",
            "Doctor": "Dr. Can Çelik",
            "Total Price": "EUR € 1800",
            "Status": "Confirmed",
            "VIP Transfer": "Yes"
        },
        {
            "Booking ID": "CP-7012",
            "Date": "2026-10-28",
            "Time": "11:30",
            "Patient Name": "Elena Petrova",
            "Phone": "+7 916 555 4321",
            "Country": "Russia",
            "Treatment": "Hollywood Smile / Dental (Diş Estetiği)",
            "Doctor": "Dr. Ayşe Kaya",
            "Total Price": "EUR € 1200",
            "Status": "Confirmed",
            "VIP Transfer": "Yes"
        },
        {
            "Booking ID": "CP-7013",
            "Date": "2026-10-29",
            "Time": "14:00",
            "Patient Name": "Markus Schmidt",
            "Phone": "+49 170 9876543",
            "Country": "Germany",
            "Treatment": "Executive VIP Health Check-Up",
            "Doctor": "Prof. Dr. Mehmet Özkan",
            "Total Price": "EUR € 650",
            "Status": "Pending",
            "VIP Transfer": "No"
        },
        {
            "Booking ID": "CP-7014",
            "Date": "2026-10-30",
            "Time": "16:00",
            "Patient Name": "Zeynep Korkmaz",
            "Phone": "+90 532 111 2233",
            "Country": "Türkiye",
            "Treatment": "Medical Aesthetics, Botox & Fillers",
            "Doctor": "Dr. Elif Demir",
            "Total Price": "EUR € 450",
            "Status": "Confirmed",
            "VIP Transfer": "No"
        }
    ])

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 25px;'>
            <div style='background: linear-gradient(135deg, #0284c7, #38bdf8); padding: 10px 14px; border-radius: 14px; color: white; font-size: 1.4rem;'>🩺</div>
            <div>
                <h3 style='margin: 0; font-weight: 800; font-size: 1.2rem; color: #ffffff;'>CarePlus Pro</h3>
                <span style='font-size: 0.75rem; color: #38bdf8; font-weight:600;'>Luxury Health Portal</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.selectbox("🌐 Portal Language", ["🇹🇷 Türkçe", "🇬🇧 English", "🇷🇺 Русский", "🇩🇪 Deutsch"])
    
    menu = st.radio(
        "Navigation",
        [
            "🏠 Ana Sayfa / Home Showcase",
            "📅 Online Randevu Al / Booking",
            "🔍 Randevu Takip / Query",
            "⚙️ Yönetici & CRM Paneli (Admin)"
        ]
    )
    
    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 16px; border-radius: 16px; font-size: 0.82rem;'>
            <b style='color:#38bdf8;'>🏥 Clinic Destinations:</b><br>
            • Alanya VIP Suites<br>
            • Antalya Health & Hair Resort<br>
            • Istanbul Bosphorus Clinic<br><br>
            <b style='color:#38bdf8;'>📞 24/7 International Line:</b><br>
            +90 (555) 012 34 56
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: Home Showcase (Matching Concept Art)
# ---------------------------------------------------------
if menu == "🏠 Ana Sayfa / Home Showcase":
    c_banner1, c_banner2 = st.columns([3, 1])
    with c_banner1:
        st.markdown("""
            <div class="dark-hero">
                <span class="badge-neon">✦ Award-Winning Medical Tourism Center</span>
                <h1 style='margin-top: 10px;'>CarePlus Health & Medical Tourism Portal</h1>
                <p>Your Gateway to 24/7 Online Booking & Advanced Patient Management for Dental, Hair Transplant & Aesthetics. Akredite uzman hekimlerimiz ile VIP sağlık seyahatinizi anında planlayın.</p>
            </div>
        """, unsafe_allow_html=True)
    with c_banner2:
        st.markdown("""
            <div style='padding-top: 25px;'>
                <div class="glow-circle-btn">
                    Book Your<br>Transformation
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### ⭐ Our Popular Treatments & Medical Specialists")
    st.caption("Fiyatlar, doktor kadroları ve süreler Yönetici CRM panelinden canlı olarak güncellenebilir.")
    
    treatments = st.session_state.treatments_db
    cols = st.columns(2)
    for idx, item in enumerate(treatments):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="glass-card">
                    <img src="{item['image']}" class="glass-card-img" alt="{item['name']}">
                    <div class="glass-card-body">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <div class="card-title">{item['name']}</div>
                            <span class="badge-neon">{item['tag']}</span>
                        </div>
                        <div class="card-doc">👨‍⚕️ <b>Specialists:</b> {item['doctors']}</div>
                        <div style="font-size:0.85rem; color:#64748b; margin-bottom:10px;">⏱️ {item['duration']}</div>
                        <div class="card-footer">
                            <div>
                                <span style="font-size:0.8rem; color:#94a3b8; display:block;">Package Price</span>
                                <span class="card-price">{item['currency']} {item['price']}</span>
                            </div>
                            <span style="font-size:0.85rem; color:#38bdf8; font-weight:600;">VIP Hotel & Transfer Included</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: Modern Stepper Booking Form
# ---------------------------------------------------------
elif menu == "📅 Online Randevu Al / Booking":
    st.markdown("""
        <div class="stepper-box">
            <span class="step-active">● Step 1: Tedavi & Uzman Seçimi</span>
            <span class="step-active">➔</span>
            <span class="step-active">● Step 2: Tarih & İletişim Bilgileri</span>
            <span class="step-inactive">➔</span>
            <span class="step-inactive">● Step 3: Anında Onay & Takip Kodu</span>
        </div>
    """, unsafe_allow_html=True)
    
    treatment_names = [t["name"] for t in st.session_state.treatments_db]
    
    c_form, c_summary = st.columns([2, 1])
    
    with c_form:
        st.markdown("### 📝 Hasta Bilgileri ve Randevu Talebi")
        with st.form("modern_booking_form"):
            selected_treat_name = st.selectbox("Branş / Tedavi Paketi *", treatment_names)
            selected_obj = next(t for t in st.session_state.treatments_db if t["name"] == selected_treat_name)
            
            docs = [d.strip() for d in selected_obj["doctors"].split(",")]
            selected_doc = st.selectbox("Hekim / Uzman Seçimi *", docs)
            
            col_a, col_b = st.columns(2)
            with col_a:
                p_name = st.text_input("Hasta Adı Soyadı *", placeholder="Alexander Smith / Ahmet Yılmaz")
                p_country = st.selectbox("İkamet Ülkesi *", ["United Kingdom", "Germany", "Russia", "Türkiye", "Netherlands", "Other"])
            with col_b:
                p_phone = st.text_input("WhatsApp / Telefon No *", placeholder="+44 7911 123456")
                p_date = st.date_input("Randevu Tarihi *", min_value=date.today())
                
            p_time = st.selectbox("Uygun Randevu Saati *", ["09:30", "11:00", "13:30", "15:00", "16:30", "18:00"])
            vip_transfer = st.checkbox("Havalimanı VIP Karşılama ve Transfer Paketi İstiyorum", value=True)
            patient_notes = st.text_area("Özel İstek veya Tıbbi Geçmiş Notları (Opsiyonel)", placeholder="Daha önce geçirilen operasyonlar veya alerjiler...")
            
            submit_btn = st.form_submit_button("🚀 Randevuyu Onayla ve Takip Kodunu Üret")
            
            if submit_btn:
                if not p_name or not p_phone:
                    st.error("⚠️ Lütfen İsim ve Telefon numaranızı eksiksiz doldurun.")
                else:
                    new_code = f"CP-{datetime.now().strftime('%d%H%M')}"
                    new_entry = {
                        "Booking ID": new_code,
                        "Date": str(p_date),
                        "Time": p_time,
                        "Patient Name": p_name,
                        "Phone": p_phone,
                        "Country": p_country,
                        "Treatment": selected_treat_name,
                        "Doctor": selected_doc,
                        "Total Price": f"{selected_obj['currency']} {selected_obj['price']}",
                        "Status": "Confirmed",
                        "VIP Transfer": "Yes" if vip_transfer else "No"
                    }
                    st.session_state.bookings_db = pd.concat([pd.DataFrame([new_entry]), st.session_state.bookings_db], ignore_index=True)
                    st.balloons()
                    st.success(f"🎉 Harika! Randevunuz oluşturuldu. Takip Kodunuz: **{new_code}**")
                    
    with c_summary:
        st.markdown("### 📋 Paket Özeti")
        st.markdown(f"""
            <div class="glass-card">
                <img src="{selected_obj['image']}" style="width:100%; height:140px; object-fit:cover;">
                <div style="padding:18px;">
                    <div style="font-weight:700; font-size:1.05rem; color:#fff;">{selected_obj['name']}</div>
                    <div style="font-size:0.85rem; color:#94a3b8; margin:6px 0;">⏱️ {selected_obj['duration']}</div>
                    <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:12px; margin-top:10px;">
                        <span style="font-size:0.8rem; color:#94a3b8;">Toplam Tutar:</span>
                        <div style="font-size:1.5rem; font-weight:800; color:#38bdf8;">{selected_obj['currency']} {selected_obj['price']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 3: Booking Tracker
# ---------------------------------------------------------
elif menu == "🔍 Randevu Takip / Query":
    st.markdown("### 🔍 Randevu Takip ve Doğrulama")
    st.caption("Randevu onay kodunuzu (Örn: CP-7011) girerek operasyon ve transfer durumunuzu kontrol edin.")
    
    track_code = st.text_input("Randevu Kodu Girin:", placeholder="CP-7011").strip()
    if track_code:
        df = st.session_state.bookings_db
        matched = df[df["Booking ID"].str.upper() == track_code.upper()]
        if not matched.empty:
            res = matched.iloc[0]
            st.markdown(f"""
                <div class="glass-card" style="padding:25px; border:2px solid #38bdf8;">
                    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:12px; margin-bottom:15px;">
                        <h3 style="margin:0; color:#38bdf8;">Randevu Durumu: {res['Booking ID']}</h3>
                        <span class="badge-neon">● {res['Status']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; font-size:0.95rem;">
                        <div><b>👤 Hasta:</b> {res['Patient Name']}</div>
                        <div><b>🏥 Tedavi:</b> {res['Treatment']}</div>
                        <div><b>👨‍⚕️ Doktor:</b> {res['Doctor']}</div>
                        <div><b>📅 Tarih & Saat:</b> {res['Date']} @ {res['Time']}</div>
                        <div><b>💶 Tutar:</b> {res['Total Price']}</div>
                        <div><b>🚗 VIP Transfer:</b> {res['VIP Transfer']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Bu koda ait bir randevu bulunamadı. Lütfen kontrol edip tekrar deneyiniz.")

# ---------------------------------------------------------
# VIEW 4: Admin Panel (CRM, Gauges, Dynamic Pricing & WhatsApp Dispatch)
# ---------------------------------------------------------
elif menu == "⚙️ Yönetici & CRM Paneli (Admin)":
    st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <div>
                <h2 style='margin:0; font-weight:800; color:#fff;'>⚙️ CarePlus Pro Admin & CRM Control Hub</h2>
                <p style='color:#94a3b8; margin:4px 0 0 0;'>Tüm hasta akışını, doktor ücretlerini ve onay süreçlerini anlık yönetin.</p>
            </div>
            <span class="badge-neon">⚡ Live Operation Mode</span>
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.bookings_db
    total_count = len(df)
    confirmed_count = len(df[df["Status"] == "Confirmed"])
    completion_rate = int((confirmed_count / total_count * 100)) if total_count > 0 else 0
    
    # Concept Art Gauges (Top Row)
    g_col1, g_col2, g_col3 = st.columns(3)
    
    with g_col1:
        fig_g1 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_count,
            title = {'text': "Bookings This Week", 'font': {'size': 14, 'color': '#94a3b8'}},
            gauge = {
                'axis': {'range': [0, max(15, total_count + 5)], 'tickcolor': '#38bdf8'},
                'bar': {'color': '#38bdf8'},
                'bgcolor': "rgba(255,255,255,0.05)"
            }
        ))
        fig_g1.update_layout(height=160, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_g1, use_container_width=True)
        
    with g_col2:
        fig_g2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confirmed_count,
            title = {'text': "Patient Consultations (Confirmed)", 'font': {'size': 14, 'color': '#94a3b8'}},
            gauge = {
                'axis': {'range': [0, max(15, total_count + 5)], 'tickcolor': '#10b981'},
                'bar': {'color': '#10b981'},
                'bgcolor': "rgba(255,255,255,0.05)"
            }
        ))
        fig_g2.update_layout(height=160, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_g2, use_container_width=True)

    with g_col3:
        fig_g3 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = completion_rate,
            number = {'suffix': "%"},
            title = {'text': "Treatment Completion Rate", 'font': {'size': 14, 'color': '#94a3b8'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': '#f59e0b'},
                'bar': {'color': '#f59e0b'},
                'bgcolor': "rgba(255,255,255,0.05)"
            }
        ))
        fig_g3.update_layout(height=160, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_g3, use_container_width=True)

    # Admin Tabs
    t1, t2, t3 = st.tabs([
        "📋 Hasta Listesi & Sipariş Kabulü (CRM)",
        "🛠️ Tedavi, Doktor & Fiyat Ayarları",
        "➕ Yeni Paket / Servis Tanımla"
    ])
    
    # TAB 1: CRM & Order Approval
    with t1:
        st.markdown("#### Canlı Hasta Randevu Listesi")
        st.caption("Hasta durumunu değiştirdikten sonra 'Değişiklikleri Kaydet' butonuna basınız.")
        
        edited_table = st.data_editor(
            st.session_state.bookings_db,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Sipariş Durumu",
                    options=["Confirmed", "Pending", "Completed", "Cancelled"],
                    help="Randevuyu onaylamak veya tamamlamak için seçin"
                )
            }
        )
        
        btn_c1, btn_c2 = st.columns([1, 4])
        with btn_c1:
            if st.button("💾 Değişiklikleri Kaydet"):
                st.session_state.bookings_db = edited_table
                st.success("Tüm değişiklikler başarıyla kaydedildi!")
        with btn_c2:
            out = io.BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as wr:
                edited_table.to_excel(wr, index=False)
            st.download_button(
                "📥 Excel Raporu Al (.xlsx)",
                data=out.getvalue(),
                file_name="CarePlus_Hasta_Veritabani.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        st.markdown("---")
        st.markdown("#### 💬 Hastaya Tek Tıkla WhatsApp Onay Mesajı Gönder")
        selected_patient = st.selectbox("Mesaj Gönderilecek Hasta:", df["Patient Name"].tolist())
        p_row = df[df["Patient Name"] == selected_patient].iloc[0]
        
        clean_phone = "".join(filter(str.isdigit, str(p_row['Phone'])))
        msg = f"Merhaba {p_row['Patient Name']}, CarePlus kliniğimizden {p_row['Treatment']} randevunuz ({p_row['Date']} @ {p_row['Time']}) onaylanmıştır. Takip Kodunuz: {p_row['Booking ID']}."
        encoded_msg = urllib.parse.quote(msg)
        wa_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
        
        st.markdown(f'<a href="{wa_url}" target="_blank" style="background:#25D366; color:white; padding:10px 20px; border-radius:12px; text-decoration:none; font-weight:700; display:inline-block;">📲 {p_row["Patient Name"]} İçin WhatsApp Aç</a>', unsafe_allow_html=True)

    # TAB 2: Dynamic Pricing & Doctors
    with t2:
        st.markdown("#### 🛠️ Mevcut Tedavileri, Doktorları ve Fiyatları Düzenle")
        for idx, item in enumerate(st.session_state.treatments_db):
            with st.expander(f"🔹 {item['name']} - ({item['currency']} {item['price']})", expanded=False):
                col_u1, col_u2 = st.columns([2, 1])
                with col_u1:
                    new_n = st.text_input("Tedavi Adı", value=item["name"], key=f"t_name_{idx}")
                    new_d = st.text_input("Doktorlar (Virgülle ayırın)", value=item["doctors"], key=f"t_doc_{idx}")
                    new_dur = st.text_input("Paket Süresi / Açıklama", value=item["duration"], key=f"t_dur_{idx}")
                with col_u2:
                    new_p = st.number_input("Paket Fiyatı", value=int(item["price"]), step=50, key=f"t_p_{idx}")
                    new_c = st.selectbox("Para Birimi", ["EUR €", "USD $", "TRY ₺", "GBP £"], 
                                         index=["EUR €", "USD $", "TRY ₺", "GBP £"].index(item.get("currency", "EUR €")), 
                                         key=f"t_c_{idx}")
                    new_tg = st.text_input("Etiket / Rozet", value=item["tag"], key=f"t_tag_{idx}")
                
                if st.button(f"Paketi Güncelle ({item['id']})", key=f"btn_save_{idx}"):
                    st.session_state.treatments_db[idx]["name"] = new_n
                    st.session_state.treatments_db[idx]["doctors"] = new_d
                    st.session_state.treatments_db[idx]["duration"] = new_dur
                    st.session_state.treatments_db[idx]["price"] = new_p
                    st.session_state.treatments_db[idx]["currency"] = new_c
                    st.session_state.treatments_db[idx]["tag"] = new_tg
                    st.success("Bilgiler güncellendi! Ana sayfa ve form anında senkronize edildi.")
                    st.rerun()

    # TAB 3: Add New Package
    with t3:
        st.markdown("#### ➕ Yeni Bir Tedavi Paketi & Doktor Grubu Ekle")
        with st.form("add_new_treatment_form"):
            add_name = st.text_input("Yeni Tedavi / Paket Adı (Örn: Rhinoplasty / Burun Estetiği)")
            add_docs = st.text_input("Görevli Doktor(lar) (Örn: Op. Dr. Hakan Yıldız)")
               add_dur = st.text_input("Tedavi Süresi (Örn: 3 Gün)", "3 Gün")

