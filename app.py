import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import random
from io import BytesIO
from streamlit_option_menu import option_menu

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CarePlus | Clinic & Medical Tourism Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- RESPONSIVE & MODERN CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .hero-box {
        background: linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%);
        color: white;
        padding: 2.2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(13, 110, 253, 0.18);
    }
    .service-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .service-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    .kpi-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 14px;
        padding: 1.2rem;
        border-left: 5px solid #0d6efd;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .kpi-title { font-size: 0.9rem; color: #6c757d; font-weight: 600; }
    .kpi-value { font-size: 1.8rem; color: #212529; font-weight: 700; margin-top: 4px; }
    
    @media (max-width: 768px) {
        .hero-box { padding: 1.3rem; }
        .kpi-value { font-size: 1.4rem; }
    }
</style>
""", unsafe_allow_html=True)

# --- MULTI-LANGUAGE DICTIONARY (TR Default, EN, RU, DE) ---
TRANSLATIONS = {
    "🇹🇷 Türkçe": {
        "lang_code": "TR",
        "menu_title": "CarePlus Menü",
        "nav": ["Ana Sayfa", "Randevu Al", "Randevu Sorgula", "Yönetici Paneli"],
        "hero_title": "CarePlus Sağlık & Medikal Turizm Portalı",
        "hero_sub": "Diş Estetiği, Saç Ekimi ve Medikal Estetik için 7/24 Online Randevu ve Hasta Yönetim Sistemi.",
        "services_title": "🌟 Popüler Tedavilerimiz ve Uzmanlarımız",
        "book_title": "📅 Online Randevu Oluştur",
        "book_desc": "Lütfen bilgilerinizi eksiksiz doldurun. Anında onay kodunuz oluşturulacaktır.",
        "name": "Adınız Soyadınız *",
        "phone": "Telefon / WhatsApp Numaranız *",
        "email": "E-Posta Adresiniz",
        "country": "Ülke / Şehir",
        "service": "Hizmet / Bölüm Seçiniz",
        "doctor": "Doktor / Uzman Seçiniz",
        "date": "Randevu Tarihi",
        "time": "Randevu Saati",
        "notes": "Özel Notunuz (VIP Transfer, Otel Talebi vb.)",
        "submit": "✅ Randevuyu Onayla ve Kaydet",
        "success_msg": "🎉 Randevunuz başarıyla oluşturuldu! Takip Kodunuz:",
        "error_msg": "⚠️ Lütfen Ad Soyad ve Telefon alanlarını doldurunuz.",
        "slot_taken": "❌ Seçtiğiniz doktor için bu tarih ve saat dolu! Lütfen başka bir saat seçiniz.",
        "track_title": "🔍 Randevu Durumu Sorgula",
        "track_input": "Takip Kodunuzu (Örn: CP-1024) veya Telefon Numaranızı Girin",
        "track_btn": "Sorgula",
        "track_not_found": "Kayıt bulunamadı. Lütfen bilgilerinizi kontrol edin.",
        "admin_title": "⚙️ Klinik Yönetim & CRM Paneli",
        "kpi_total": "Toplam Randevu",
        "kpi_confirmed": "Onaylanan",
        "kpi_pending": "Bekleyen",
        "kpi_revenue": "Tahmini Gelir (€)",
        "admin_table": "📋 Tüm Randevular (Durumu tabloda çift tıklayarak değiştirebilirsiniz)",
        "save_changes": "💾 Değişiklikleri Kaydet",
        "saved_toast": "Değişiklikler başarıyla kaydedildi!",
        "export_excel": "📥 Excel Olarak İndir (.xlsx)",
        "chart_dept": "Bölümlere Göre Randevu Dağılımı",
        "chart_status": "Randevu Durum Analizi"
    },
    "🇬🇧 English": {
        "lang_code": "EN",
        "menu_title": "CarePlus Menu",
        "nav": ["Home", "Book Appointment", "Track Booking", "Admin Panel"],
        "hero_title": "CarePlus Health & Medical Tourism Portal",
        "hero_sub": "24/7 Online Booking & Patient Management System for Dental, Hair Transplant & Aesthetics.",
        "services_title": "🌟 Our Popular Treatments & Specialists",
        "book_title": "📅 Book an Online Appointment",
        "book_desc": "Please fill in your details below. Your instant tracking code will be generated.",
        "name": "Full Name *",
        "phone": "Phone / WhatsApp Number *",
        "email": "Email Address",
        "country": "Country / City",
        "service": "Select Department / Treatment",
        "doctor": "Select Doctor / Specialist",
        "date": "Preferred Date",
        "time": "Preferred Time",
        "notes": "Special Notes (VIP Airport Transfer, Hotel Request, etc.)",
        "submit": "✅ Confirm & Book Appointment",
        "success_msg": "🎉 Your appointment is booked! Your Tracking Code:",
        "error_msg": "⚠️ Please fill in both Full Name and Phone fields.",
        "slot_taken": "❌ This time slot is already booked for the selected specialist! Please pick another time.",
        "track_title": "🔍 Track Your Appointment",
        "track_input": "Enter your Tracking Code (e.g., CP-1024) or Phone Number",
        "track_btn": "Search",
        "track_not_found": "No booking found. Please check your code or phone number.",
        "admin_title": "⚙️ Clinic Management & CRM Dashboard",
        "kpi_total": "Total Bookings",
        "kpi_confirmed": "Confirmed",
        "kpi_pending": "Pending",
        "kpi_revenue": "Est. Revenue (€)",
        "admin_table": "📋 All Appointments (Double-click 'Status' cell to update)",
        "save_changes": "💾 Save Changes",
        "saved_toast": "Changes saved successfully!",
        "export_excel": "📥 Export to Excel (.xlsx)",
        "chart_dept": "Appointments by Department",
        "chart_status": "Booking Status Breakdown"
    },
    "🇷🇺 Русский": {
        "lang_code": "RU",
        "menu_title": "Меню CarePlus",
        "nav": ["Главная", "Записаться", "Проверка записи", "Панель Админа"],
        "hero_title": "Портал здоровья и медтуризма CarePlus",
        "hero_sub": "Онлайн-запись 24/7: стоматология, пересадка волос и эстетическая медицина в Турции.",
        "services_title": "🌟 Популярные процедуры и специалисты",
        "book_title": "📅 Онлайн-запись на прием",
        "book_desc": "Заполните форму ниже. Вы мгновенно получите код отслеживания.",
        "name": "Имя и Фамилия *",
        "phone": "Телефон / WhatsApp *",
        "email": "Электронная почта",
        "country": "Страна / Город",
        "service": "Выберите отделение / процедуру",
        "doctor": "Выберите врача",
        "date": "Дата приема",
        "time": "Время приема",
        "notes": "Примечания (VIP-трансфер, отель, переводчик)",
        "submit": "✅ Подтвердить запись",
        "success_msg": "🎉 Ваша запись успешно создана! Код отслеживания:",
        "error_msg": "⚠️ Пожалуйста, укажите Имя и Телефон.",
        "slot_taken": "❌ Это время уже занято у выбранного врача! Выберите другое время.",
        "track_title": "🔍 Проверить статус записи",
        "track_input": "Введите код записи (напр. CP-1024) или номер телефона",
        "track_btn": "Найти",
        "track_not_found": "Запись не найдена. Проверьте введенные данные.",
        "admin_title": "⚙️ Панель управления клиникой (CRM)",
        "kpi_total": "Всего записей",
        "kpi_confirmed": "Подтверждено",
        "kpi_pending": "В ожидании",
        "kpi_revenue": "Ожид. доход (€)",
        "admin_table": "📋 Все записи (Дважды кликните по статусу для изменения)",
        "save_changes": "💾 Сохранить изменения",
        "saved_toast": "Изменения успешно сохранены!",
        "export_excel": "📥 Скачать Excel (.xlsx)",
        "chart_dept": "Записи по отделениям",
        "chart_status": "Статус записей"
    },
    "🇩🇪 Deutsch": {
        "lang_code": "DE",
        "menu_title": "CarePlus Menü",
        "nav": ["Startseite", "Termin Buchen", "Termin Prüfen", "Admin-Bereich"],
        "hero_title": "CarePlus Gesundheits- & Medizintourismus-Portal",
        "hero_sub": "24/7 Online-Terminbuchung für Zahnästhetik, Haartransplantation und Schönheitschirurgie.",
        "services_title": "🌟 Unsere Behandlungen & Spezialisten",
        "book_title": "📅 Online-Termin vereinbaren",
        "book_desc": "Bitte füllen Sie das Formular aus. Sie erhalten sofort Ihren Tracking-Code.",
        "name": "Vor- und Nachname *",
        "phone": "Telefon / WhatsApp Nummer *",
        "email": "E-Mail-Adresse",
        "country": "Land / Stadt",
        "service": "Abteilung / Behandlung wählen",
        "doctor": "Arzt / Spezialist wählen",
        "date": "Wunschdatum",
        "time": "Wunschuhrzeit",
        "notes": "Besondere Wünsche (VIP-Transfer, Hotel, Dolmetscher)",
        "submit": "✅ Termin verbindlich buchen",
        "success_msg": "🎉 Ihr Termin wurde erfolgreich gebucht! Ihr Tracking-Code:",
        "error_msg": "⚠️ Bitte füllen Sie Name und Telefonnummer aus.",
        "slot_taken": "❌ Dieser Zeitpunkt ist beim gewählten Arzt bereits vergeben!",
        "track_title": "🔍 Terminstatus abfragen",
        "track_input": "Tracking-Code (z.B. CP-1024) oder Telefonnummer eingeben",
        "track_btn": "Suchen",
        "track_not_found": "Kein Eintrag gefunden. Bitte überprüfen Sie Ihre Eingabe.",
        "admin_title": "⚙️ Klinik-Management & CRM-Dashboard",
        "kpi_total": "Termine Gesamt",
        "kpi_confirmed": "Bestätigt",
        "kpi_pending": "Ausstehend",
        "kpi_revenue": "Geschätzter Umsatz (€)",
        "admin_table": "📋 Alle Termine (Doppelklick auf 'Status' zum Ändern)",
        "save_changes": "💾 Änderungen speichern",
        "saved_toast": "Änderungen erfolgreich gespeichert!",
        "export_excel": "📥 Als Excel herunterladen (.xlsx)",
        "chart_dept": "Termine nach Abteilung",
        "chart_status": "Buchungsstatus"
    }
}

# --- DEPARTMENTS, DOCTORS & PRICES ---
CATALOG = {
    "Hollywood Smile / Dental (Diş Estetiği)": {
        "doctors": ["Dt. Ayşe Kaya", "Dt. Burak Yılmaz"],
        "price": 1200,
        "icon": "🦷"
    },
    "Sapphire FUE Hair Transplant (Saç Ekimi)": {
        "doctors": ["Dr. Can Çelik", "Dr. Kerem Arslan"],
        "price": 1800,
        "icon": "💇‍♂️"
    },
    "Medical Aesthetics & Botox (Medikal Estetik)": {
        "doctors": ["Uzm. Dr. Zeynep Nur", "Dr. Selin Demir"],
        "price": 450,
        "icon": "✨"
    },
    "Check-Up & Consultation (Genel Muayene)": {
        "doctors": ["Prof. Dr. Ahmet Vural"],
        "price": 150,
        "icon": "🩺"
    }
}

TIME_SLOTS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]

# --- INITIALIZE SESSION STATE DATABASE ---
if "bookings_df" not in st.session_state:
    initial_data = [
        {"Code": "CP-1021", "Date": "2026-10-26", "Time": "10:00", "Patient": "Alexander Ivanov", "Phone": "+7 916 123 4567", "Country": "Russia", "Department": "Sapphire FUE Hair Transplant (Saç Ekimi)", "Doctor": "Dr. Can Çelik", "Price_EUR": 1800, "Status": "Confirmed", "Notes": "VIP Airport Pickup requested"},
        {"Code": "CP-1022", "Date": "2026-10-26", "Time": "14:00", "Patient": "Hans Müller", "Phone": "+49 170 987 6543", "Country": "Germany", "Department": "Hollywood Smile / Dental (Diş Estetiği)", "Doctor": "Dt. Ayşe Kaya", "Price_EUR": 1200, "Status": "Confirmed", "Notes": "4-Star Hotel in Alanya"},
        {"Code": "CP-1023", "Date": "2026-10-27", "Time": "11:00", "Patient": "Sarah Jenkins", "Phone": "+44 7700 900077", "Country": "UK", "Department": "Medical Aesthetics & Botox (Medikal Estetik)", "Doctor": "Uzm. Dr. Zeynep Nur", "Price_EUR": 450, "Status": "Pending", "Notes": "First consultation"},
        {"Code": "CP-1024", "Date": "2026-10-28", "Time": "09:00", "Patient": "Mehmet Özkan", "Phone": "+90 532 111 2233", "Country": "Turkey", "Department": "Check-Up & Consultation (Genel Muayene)", "Doctor": "Prof. Dr. Ahmet Vural", "Price_EUR": 150, "Status": "Confirmed", "Notes": "Local patient"}
    ]
    st.session_state["bookings_df"] = pd.DataFrame(initial_data)

# --- SIDEBAR: LANGUAGE & NAVIGATION ---
with st.sidebar:
    st.markdown("## 🏥 **CarePlus Pro**")
    selected_lang = st.selectbox(
        "🌍 Dil / Language / Язык / Sprache",
        list(TRANSLATIONS.keys()),
        index=0  # Turkish is Default
    )
    t = TRANSLATIONS[selected_lang]
    
    st.markdown("---")
    selected_nav = option_menu(
        menu_title=t["menu_title"],
        options=t["nav"],
        icons=["house-heart", "calendar2-check", "search", "speedometer2"],
        menu_icon="hospital",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "#0d6efd", "font-size": "18px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "2px"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
        }
    )
    st.markdown("---")
    st.caption("📍 Alanya / Antalya / İstanbul\n📞 7/24 WhatsApp: +90 500 000 0000")

# --- PAGE 1: HOME (ANA SAYFA) ---
if selected_nav == t["nav"][0]:
    st.markdown(f"""
    <div class="hero-box">
        <h1 style="margin:0; font-size:2.1rem;">{t['hero_title']}</h1>
        <p style="margin-top:10px; font-size:1.1rem; opacity:0.95;">{t['hero_sub']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(t["services_title"])
    
    cols = st.columns(2)
    for idx, (dept, info) in enumerate(CATALOG.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="service-card">
                <h4 style="margin:0; color:#0d6efd;">{info['icon']} {dept}</h4>
                <p style="margin:8px 0 4px 0; color:#495057;"><b>👨‍⚕️ Doctors:</b> {', '.join(info['doctors'])}</p>
                <p style="margin:0; color:#198754; font-weight:600;">💶 Package Price: €{info['price']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- PAGE 2: BOOK APPOINTMENT (RANDEVU AL) ---
elif selected_nav == t["nav"][1]:
    st.title(t["book_title"])
    st.write(t["book_desc"])
    
    # Dynamic Department -> Doctor selection outside form for instant reactivity
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        chosen_dept = st.selectbox(t["service"], list(CATALOG.keys()))
    with col_d2:
        available_docs = CATALOG[chosen_dept]["doctors"]
        chosen_doc = st.selectbox(t["doctor"], available_docs)
        
    with st.form("booking_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input(t["name"], placeholder="Alexey Smirnov / Ahmet Yılmaz")
            p_phone = st.text_input(t["phone"], placeholder="+90 5XX XXX XX XX")
            p_country = st.text_input(t["country"], placeholder="Türkiye / Germany / Russia / UK")
        with c2:
            p_date = st.date_input(t["date"], min_value=datetime.date.today())
            p_time = st.selectbox(t["time"], TIME_SLOTS)
            p_notes = st.text_input(t["notes"])
            
        submitted = st.form_submit_button(t["submit"], type="primary", use_container_width=True)
        
        if submitted:
            if not p_name.strip() or not p_phone.strip():
                st.error(t["error_msg"])
            else:
                df = st.session_state["bookings_df"]
                date_str = p_date.strftime("%Y-%m-%d")
                # Check slot conflict
                conflict = df[(df["Doctor"] == chosen_doc) & (df["Date"] == date_str) & (df["Time"] == p_time) & (df["Status"] != "Cancelled")]
                if not conflict.empty:
                    st.error(t["slot_taken"])
                else:
                    new_code = f"CP-{random.randint(1025, 9999)}"
                    new_row = {
                        "Code": new_code,
                        "Date": date_str,
                        "Time": p_time,
                        "Patient": p_name.strip(),
                        "Phone": p_phone.strip(),
                        "Country": p_country.strip() if p_country.strip() else "N/A",
                        "Department": chosen_dept,
                        "Doctor": chosen_doc,
                        "Price_EUR": CATALOG[chosen_dept]["price"],
                        "Status": "Pending",
                        "Notes": p_notes.strip()
                    }
                    st.session_state["bookings_df"] = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"{t['success_msg']} **{new_code}**")
                    st.balloons()

# --- PAGE 3: TRACK BOOKING (RANDEVU SORGULA) ---
elif selected_nav == t["nav"][2]:
    st.title(t["track_title"])
    query = st.text_input(t["track_input"])
    if st.button(t["track_btn"], type="primary"):
        if query.strip():
            df = st.session_state["bookings_df"]
            res = df[df["Code"].str.contains(query.strip(), case=False, na=False) | df["Phone"].str.contains(query.strip(), case=False, na=False)]
            if not res.empty:
                st.dataframe(res, use_container_width=True, hide_index=True)
            else:
                st.warning(t["track_not_found"])

# --- PAGE 4: ADMIN PANEL (YÖNETİCİ PANELİ) ---
elif selected_nav == t["nav"][3]:
    st.title(t["admin_title"])
    df = st.session_state["bookings_df"]
    
    # KPIs
    total_b = len(df)
    conf_b = len(df[df["Status"] == "Confirmed"])
    pend_b = len(df[df["Status"] == "Pending"])
    rev_eur = df[df["Status"] == "Confirmed"]["Price_EUR"].sum()
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="kpi-card"><div class="kpi-title">{t["kpi_total"]}</div><div class="kpi-value">{total_b}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card" style="border-left-color:#198754;"><div class="kpi-title">{t["kpi_confirmed"]}</div><div class="kpi-value" style="color:#198754;">{conf_b}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card" style="border-left-color:#ffc107;"><div class="kpi-title">{t["kpi_pending"]}</div><div class="kpi-value" style="color:#d39e00;">{pend_b}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card" style="border-left-color:#0dcaf0;"><div class="kpi-title">{t["kpi_revenue"]}</div><div class="kpi-value">€{rev_eur:,}</div></div>', unsafe_allow_html=True)
    
    st.subheader(t["admin_table"])
    
    # Interactive Editable Table for Receptionist / Admin
    edited_df = st.data_editor(
        df,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Pending", "Confirmed", "Completed", "Cancelled"],
                required=True
            )
        },
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button(t["save_changes"], type="primary", use_container_width=True):
            st.session_state["bookings_df"] = edited_df
            st.toast(t["saved_toast"], icon="✅")
            st.rerun()
            
    with col_btn2:
        # Excel Export
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            edited_df.to_excel(writer, index=False, sheet_name="Appointments")
        st.download_button(
            label=t["export_excel"],
            data=output.getvalue(),
            file_name="CarePlus_Appointments.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    st.markdown("---")
    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        st.markdown(f"**{t['chart_dept']}**")
        fig1 = px.pie(edited_df, names="Department", hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig1, use_container_width=True)
    with c_chart2:
        st.markdown(f"**{t['chart_status']}**")
        fig2 = px.bar(edited_df["Status"].value_counts().reset_index(), x="Status", y="count", color="Status")
        st.plotly_chart(fig2, use_container_width=True)
