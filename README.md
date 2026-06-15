# AWS Auto Scaling ve Yük Dengeleme Tabanlı E-Ticaret Mimarisi

Bu proje, "Efsane Cuma" (Black Friday) gibi ani ve yüksek trafik dalgalanmalarına maruz kalan e-ticaret platformları için tasarlanmış, kendi kendini onarabilen (Self-Healing) ve dinamik olarak ölçeklenebilen (Auto Scaling) bir bulut bilişim altyapısıdır.

## Proje Amacı
Geleneksel veri merkezlerindeki atıl kapasite maliyetlerini önlemek amacıyla, sistem işlemci (CPU) yüküne göre otomatik olarak genişleyecek (Scale-Out) ve trafik normale döndüğünde küçülerek (Scale-In) maliyet optimizasyonu sağlayacak şekilde kurgulanmıştır. Python (Flask) tabanlı bir web uygulaması aracılığıyla donanım kasten yorularak AWS bulut otomasyonunun stres altındaki tepkileri test edilmiştir.

## Kullanılan Teknolojiler ve Bulut Servisleri
Bu sistem, AWS ekosisteminin temel bileşenleri entegre edilerek endüstri standartlarında bir mimari ile inşa edilmiştir:
* **Uygulama Katmanı:** Python 3, Flask Framework, HTML5/CSS3
* **İşlem ve Otomasyon:** AWS EC2 (t2.micro, Amazon Linux 2023), EC2 Launch Templates, Bash Scripting (User Data)
* **Trafik Yönetimi:** AWS Application Load Balancer (ALB), Target Groups
* **Ölçeklendirme ve İzleme:** AWS Auto Scaling Groups (ASG), Amazon CloudWatch

## Sistem Mimarisi ve Çalışma Mantığı
1. **Trafik Dağıtımı:** Kullanıcı istekleri doğrudan sunuculara değil, Application Load Balancer'a (ALB) gelir. ALB, HTTP Port 80 trafiğini arkadaki sağlıklı sunuculara dengeli bir şekilde paylaştırır.
2. **Kasıtlı İşlemci Yükü (Stress Test):** Müşteri e-ticaret arayüzündeki "Hemen Satın Al" butonuna tıkladığında, arka planda çalışan Flask uygulaması 15 milyon adımlık bir matematiksel döngüyü (`math.sqrt`) tetikleyerek işlemciyi anlık olarak %100 kullanım oranına ulaştırır.
3. **Otomatik Ölçeklendirme (Scale-Out):** Amazon CloudWatch, ortalama CPU tüketiminin %10 barajını aştığını tespit eder ve Auto Scaling grubunu tetikler. Sistem, kapasiteyi anında 1'den 3 sunucuya çıkararak site çökmesini engeller.
4. **Kendi Kendini Onarma (Self-Healing):** Sağlık kontrolünden (Health Check) geçemeyen veya kurulumu yarım kalan arızalı sunucular ALB tarafından anında tespit edilir. Fişleri çekilir (Terminate) ve yerlerine sıfırdan sağlıklı sunucular açılır.
5. **Maliyet Tasarrufu (Scale-In):** Trafik taarruzu sona erdiğinde ve işlemci rahatladığında, sistem fazla sunucuları otomatik olarak silerek başlangıç kapasitesine geri döner.

## Kurulum ve Simülasyon Adımları

**1. Depoyu Klonlayın:**
```bash
git clone [https://github.com/BerkayBozlar/BulutEticaret-AutoScaling.git](https://github.com/BerkayBozlar/BulutEticaret-AutoScaling.git)
cd BulutEticaret-AutoScaling
```

**2. AWS Başlatma Şablonu (Launch Template) Ayarları:**
Proje içerisindeki `user_data.sh` (veya `app.py` üretim) betiğini AWS EC2 Launch Template oluştururken "User Data" bölümüne yapıştırın. Bu betik, sunucu açılır açılmaz Python/Flask bağımlılıklarını kuracak ve web sunucusunu otomatik olarak yayına alacaktır.

**3. Test Senaryoları:**
* ALB DNS adresi üzerinden ana sayfaya gidin.
* "Hemen Satın Al" butonuna basarak veya sunucu terminaline SSH ile bağlanıp `cat /dev/zero > /dev/null &` komutunu çalıştırarak CPU'yu kasten kilitleyin.
* AWS Console üzerinden ASG ve EC2 Activity geçmişini izleyerek sistemin panik anında yeni sunucular açtığını gözlemleyin.
* İşlemci rahatladığında (`killall cat`) sistemin fazla sunucuları imha ettiğini (Scale-In) doğrulayın.
