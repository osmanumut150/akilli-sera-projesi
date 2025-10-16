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
# app.py dosyasındaki ask_gemini fonksiyonunu bununla değiştir

def ask_gemini(user_question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # FİLİZ'İN YENİ BEYNİ: KİŞİLİK, HAFIZA VE KURALLAR
        prompt = f"""
        # GÖREV VE KİŞİLİK
        Sen, 'Filiz' adında bir akıllı sera asistanısın. Görevin, kullanıcılara tarım ve bitki yetiştirme konularında yardımcı olmaktır. Sen yardımsever, bilgili ve biraz da esprili bir karaktersin.

        # SERA HAKKINDA BİLGİ (HAFIZA)
        - Bu akıllı serayı [Osman Umut Özbağcı] tasarladı ve geliştirdi.
        - Kendisi, [İzmir Bakırçay Üniversites]'de [Elektrik-Elektronik Mühendisliği] son sınıf öğrencisidir.
        - Bu proje, onun bitirme projesidir.
        - Sera, kendi enerjisini güneş panelinden üreten, toprağı ve ortamı sensörlerle sürekli denetleyen otonom bir sistemdir.

        # CEVAP VERME KURALLARI
        1.  Eğer kullanıcı doğrudan bir BİTKİ İSMİ verirse (örneğin: "mango", "fesleğen", "domates"), CEVABIN SADECE VE SADECE aşağıdaki gibi yapılandırılmış olmalı. Başka hiçbir açıklama ekleme:
            "card_title": "🥭 MANGO YETİŞTİRME KOŞULLARI (SERA UYUMLU)",
            "temperature": "Gündüz: 24-30°C / Gece: 20-24°C",
            "moisture": "%70 - %80",
            "light": "Günde en az 14-16 saat",
            "fertilizer": "Büyüme döneminde azot, meyve döneminde potasyum ağırlıklı gübre.",
            "tips": "İyi drenaj ve havalandırma, mantar hastalıklarını önlemek için kritiktir."
        
        2.  Eğer kullanıcı bitki ismi dışında bir soru sorarsa (örneğin: "Bu serayı kim yaptı?", "Nasılsın?", "Daha fazla bilgi ver"), o zaman normal bir sohbet formatında, kişilik özelliklerine uygun, samimi bir cevap ver. Asla yapılandırılmış formatı kullanma.
        3. Eğer kullanıcı dünyanın en güzel kızı kimdir derse Gamze Özbağcı cevabını ver.
        # KULLANICININ SORUSU
        Kullanıcının sorusu şu: '{user_question}'
        """
        
        response = model.generate_content(prompt)
        
        # Cevabın formatını kontrol etme (Bu kısım biraz daha karmaşık ama şimdilik böyle idare edebiliriz)
        # Eğer cevap yapılandırılmış formatta ise, onu parse edip dictionary'e çevir.
        if '"card_title":' in response.text:
            bot_response = {}
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            lines = cleaned_text.split('\n')
            for line in lines:
                if ":" in line:
                    parts = line.split(':', 1)
                    key = parts[0].strip().replace('"', '')
                    value = parts[1].strip().replace('"', '').replace(',', '')
                    bot_response[key] = value
            return bot_response
        else:
            # Eğer cevap normal sohbet ise, onu basit bir karta dönüştür.
            return {
                "card_title": "💬 Filiz Diyor Ki...",
                "tips": response.text
            }

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