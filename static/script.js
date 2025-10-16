// static/script.js

// --- FİLİZ ANİMASYON KONTROL FONKSİYONU ---
function setAnimation(state) {
  // Animasyonun var olup olmadığını kontrol et, sadece ana sayfada çalışsın
  const filizAnimation = document.getElementById('filiz-animation');
  if (!filizAnimation) return;

  const leds = filizAnimation.querySelectorAll('.led');
  leds.forEach(led => led.style.animation = ''); // Önceki animasyonu sıfırla

  if (state === 'idle') {
    leds.forEach(led => { led.style.background = 'purple'; led.style.animation = 'pulse 2s infinite'; });
  } else if (state === 'thinking') {
    leds.forEach(led => { led.style.background = 'cyan'; led.style.animation = 'loading 2s infinite'; });
  } else if (state === 'speaking') {
    leds.forEach(led => { led.style.background = 'white'; led.style.animation = 'speak 1s infinite'; });
  } else if (state === 'user_speaking') {
    leds.forEach(led => { led.style.background = 'yellow'; led.style.animation = 'user-speak 1s infinite'; });
  }
}

// Sayfa yüklendiğinde animasyonu başlat
document.addEventListener("DOMContentLoaded", () => {
    setAnimation('idle'); // Başlangıç durumu

    const chatForm = document.getElementById("chat-form");
    if(!chatForm) return; // Sohbet formu yoksa devam etme
    
    const messageInput = document.getElementById("message-input");
    const chatMessages = document.getElementById("chat-messages");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userMessage = messageInput.value.trim();
        if (userMessage === "") return;

        addMessage(userMessage, "user-message");
        messageInput.value = "";
        
        // KULLANICI MESAJ GÖNDERİNCE: 'DÜŞÜNME' MODU
        setAnimation('thinking');
        showTypingIndicator();

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage }),
            });
            const data = await response.json();
            
            removeTypingIndicator();
            
            // FİLİZ CEVAP VERİRKEN: 'KONUŞMA' MODU
            setAnimation('speaking');
            addBotResponseCard(data);

            // Konuşma bittikten 3 saniye sonra 'bekleme' moduna dön
            setTimeout(() => {
                setAnimation('idle');
            }, 3000);

        } catch (error) {
            removeTypingIndicator();
            setAnimation('idle'); // Hata olursa da başa dön
            addMessage("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", "assistant-message");
            console.error("Hata:", error);
        }
    });

    function addMessage(message, className) {
        // ... (Bu fonksiyonun geri kalanı öncekiyle aynı, değiştirmeye gerek yok)
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${className}`;
        const contentDiv = document.createElement("div");
        contentDiv.className = "message-content";
        contentDiv.textContent = message;
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addBotResponseCard(data) {
        // ... (Bu fonksiyonun geri kalanı öncekiyle aynı, değiştirmeye gerek yok)
        const messageDiv = document.createElement("div");
        messageDiv.className = "message assistant-message";
        const cardHTML = `<div class="plant-card"><h3>${data.card_title}</h3>${data.temperature?`<p><strong>🌡️ İdeal Sıcaklık:</strong> ${data.temperature}</p>`:''}${data.moisture?`<p><strong>💧 İdeal Toprak Nemi:</strong> ${data.moisture}</p>`:''}${data.light?`<p><strong>💡 Işık İhtiyacı:</strong> ${data.light}</p>`:''}${data.fertilizer?`<p><strong>🌿 Gübreleme:</strong> ${data.fertilizer}</p>`:''}${data.tips?`<p><strong>⚠️ Dikkat:</strong> ${data.tips}</p>`:''}</div>`;
        messageDiv.innerHTML = cardHTML;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        // ... (Bu fonksiyonun geri kalanı öncekiyle aynı, değiştirmeye gerek yok)
        const typingDiv = document.createElement("div");
        typingDiv.id = "typing-indicator";
        typingDiv.className = "message assistant-message";
        typingDiv.innerHTML = `<div class="message-content">...</div>`;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        // ... (Bu fonksiyonun geri kalanı öncekiyle aynı, değiştirmeye gerek yok)
        const typingIndicator = document.getElementById("typing-indicator");
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
});