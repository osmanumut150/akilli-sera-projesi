# app.py (Hibrit Model - Gemini Entegreli Tam Sürüm)

from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# YENİ ve GÜVENLİ YÖNTEM: Gemini API Anahtarını Ayarlama
# ----------------------------------------------------
# API anahtarını ortam değişkeninden güvenli bir şekilde alıyoruz.
# Terminalde şu komutu çalıştırarak anahtarı ayarlaman gerekir:
# Windows için: set GOOGLE_API_KEY="SENİN_YENİ_API_ANAHTARIN"
# Mac/Linux için: export GOOGLE_API_KEY="SENİN_YENİ_API_ANAHTARIN"
try:
    # DÜZELTİLDİ: Ortam değişkeninin ADINI doğru yazdık.
    api_key = os.getenv("GOOGLE_API_KEY") 
    if not api_key:
        # GEÇİCİ ÇÖZÜM: Eğer ortam değişkeni ayarlanmadıysa, anahtarı buraya yazabilirsin.
        # AMA BU GÜVENLİ DEĞİLDİR! Kodu paylaşırken bu satırı sildiğinden emin ol.
        api_key = "AIzaSyD17OX3mSYRuIyxcP1ImSkVPlBN6Bt4OEg"
    
    genai.configure(api_key=api_key)
    print("Gemini API başarıyla yapılandırıldı.")
except Exception as e:
    print(f"HATA: API anahtarı okunamadı veya yapılandırılamadı. Lütfen 'GOOGLE_API_KEY' ortam değişkenini ayarladığınızdan veya koda yazdığınızdan emin olun. Hata: {e}")
# ----------------------------------------------------


# YENİ ve GELİŞTİRİLMİŞ FONKSİYON
def ask_gemini(user_question):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # DİKKAT: İsteğimizi (Prompt) çok daha detaylı hale getiriyoruz.
        # Gemini'ye hem rolünü anlatıyor hem de nasıl bir cevap formatı istediğimizi örnekle gösteriyoruz.
        prompt = f"""
        Sen, 'Filiz' adında bir akıllı sera asistanısın. Görevin, kullanıcıların sorduğu bitkiler için sera ortamında geçerli olacak şekilde, ölçülebilir ve net yetiştirme koşulları sağlamaktır. Cevapların her zaman aşağıdaki gibi yapılandırılmış olmalı:

        ÖRNEK İSTENEN FORMAT:
        "card_title": "🍓 ÇİLEK YETİŞTİRME KOŞULLARI (SERA UYUMLU)",
        "temperature": "Gündüz: 20-25°C / Gece: 10-15°C",
        "moisture": "%60 - %70",
        "light": "12-14 saat/gün",
        "fertilizer": "Potasyum ağırlıklı sıvı gübre.",
        "tips": "Kök çürümesine karşı iyi drenaj ve havalandırma şarttır."

        Şimdi, bu formata birebir uyarak aşağıdaki bitki için sera yetiştirme koşullarını oluştur. Sadece ve sadece istenen formatta JSON benzeri bir metin çıktısı ver. Başka hiçbir açıklama ekleme.

        Kullanıcının Sorusu: '{user_question}'
        """
        
        response = model.generate_content(prompt)
        
        # Gemini'den gelen metni satırlara ayırıp bir sözlük (dictionary) haline getiriyoruz.
        # Bu sayede frontend tarafına her zaman tutarlı veri göndereceğiz.
        bot_response = {}
        # response.text içindeki "python" ve ``` işaretlerini temizliyoruz.
        cleaned_text = response.text.replace("```python", "").replace("```", "").strip()
        
        lines = cleaned_text.split('\n')
        for line in lines:
            if ":" in line:
                # Satırı ilk ':' karakterinden ikiye bölüyoruz.
                parts = line.split(':', 1)
                key = parts[0].strip().replace('"', '') # Anahtardaki tırnak işaretlerini temizle
                value = parts[1].strip().replace('"', '').replace(',', '') # Değerdeki tırnak ve virgülleri temizle
                bot_response[key] = value

        return bot_response

    except Exception as e:
        print(f"Gemini API Hatası: {e}")
        return {
            "card_title": "❌ Bir Sorun Oluştu",
            "tips": "Yapay zeka servisine şu anda ulaşılamıyor. Lütfen daha sonra tekrar deneyin."
        }


# MEVCUT FONKSİYONUN GÜNCELLENMİŞ HALİ
def get_bot_response(user_message):
    plant_name = user_message.lower()
    
    plant_database = {
        "çilek": {
            "card_title": "🍓 ÇİLEK YETİŞTİRME KOŞULLARI (SERA UYUMLU)",
            "temperature": "Gündüz: 20-25°C / Gece: 10-15°C",
            "moisture": "%60 - %70 (Kapasitif sensör değeri)",
            "light": "12-14 saat/gün (Tam spektrum veya Kırmızı/Mavi ağırlıklı)",
            "fertilizer": "Büyüme döneminde 2 haftada bir, potasyum ağırlıklı sıvı gübre.",
            "tips": "Kök çürümesine karşı iyi drenaj şarttır. Mantar hastalıklarına karşı havalandırma önemlidir."
        },
        "domates": {
            "card_title": "🍅 DOMATES YETİŞTİRME KOŞULLARI (SERA UYUMLU)",
            "temperature": "Gündüz: 22-28°C / Gece: 16-20°C",
            "moisture": "%65 - %75",
            "light": "En az 8-10 saat/gün doğrudan güneş ışığı",
            "fertilizer": "Fide döneminde azot, çiçeklenme döneminde fosfor ve potasyum ağırlıklı gübre.",
            "tips": "İyi havalandırma yaprak hastalıklarını önler. Düzenli sulama, meyve çatlamasını engeller."
        },
        "fesleğen": {
            "card_title": "🌿 FESLEĞEN YETİŞTİRME KOŞULLARI (SERA UYUMLU)",
            "temperature": "20-30°C arası sıcaklık idealdir. Soğuğa dayanıksızdır.",
            "moisture": "Toprağı kurumadan sulanmalı, ancak aşırı sudan kaçınılmalıdır.",
            "light": "Günde en az 6-8 saat ışık ister.",
            "fertilizer": "Ayda bir genel amaçlı sıvı gübre yeterlidir.",
            "tips": "Uçlarından düzenli budama, daha gür ve dallı büyümesini sağlar."
        }
    }
    
    if plant_name in plant_database:
        return plant_database[plant_name]
    else:
        return ask_gemini(user_message)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    bot_response = get_bot_response(user_message)
    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)