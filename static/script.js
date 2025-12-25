document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. TANIMLAMALAR ---
    const modeSelect = document.getElementById('grow-mode');
    const filizImg = document.getElementById('filiz-img');
    const bodyTag = document.body;
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    // --- 2. MOD VE GÖRSEL AYARLARI ---
    // Filiz'in resim yolları (Dosya isimlerinin birebir tuttuğundan emin ol)
    const images = {
        'default': 'static/img/filiz_yuz.png',       // Normal
        'yaz': 'static/img/filiz_yaz_kombin.png',    // Gözlüklü
        'kis': 'static/img/filiz_kis_kombin.png',    // Bereli (Varsa)
        'kurak': 'static/img/filiz_kurak_kombin.png',// Şapkalı (Varsa)
        'iliman': 'static/img/filiz_iliman_kombin.png' // Çiçekli (Varsa)
    };

    // Eğer select menüsü varsa (Bazen mobilde veya başka sayfada olmayabilir diye kontrol ediyoruz)
    if (modeSelect) {
        modeSelect.addEventListener('change', (event) => {
            const selectedMode = event.target.value;
            console.log("Seçilen Mod:", selectedMode); // Test için konsola yazdırır

            // Eski sınıfları temizle
            bodyTag.classList.remove('mode-yaz', 'mode-kis', 'mode-kurak', 'mode-iliman');

            // Yeni moda geçiş
            if (images[selectedMode]) {
                // Arka plan rengini değiştir (CSS'teki class'ı tetikler)
                bodyTag.classList.add('mode-' + selectedMode);
                
                // Resmi değiştir
                if (filizImg) {
                    filizImg.src = images[selectedMode];
                    
                    // Zıplama Animasyonu
                    filizImg.classList.add('filiz-pop');
                    setTimeout(() => {
                        filizImg.classList.remove('filiz-pop');
                    }, 300);
                }
            } else {
                // Tanımsız bir modsa varsayılana dön
                if (filizImg) filizImg.src = images['default'];
            }
        });
    }

    // --- 3. SOHBET (CHAT) MANTIĞI ---
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (!message) return;

            // Kullanıcı mesajını ekrana yaz
            addMessage(message, 'user');
            messageInput.value = '';
            
            // Animasyon: Filiz Düşünüyor...
            setAnimation('thinking');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();

                // Filiz Cevap Veriyor...
                setAnimation('speaking');
                
                // Cevabı ekrana bas
                if (data.card_title) {
                    addCard(data); // Eğer özel kart geldiyse
                } else {
                    addMessage(data.response, 'assistant'); // Normal metin
                }

            } catch (error) {
                console.error('Hata:', error);
                addMessage('Bağlantı hatası oluştu. Lütfen tekrar dene.', 'assistant');
            } finally {
                // İşlem bitince normale dön
                setTimeout(() => setAnimation('idle'), 2000);
            }
        });
    }

    // --- YARDIMCI FONKSİYONLAR ---

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}-message`;
        div.textContent = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addCard(data) {
        const div = document.createElement('div');
        div.className = 'message assistant-message';
        // HTML Kart Yapısı
        div.innerHTML = `
            <div class="plant-card">
                <h3>${data.card_title}</h3>
                ${data.temperature ? `<p><strong>🌡️ Sıcaklık:</strong> ${data.temperature}</p>` : ''}
                ${data.moisture ? `<p><strong>💧 Nem:</strong> ${data.moisture}</p>` : ''}
                ${data.light ? `<p><strong>💡 Işık:</strong> ${data.light}</p>` : ''}
                ${data.fertilizer ? `<p><strong>🌿 Gübre:</strong> ${data.fertilizer}</p>` : ''}
                ${data.tips ? `<p><strong>⚠️ İpucu:</strong> ${data.tips}</p>` : ''}
            </div>
        `;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function setAnimation(state) {
        const animContainer = document.getElementById('filiz-animation');
        if (!animContainer) return;

        const leds = animContainer.querySelectorAll('.led');
        leds.forEach(led => led.style.animation = ''); // Reset

        if (state === 'idle') {
            leds.forEach(led => { led.style.background = 'purple'; led.style.animation = 'pulse 2s infinite'; });
        } else if (state === 'thinking') {
            leds.forEach(led => { led.style.background = 'cyan'; led.style.animation = 'loading 1s infinite'; });
        } else if (state === 'speaking') {
            leds.forEach(led => { led.style.background = 'white'; led.style.animation = 'speak 0.5s infinite'; });
        }
    }

});