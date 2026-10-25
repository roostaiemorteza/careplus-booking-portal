import streamlit as st
import pandas as pd
import plotly.express as px
import io
from datetime import datetime, date

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="CarePlus | International Health & Clinic Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Ultra-Modern Medical Theme & CSS Injection
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Modern Background & Container */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef5f9 100%);
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #0f172a 100%);
        padding: 40px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px -15px rgba(3, 105, 161, 0.35);
        position: relative;
        overflow: hidden;
    }
    .hero-banner h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .hero-banner p {
        font-size: 1.05rem;
        opacity: 0.9;
        max-width: 650px;
        line-height: 1.6;
        margin-bottom: 0px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 14px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Medical Treatment Cards */
    .treatment-card {
        background: #ffffff;
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 25px;
    }
    .treatment-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 35px -8px rgba(2, 132, 199, 0.18);
        border-color: #38bdf8;
    }
    .treatment-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .treatment-body {
        padding: 20px;
    }
    .treatment-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
    }
    .treatment-doctor {
        font-size: 0.88rem;
        color: #64748b;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .treatment-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #f1f5f9;
        padding-top: 12px;
        margin-top: 6px;
    }
    .treatment-price {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0284c7;
    }
    .tag-badge {
        background: #e0f2fe;
        color: #0369a1;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 15px;
    }
    .kpi-num {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0284c7;
        margin: 4px 0;
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Primary Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Dynamic Database / Session State Setup
# ---------------------------------------------------------
if "treatments_db" not in st.session_state:
    st.session_state.treatments_db = [
        {
            "id": "dental",
            "name": "Hollywood Smile / Dental Estetik",
            "doctors": "Dt. Ayşe Kaya, Dt. Burak Yılmaz",
            "price": 1250,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=800&q=80",
            "duration": "5 Days Package",
            "tag": "High Demand"
        },
        {
            "id": "hair",
            "name": "Sapphire FUE Hair Transplant (Saç Ekimi)",
            "doctors": "Dr. Can Çelik, Dr. Kerem Arslan",
            "price": 1850,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=800&q=80",
            "duration": "3 Days Package (VIP Transfer Included)",
            "tag": "All Inclusive"
        },
        {
            "id": "aesthetics",
            "name": "Medical Aesthetics & Botox (Medikal Estetik)",
            "doctors": "Dr. Elif Demir, Dr. Selin Doğan",
            "price": 450,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1512290900672-1f5bebb23cb2?auto=format&fit=crop&w=800&q=80",
            "duration": "Same Day Procedure",
            "tag": "Instant Result"
        },
        {
            "id": "checkup",
            "name": "Full Body Executive VIP Check-Up",
            "doctors": "Prof. Dr. Mehmet Özkan",
            "price": 650,
            "currency": "EUR €",
            "image": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80",
            "duration": "1 Full Day Comprehensive",
            "tag": "Preventive Care"
        }
    ]

if "bookings_db" not in st.session_state:
    st.session_state.bookings_db = pd.DataFrame([
        {
            "Booking ID": "CP-1011",
            "Date": "2026-10-27",
            "Time": "10:00",
            "Patient Name": "Alexander Miller",
            "Phone": "+44 7911 123456",
            "Country": "United Kingdom",
            "Treatment": "Sapphire FUE Hair Transplant (Saç Ekimi)",
            "Doctor": "Dr. Can Çelik",
            "Total Price": "€1850",
            "Status": "Confirmed",
            "VIP Transfer": "Yes (Antalya Airport)"
        },
        {
            "Booking ID": "CP-1012",
            "Date": "2026-10-28",
            "Time": "11:30",
            "Patient Name": "Elena Petrova",
            "Phone": "+7 916 555 4321",
            "Country": "Russia",
            "Treatment": "Hollywood Smile / Dental Estetik",
            "Doctor": "Dt. Ayşe Kaya",
            "Total Price": "€1250",
            "Status": "Confirmed",
            "VIP Transfer": "Yes (Gazipaşa-Alanya Airport)"
        },
        {
            "Booking ID": "CP-1013",
            "Date": "2026-10-29",
            "Time": "14:00",
            "Patient Name": "Markus Schmidt",
            "Phone": "+49 170 9876543",
            "Country": "Germany",
            "Treatment": "Full Body Executive VIP Check-Up",
            "Doctor": "Prof. Dr. Mehmet Özkan",
            "Total Price": "€650",
            "Status": "Pending",
            "VIP Transfer": "No"
        },
        {
            "Booking ID": "CP-1014",
            "Date": "2026-10-30",
            "Time": "15:30",
            "Patient Name": "Zeynep Korkmaz",
            "Phone": "+90 532 111 2233",
            "Country": "Türkiye",
            "Treatment": "Medical Aesthetics & Botox (Medikal Estetik)",
            "Doctor": "Dr. Elif Demir",
            "Total Price": "€450",
            "Status": "Confirmed",
            "VIP Transfer": "No"
        }
    ])

# ---------------------------------------------------------
# Sidebar Navigation & Multilingual Support
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px;'>
            <div style='background: #0284c7; padding: 10px; border-radius: 12px; color: white; font-size: 1.5rem;'>🩺</div>
            <div>
                <h3 style='margin: 0; font-weight: 800; font-size: 1.25rem; color: #0f172a;'>CarePlus Pro</h3>
                <span style='font-size: 0.78rem; color: #64748b;'>Clinic & Medical Tourism Portal</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    lang = st.selectbox(
        "🌐 Language / Dil / Язык / Sprache",
        ["🇹🇷 Türkçe", "🇬🇧 English", "🇷🇺 Русский", "🇩🇪 Deutsch"]
    )
    
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        [
            "🏠 Ana Sayfa / Home",
            "📅 Online Randevu Al / Book",
            "🔍 Randevu Sorgula / Track",
            "⚙️ Yönetici & Fiyat Paneli (Admin)"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
        <div style='background: #f1f5f9; padding: 15px; border-radius: 14px; font-size: 0.82rem; color: #475569;'>
            <b>📍 Clinic Locations:</b><br>
            • Alanya Medical Suites<br>
            • Antalya Health Hub<br>
            • Istanbul International Center<br>
            <br>
            <b>📞 7/24 WhatsApp Concierge:</b><br>
            +90 (555) 012 34 56
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: Home Page (Showcase Treatments & Services)
# ---------------------------------------------------------
if menu == "🏠 Ana Sayfa / Home":
    st.markdown("""
        <div class="hero-banner">
            <span class="hero-badge">✦ Award-Winning Medical Tourism in Turkey</span>
            <h1>CarePlus Health & Medical Tourism Portal</h1>
            <p>Dünya standartlarında akredite kliniklerimiz, uzman cerrahlarımız ve 7/24 VIP hasta karşılama hizmetimizle sağlığınıza ve gülüşünüze değer katıyoruz.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⭐ Popüler Tedavi Paketlerimiz & Uzmanlarımız")
    st.caption("Fiyatlar, doktor kadroları ve paketler Yönetici Panelinden canlı olarak güncellenebilir.")
    
    treatments = st.session_state.treatments_db
    cols = st.columns(2)
    
    for idx, item in enumerate(treatments):
        col = cols[idx % 2]
        with col:
            st.markdown(f"""
                <div class="treatment-card">
                    <img src="{item['image']}" class="treatment-img" alt="{item['name']}">
                    <div class="treatment-body">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div class="treatment-title">{item['name']}</div>
                            <span class="tag-badge">{item['tag']}</span>
                        </div>
                        <div class="treatment-doctor">👨‍⚕️ <b>Doktorlar:</b> {item['doctors']}</div>
                        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 8px;">⏱️ Paket Süresi: {item['duration']}</div>
                        <div class="treatment-footer">
                            <span class="treatment-price">{item['currency']} {item['price']}</span>
                            <span style="font-size: 0.8rem; color: #0284c7; font-weight: 600;">Otel & VIP Transfer Dahil</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: Online Booking Form
# ---------------------------------------------------------
elif menu == "📅 Online Randevu Al / Book":
    st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 30px; border: 1px solid #e2e8f0; margin-bottom: 25px;'>
            <h2 style='margin:0; font-weight: 800; color: #0f172a;'>📅 Online Randevu & VIP Konsültasyon Formu</h2>
            <p style='color: #64748b; margin-top: 5px;'>Lütfen bilgilerinizi eksiksiz doldurunuz. Randevunuz anında sisteme kaydedilecek ve takip kodunuz üretilecektir.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Treatment Options from dynamic state
    treatment_names = [t["name"] for t in st.session_state.treatments_db]
    
    with st.form("booking_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            selected_treatment_name = st.selectbox("Tedavi / Branş Seçiniz *", treatment_names)
            # Find selected treatment object
            selected_obj = next(t for t in st.session_state.treatments_db if t["name"] == selected_treatment_name)
            
            # Split doctors
            doc_list = [d.strip() for d in selected_obj["doctors"].split(",")]
            selected_doctor = st.selectbox("Tercih Edilen Doktor / Uzman *", doc_list)
            full_name = st.text_input("Hasta Adı Soyadı *", placeholder="Örn: Alexey Smirnov / Ahmet Yılmaz")
            phone = st.text_input("WhatsApp / Telefon Numarası *", placeholder="+90 5XX XXX XX XX veya +7 9XX XXX XX XX")
            
        with c2:
            pref_date = st.date_input("Randevu Tarihi *", min_value=date.today())
            pref_time = st.selectbox("Randevu Saati *", ["09:00", "10:30", "12:00", "14:00", "15:30", "17:00"])
            country = st.selectbox("İkamet Ettiğiniz Ülke *", ["Türkiye", "Germany / Deutschland", "United Kingdom", "Russia / Россия", "Other"])
            vip_transfer = st.checkbox("Havalimanı VIP Transfer ve Otel Rezervasyonu İstiyorum (+Ücretsiz Konsültasyon)", value=True)
            notes = st.text_area("Özel İstekler / Tıbbi Geçmiş Notları (Opsiyonel)", placeholder="Daha önce operasyon geçirdiniz mi? Özel bir sağlık durumunuz var mı?")

        # Price preview box
        st.markdown(f"""
            <div style='background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 15px; margin: 15px 0; display:flex; justify-content: space-between; align-items:center;'>
                <span style='font-size: 0.95rem; color: #166534; font-weight: 600;'>💶 Tahmini Paket Tutarı:</span>
                <span style='font-size: 1.4rem; color: #166534; font-weight: 800;'>{selected_obj['currency']} {selected_obj['price']}</span>
            </div>
        """, unsafe_allow_html=True)

        submit = st.form_submit_button("✅ Randevuyu Onayla ve Takip Kodu Al")
        
        if submit:
            if not full_name or not phone:
                st.error("⚠️ Lütfen adınızı ve telefon numaranızı eksiksiz giriniz.")
            else:
                new_id = f"CP-{datetime.now().strftime('%d%H%M')}"
                new_row = {
                    "Booking ID": new_id,
                    "Date": str(pref_date),
                    "Time": pref_time,
                    "Patient Name": full_name,
                    "Phone": phone,
                    "Country": country,
                    "Treatment": selected_treatment_name,
                    "Doctor": selected_doctor,
                    "Total Price": f"{selected_obj['currency']} {selected_obj['price']}",
                    "Status": "Confirmed",
                    "VIP Transfer": "Yes" if vip_transfer else "No"
                }
                st.session_state.bookings_db = pd.concat([pd.DataFrame([new_row]), st.session_state.bookings_db], ignore_index=True)
                st.balloons()
                st.success(f"🎉 Tebrikler! Randevunuz başarıyla oluşturuldu. Takip Kodunuz: **{new_id}**")
                st.info("Bu kod ile randevu durumunuzu 'Randevu Sorgula' sekmesinden dilediğiniz an takip edebilirsiniz.")

# ---------------------------------------------------------
# VIEW 3: Booking Tracker
# ---------------------------------------------------------
elif menu == "🔍 Randevu Sorgula / Track":
    st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 30px; border: 1px solid #e2e8f0; margin-bottom: 25px;'>
            <h2 style='margin:0; font-weight: 800; color: #0f172a;'>🔍 Hasta Randevu Durumu Sorgulama</h2>
            <p style='color: #64748b;'>Randevu onay kodunuzu (örn: CP-1011) girerek randevu detaylarını ve transfer durumunuzu görüntüleyebilirsiniz.</p>
        </div>
    """, unsafe_allow_html=True)
    
    code = st.text_input("Randevu Takip Kodu (Booking Reference):", placeholder="CP-1011").strip()
    if code:
        df = st.session_state.bookings_db
        matched = df[df["Booking ID"].str.upper() == code.upper()]
        if not matched.empty:
            item = matched.iloc[0]
            st.markdown(f"""
                <div style='background: white; border-radius: 20px; border: 2px solid #0284c7; padding: 25px; box-shadow: 0 10px 30px rgba(2, 132, 199, 0.1);'>
                    <div style='display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 15px;'>
                        <h3 style='margin:0; color:#0284c7;'>Randevu Detayları - {item['Booking ID']}</h3>
                        <span style='background:#dcfce7; color:#15803d; font-weight:700; padding:6px 14px; border-radius:20px;'>● {item['Status']}</span>
                    </div>
                    <div style='display:grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 0.95rem;'>
                        <div><b>👤 Hasta:</b> {item['Patient Name']}</div>
                        <div><b>🏥 Branş:</b> {item['Treatment']}</div>
                        <div><b>👨‍⚕️ Doktor:</b> {item['Doctor']}</div>
                        <div><b>📅 Tarih & Saat:</b> {item['Date']} @ {item['Time']}</div>
                        <div><b>💶 Tutar:</b> {item['Total Price']}</div>
                        <div><b>🚗 VIP Transfer:</b> {item['VIP Transfer']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Bu koda ait bir randevu bulunamadı. Lütfen kontrol edip tekrar deneyiniz.")

# ---------------------------------------------------------
# VIEW 4: Admin Panel & Settings (Dynamic Clinic Management)
# ---------------------------------------------------------
elif menu == "⚙️ Yönetici & Fiyat Paneli (Admin)":
    st.markdown("""
        <div style='background: white; border-radius: 20px; padding: 25px; border: 1px solid #e2e8f0; margin-bottom: 25px; display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <h2 style='margin:0; font-weight: 800; color: #0f172a;'>⚙️ CarePlus Clinic CRM & Fiyat Yönetim Paneli</h2>
                <p style='color: #64748b; margin: 4px 0 0 0;'>Tüm hasta kayıtlarını, doktor atamalarını ve tedavi ücretlerini anlık olarak yönetin.</p>
            </div>
            <span style='background: #e0f2fe; color: #0369a1; padding: 8px 16px; border-radius: 30px; font-weight: 700; font-size: 0.85rem;'>Admin Modu Aktif</span>
        </div>
    """, unsafe_allow_html=True)
    
    # KPIs Top Row
    df = st.session_state.bookings_db
    total_bookings = len(df)
    confirmed_count = len(df[df["Status"] == "Confirmed"])
    est_revenue = f"€{total_bookings * 1150:,}"
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Toplam Başvuru</div>
                <div class="kpi-num">{total_bookings}</div>
                <span style="color:#16a34a; font-size:0.8rem; font-weight:600;">↑ 18% Bu Hafta</span>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Onaylanan Randevular</div>
                <div class="kpi-num">{confirmed_count}</div>
                <span style="color:#0284c7; font-size:0.8rem; font-weight:600;">Yüksek Doluluk</span>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Tahmini Ciro Hacmi</div>
                <div class="kpi-num">{est_revenue}</div>
                <span style="color:#16a34a; font-size:0.8rem; font-weight:600;">Medikal Turizm</span>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Aktif Doktor Sayısı</div>
                <div class="kpi-num">8</div>
                <span style="color:#64748b; font-size:0.8rem; font-weight:600;">4 Klinik Branşı</span>
            </div>
        """, unsafe_allow_html=True)
        
    # Tabs for CRM vs Dynamic Treatment Settings
    tab1, tab2, tab3 = st.tabs([
        "📋 Hasta Kayıtları & CRM Tablosu", 
        "🛠️ Tedavi, Doktor & Fiyat Ayarları", 
        "📊 İstatistik ve Analiz Raporları"
    ])
    
    # TAB 1: CRM Table & Edit
    with tab1:
        st.markdown("#### Canlı Hasta Listesi (Düzenlenebilir Tablo)")
        edited_df = st.data_editor(
            st.session_state.bookings_db,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Status": st.column_config.SelectboxColumn("Durum", options=["Confirmed", "Pending", "Completed", "Cancelled"])
            }
        )
        
        c_btn1, c_btn2 = st.columns([1, 4])
        with c_btn1:
            if st.button("💾 Değişiklikleri Kaydet"):
                st.session_state.bookings_db = edited_df
                st.success("Tüm değişiklikler kaydedildi!")
        with c_btn2:
            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='Bookings')
            st.download_button(
                label="📥 Excel Olarak İndir (.xlsx)",
                data=output.getvalue(),
                file_name="CarePlus_Hasta_Listesi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # TAB 2: Dynamic Management of Doctors, Pricing, Currency
    with tab2:
        st.markdown("#### 🛠️ Tedavi Paketleri, Doktor Kadroları ve Fiyatları Güncelleyin")
        st.caption("Burada yaptığınız değişiklikler ana sayfadaki kartlara ve randevu formundaki seçeneklere otomatik yansır.")
        
        for idx, treat in enumerate(st.session_state.treatments_db):
            with st.expander(f"🔹 {treat['name']} (Şu Anki Fiyat: {treat['currency']} {treat['price']})", expanded=False):
                tc1, tc2 = st.columns([2, 1])
                with tc1:
                    new_name = st.text_input(f"Tedavi / Paket Adı #{idx+1}", value=treat["name"], key=f"name_{idx}")
                    new_docs = st.text_input(f"Doktor Kadrosu (Virgülle ayırın) #{idx+1}", value=treat["doctors"], key=f"docs_{idx}")
                    new_dur = st.text_input(f"Paket Süresi / Açıklama #{idx+1}", value=treat["duration"], key=f"dur_{idx}")
                with tc2:
                    new_price = st.number_input(f"Paket Fiyatı #{idx+1}", value=int(treat["price"]), step=50, key=f"price_{idx}")
                    new_curr = st.selectbox(f"Para Birimi #{idx+1}", ["EUR €", "USD $", "TRY ₺", "GBP £"], 
                                           index=["EUR €", "USD $", "TRY ₺", "GBP £"].index(treat.get("currency", "EUR €")), 
                                           key=f"curr_{idx}")
                    new_tag = st.text_input(f"Etiket Rozeti #{idx+1}", value=treat["tag"], key=f"tag_{idx}")
                
                if st.button(f"Güncellemeleri Kaydet ({treat['id']})", key=f"save_treat_{idx}"):
                    st.session_state.treatments_db[idx]["name"] = new_name
                    st.session_state.treatments_db[idx]["doctors"] = new_docs
                    st.session_state.treatments_db[idx]["duration"] = new_dur
                    st.session_state.treatments_db[idx]["price"] = new_price
                    st.session_state.treatments_db[idx]["currency"] = new_curr
                    st.session_state.treatments_db[idx]["tag"] = new_tag
                    st.success(f"{new_name} paketi başarıyla güncellendi! Ana sayfayı kontrol edebilirsiniz.")
                    st.rerun()

    # TAB 3: Visual Analytics
    with tab3:
        st.markdown("#### 📊 Klinik Performans Grafikleri")
        g1, g2 = st.columns(2)
        with g1:
            fig1 = px.pie(
                df, 
                names="Treatment", 
                title="Tedavi Branşlarına Göre Başvuru Dağılımı",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig1.update_layout(margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig1, use_container_width=True)
            
        with g2:
            fig2 = px.histogram(
                df, 
                x="Country", 
                color="Status", 
                barmode="group",
                title="Ülkelere Göre Hasta Kökenleri",
                color_discrete_sequence=['#0284c7', '#38bdf8', '#94a3b8']
            )
            fig2.update_layout(margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig2, use_container_width=True)
