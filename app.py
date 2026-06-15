from flask import Flask, render_template
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Bu rota, Auto Scaling'i tetiklemek için CPU'yu kasten yoracak
@app.route('/satin-al')
def satin_al():
    sonuc = 0
    # İşlemciyi terleten o meşhur stres döngüsü
    for i in range(1, 15000000):
        sonuc += math.sqrt(i)
    
    return f"<h1>Tebrikler! Siparişiniz Alındı.</h1><p>İşlemci yoruldu, hesaplanan değer: {sonuc}</p><a href='/'>Geri Dön</a>"

if __name__ == '__main__':
    # Bulut sunucusunda tüm dış bağlantılara açmak için host='0.0.0.0' yapıyoruz
    app.run(host='0.0.0.0', port=5000, debug=True)