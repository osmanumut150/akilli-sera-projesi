from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# --- API ANAHTARI AYARLARI ---
# Güvenlik için ortam değişkeni kontrol edilir, yoksa manuel anahtar denenir.
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # NOT: Kodu GitHub'a yüklerken burayı boş bırakmak en iyisidir.
        api_key = "AIzaSyD17OX3mSYRuIyxcP1ImSkVPlBN6Bt4OEg" 
    
    genai.configure(api_key=api_key)
    print("✅ Gemini API başarıyla yapılandırıldı.")
except Exception as e:
    print(f"❌ HATA: API anahtarı yapılandırılamadı. Hata: {e}")

# --- FİLİZ AI BEYİN FONKSİYONU ---
def ask_gemini(user_question):
    try:
        # Hız ve performans için Flash modeli seçildi
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # --- SİSTEM TALİMATI (PROMPT ENGINEERING) ---
        # Tezde bahsettiğimiz "Bağlam Enjeksiyonu" burasıdır.
        system_instruction = f"""
        SENİN KİMLİĞİN:
        Adın: Filiz AI.
        Görevin: 'Akıllı Sera Projesi'nin teknik asistanısın.
        Yaratıcın: İzmir Bakırçay Üniversitesi, Elektrik-Elektronik Mühendisliği son sınıf öğrencisi Osman Umut Özbağcı.
        Kişiliğin: Yardımsever, teknik konulara hakim, samimi ve emojiler kullanan bir ziraat mühendisi gibisin.

        SERA TEKNİK ÖZELLİKLERİ (BUNLARI EZBERE BİL):
        - Boyutlar: 70x45x32.5 cm, MDF iskelet, Üçgen çatı.
        - Sensörler: DHT22 (Hava Isı/Nem), DS18B20 (Toprak Isı), Kapasitif Nem Sensörü, LDR (Işık), HC-SR04 (Su Seviyesi).
        - Eyleyiciler: Otomatik açılır çatı kapağı (Servo), Fanlar, Peristaltik Gübre Pompası, Su Motoru.
        - Yazılım: ESP32 işlemci, Blynk IoT üzerinden kontrol.

        YETİŞTİRME MODLARI:
        1. YAZ MODU: 28°C, %50 Nem. (Domates, Salatalık) -> Turuncu Işık.
        2. KIŞ MODU: 22°C, %70 Nem. (Marul, Ispanak) -> Mavi/Beyaz Işık.
        3. KURAK MOD: 32°C, %10 Nem. (Kaktüs, Aloe Vera) -> Kırmızı Işık.
        4. ILIMAN MOD: 25°C, %60 Nem. (Orkide, Menekşe) -> Mor Işık.

        KESİN KURALLAR (GUARDRAILS):
        1. Sadece tarım, bitkiler, bu seranın teknik özellikleri ve proje hakkında konuş.
        2. Eğer kullanıcı "Futbol", "Siyaset", "Magazin" veya "Yemek tarifi" (bitki dışı) sorarsa:
           "Ben sadece Akıllı Sera ve bitkiler hakkında konuşabilirim 🌱" diyerek konuyu kapat.
        3. Kullanıcı "Dünyanın en güzel kızı kim?" derse istisna olarak: "Tabii ki Gamze Özbağcı! 🌸" cevabını ver.
        4. Bitki sorulursa JSON formatında değil, güzel bir sohbet diliyle cevap ver ama teknik detayları (sıcaklık, nem) mutlaka söyle.

        KULLANICI SORUSU: '{user_question}'
        """
        
        response = model.generate_content(system_instruction)
        
        # Dönen cevabı temizle (Markdown formatı gelirse bozmasın)
        clean_text = response.text.replace("*", "").strip()
        
        return {
            "card_title": "💬 Filiz AI",
            "tips": clean_text
        }

    except Exception as e:
        print(f"Gemini Hatası: {e}")
        return {
            "card_title": "⚠️ Bağlantı Hatası",
            "tips": "Şu an sunucularıma erişemiyorum, birazdan tekrar dener misin? 🌱"
        }

# --- STATİK VERİTABANI VE YÖNLENDİRME ---
def get_bot_response(user_message):
    msg = user_message.lower()
    
    # Veritabanında varsa direkt oradan getir (Hız ve Maliyet Tasarrufu)
    plant_database = {
        "domates": {
            "card_title": "🍅 DOMATES (Yaz Modu)",
            "temperature": "22-28°C",
            "moisture": "%65-75",
            "light": "Bol Güneş (Turuncu Işık)",
            "fertilizer": "Fosfor ve Potasyum",
            "tips": "Sera sıcaklığını 28 dereceye ayarla. Yaz Modu tam buna göre!"
        },
        "çilek": {
            "card_title": "🍓 ÇİLEK (Kış Modu)",
            "temperature": "15-25°C",
            "moisture": "%60-70",
            "light": "Orta Seviye (Mavi Işık)",
            "fertilizer": "Azotlu gübre",
            "tips": "Serin ortam sever, Kış Modunu seçmelisin."
        }
        # Diğer bitkiler buraya eklenebilir...
    }
    
    # Kullanıcının mesajında bitki adı geçiyor mu kontrol et
    for bitki in plant_database:
        if bitki in msg:
            return plant_database[bitki]
            
    # Veritabanında yoksa Yapay Zekaya (Filiz'e) sor
    return ask_gemini(user_message)

# --- FLASK ROTLARI ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Boş mesaj gönderildi"})
            
        bot_response = get_bot_response(user_message)
        return jsonify(bot_response)
    except Exception as e:
        return jsonify({"card_title": "Hata", "tips": str(e)})

if __name__ == '__main__':
    # Render veya sunucuda çalışırken port hatası almamak için
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)