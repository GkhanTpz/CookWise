# 🍽️ CookWise - Akıllı Yemek Öneri Sistemi

CookWise, **elinizdeki malzemelere** göre **akıllı yemek önerileri** sunan bir Python uygulamasıdır. Kullanıcılar, sahip oldukları malzemeleri girdiklerinde, uygulama bu malzemelere en uygun yemekleri önerir. Ayrıca, tariflerin detaylarına kolayca ulaşabilirler. 🍳🥘

---

## 🚀 Özellikler

- **Malzeme Tabanlı Yemek Önerisi**: Kullanıcı, elindeki malzemeleri girdikten sonra, sistem mevcut malzemelere göre yemek önerileri sunar. 🥒🍅
- **Tarif Detayları**: Kullanıcı, önerilen yemeklerin tariflerine ulaşabilir. 📖🍴
- **Eksik Malzemeler**: Eğer önerilen yemeklerde eksik malzemeler varsa, sistem eksik malzemeleri de gösterir. ❌🍞
- **Basit ve Kullanıcı Dostu Arayüz**: PyQt6 kullanılarak oluşturulmuş modern ve kullanıcı dostu bir arayüz sunulmaktadır. 💻🎨

---

## 🛠️ Kullanım

### Gereksinimler

- **Python 3.8+** 🐍
- **PyQt6** (GUI için) 🎨
- **JSON verisi** ile yemek tarifleri ve malzeme listeleri 🍲📜

### Kurulum

1. **Projeyi bilgisayarınıza indirin**:
   ```bash
   git clone https://github.com/kullaniciadi/CookWise.git
   cd CookWise
   ```

2. **Sanal ortam oluşturun ve gerekli bağımlılıkları yükleyin**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Veritabanı dosyalarını** (`recipes.json` ve `preparations.json`) **`data/` klasörüne yerleştirin**.

4. **Uygulamayı çalıştırın**:

   ```bash
   python main.py
   ```

---

## 📁 Dosya Yapısı

Projenin dosya yapısı aşağıdaki gibi düzenlenmiştir:

```
CookWise/
│
├── main.py                # Ana uygulama dosyası 🖥️
├── data/
│   ├── recipes.json       # Yemek malzemelerini içeren JSON dosyası 🥗
│   └── preparations.json  # Yemek tariflerini içeren JSON dosyası 🍽️
├── icons/
│   ├── chef.png           # Şef ikonu 🍳
│   └── book.png           # Tarife kitap ikonu 📚
├── ui/
│   ├── icons.py           # İkonları yüklemek için fonksiyonlar 📦
│   └── styles.py          # Uygulama stil (QSS) temalarını içeren dosya 🎨
└── requirements.txt       # Gerekli Python paketlerinin listesi 📑
```

---

## 💻 Geliştirme

Proje üzerinde geliştirme yapmak için aşağıdaki adımları takip edebilirsiniz:

1. **Yeni özellikler ekleyin**: Örneğin, kullanıcı tercihlerine göre yemek önerileri veya diyet seçenekleri eklenebilir. 🥗🍔
2. **UI İyileştirmeleri**: Kullanıcı arayüzünü daha da profesyonelleştirebilirsiniz. Daha fazla tema veya animasyonlar eklemek mümkündür. 🌟
3. **Veri Güncellemeleri**: Yeni yemek tarifleri ve malzemeler eklemek için `recipes.json` ve `preparations.json` dosyalarını güncelleyebilirsiniz. 📈

---

## 🛠️ Teknolojiler

* **Python**: Uygulama Python 3 ile geliştirilmiştir. 🐍
* **PyQt6**: Kullanıcı arayüzü için PyQt6 kütüphanesi kullanılmaktadır. 🎨
* **JSON**: Yemek verisi ve tarifler JSON formatında saklanmaktadır. 📑

---

## 🤝 Katkı

Eğer projeye katkıda bulunmak isterseniz, **pull request** gönderebilir veya **sorunları (issues)** bildirebilirsiniz. Yeni özellik önerileri veya hata düzeltmeleri her zaman kabul edilir! 🔧

**CookWise** projesi, yemek yapmayı kolaylaştırmak ve kullanıcıların ellerindeki malzemelerle hızlıca yemek bulmalarını sağlamak amacıyla geliştirilmiştir. Yardımcı olabileceğimiz herhangi bir konuda çekinmeden bizimle iletişime geçebilirsiniz. 😊

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz. 📄
