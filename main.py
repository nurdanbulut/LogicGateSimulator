import pygame, os
from LogicGates import VEKapisi, VEYAKapisi, DEGILKapisi, VEDEGILKapisi, VEYADEGILKapisi, OZELVEYAKapisi, XNORKapisi, BUFFERKapisi, Anahtar, Ampul

# Genel ayarlar
pygame.init()
saat = pygame.time.Clock()

# Programın başlığını ayarlar
pygame.display.set_caption("Sayisal Tasarim Odevi ")

# Programın genişlik ve yüksekliğini ayarlar
GENISLIK, YUKSEKLIK = 1332, 802

# Ekran yüzeyini oluşturur
EKRAN = pygame.display.set_mode((GENISLIK, YUKSEKLIK))

# Arka planı yükler
ARKAPLAN = pygame.image.load(os.path.join("Assets", "arkaplanIzgarasi.png"))

# Her bir bileşenin resmini yükler ve boyutunu ayarlar
# Bu, tüm resimlerin aynı ve doğru boyutta olmasını sağlarken, resim kalitesini de korur.
# .convert_alpha performans nedenleriyle kullanılır.
VE_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "VEKapisi.png")).convert_alpha(), (128, 64))
VEYA_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "VEYAKapisi.png")).convert_alpha(), (128, 64))
DEGIL_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "DEGILKapisi.png")).convert_alpha(), (128, 64))
VE_DEGIL_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "VEDEGILKapisi.png")).convert_alpha(), (128, 64))
VEYA_DEGIL_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "VEYADEGILKapisi.png")).convert_alpha(), (128, 64))
OZELVEYA_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "OZELVEYAKapisi.png")).convert_alpha(), (128, 64))
BUFFER_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "BUFFERKapisi.png")).convert_alpha(), (128, 64))
XNOR_KAPISI_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "XNORKapisi.png")).convert_alpha(), (128, 64))
ACIK_ANAHTAR_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "acikAnahtar.png")).convert_alpha(), (90, 45))
KAPALI_ANAHTAR_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "kapaliAnahtar.png")).convert_alpha(), (90, 45))

ACIK_AMPOUL_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "acikAmpul.png")).convert_alpha(), (75, 75))
KAPALI_AMPOUL_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "kapaliAmpul.png")).convert_alpha(), (75, 75))

BILGI_MENU_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "bilgiMenu.png")).convert_alpha(), (90, 90))
BILGI_MENU_HOVER_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "bilgiMenuHover.png")).convert_alpha(), (90, 90))
BILGI_MENU_EKRAN_RESIM = pygame.image.load(os.path.join("Assets", "bilgiMenuEkran.png")).convert_alpha()  # 1066, 642

COP_KUTUSU_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "copKutusu.png")).convert_alpha(), (50, 65))
TEMIZLE_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "temizle.png")).convert_alpha(), (50, 65))
LOGO_RESIM = pygame.transform.smoothscale(pygame.image.load(os.path.join("Assets", "logo.png")).convert_alpha(), (260, 150))

# Bu sprite grubu tüm bileşenleri tutar
yanMenuSpriteGrubu = pygame.sprite.Group()
# Bu sprite grubu her mantık kapısının soketlerini tutar
tumSoketSpriteGrubu = pygame.sprite.Group()
# Bu sprite grubu tüm bağlı kabloları tutar
tumKabloSpriteGrubu = pygame.sprite.Group()
# Bu liste tüm mantık kapılarını tutar
tumMantikKapilariListesi = []
# Tüm sürüklenebilir sprite'lar (tüm bileşenler), çöp kutusu veya bilgi menüsü hariç
tumBilesenSpriteGrubu = pygame.sprite.Group()


# COP KUTUSU SINIFI
# --------------------------------------------------------------------------------------------
# Çöp kutusunu temsil eder, bileşenleri ve bunlara bağlı kabloları silmenizi sağlar.
class CopKutusu(pygame.sprite.Sprite):
    tiklandi = False
    def __init__(self, resim, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isim = "cop"

class Temizle(pygame.sprite.Sprite):
    tiklandi = False
    def __init__(self, resim, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isim = "temizle"
    def temizle(self):
        # Tüm mantık kapıları ve bileşenleri siler
        for bilesen in tumBilesenSpriteGrubu:
            if bilesen.isim not in ["temizle", "cop", "menu"]:
                if bilesen.rect.x>200:
                    if hasattr(bilesen, 'girisListesi'):
                        for giris in bilesen.girisListesi:
                            if giris.bagli:
                                giris.girisKablo.kill()
                            giris.kill()
                    if hasattr(bilesen, 'cikis'):
                        if bilesen.cikis.bagli:
                            for cikisKablolari in bilesen.cikis.cikisKablolari:
                                cikisKablolari.kill()
                        bilesen.cikis.kill()
                    bilesen.kill()
        # Tüm kabloları siler
        for kablo in tumKabloSpriteGrubu:
            kablo.kill()

# BILGI MENUSU SINIFI
# --------------------------------------------------------------------------------------------
# Bilgi menüsünü temsil eder, mantık kapısı simülatörünü nasıl kullanacağınızı ve her bileşenin nasıl çalıştığını açıklar.
class BilgiMenusu(pygame.sprite.Sprite):
    tiklandi = False
    goster = False
    def __init__(self, resim, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isim = "menu"
        # 1332 x 0.8 = 1066, 802 x 0.8 = 642
        # ^^^ Bilgi menüsü ekran çözünürlüğü

# KABLO SINIFI
# --------------------------------------------------------------------------------------------
# Farklı mantık kapısı bileşenlerini birbirine bağlayan kabloları temsil eder
class Kablo(pygame.sprite.Sprite):
    def __init__(self, baslangic, bitis):
        pygame.sprite.Sprite.__init__(self)
        self.baslangic = baslangic
        self.bitis = bitis
        self.renk = (0, 0, 0)
        self.genislik = 4

        self.baslangicSoket = None
        self.bitisSoket = None

    def ciz(self, ekran):
        pygame.draw.line(ekran, self.renk, self.baslangic, self.bitis, self.genislik)


# FARE IMLECI SINIFI
# --------------------------------------------------------------------------------------------
# Kullanıcının fare imlecini temsil eder.
# Sürükle ve bırak işlevini gerçekleştirir ve sürüklenen mantık kapısının ve ilgili giriş, çıkış soketlerinin
# ve kablolarının pozisyonunu günceller. Bu, kabloların ve soketlerin bileşenlere yapışmasını sağlar.
# Ayrıca yeni kabloların oluşturulmasını yönetir ve geçersiz kablo bağlantılarını önler.
class FareImleci(pygame.sprite.Sprite):
    tasimaListesi = []
    kaynakSoketListesi = []
    bitisSoketListesi = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.kaynakSoket = None

        # Fare imleci için bir dikdörtgen nesne oluşturur
        self.rect = pygame.Rect(0, 0, 5, 5)
        self.offsetX = 0
        self.offsetY = 0

    # Farenin ve taşıdığı nesnenin pozisyonunu günceller
    def guncelle(self):

        # Fare imlecinin x ve y pozisyonu
        self.xPos, self.yPos = pygame.mouse.get_pos()

        # Fare ne kadar hareket ettirildiğinin offsetini bulur
        self.offsetX = self.rect.x - self.xPos
        self.offsetY = self.rect.y - self.yPos

        # KAYNAK SOKETTEN KABLO SÜRÜKLE
        # Bu durumda bileşenin hareket etmesini durdurur, bu da kullanıcının soketten bir kablo sürüklemesine olanak tanır.
        if self.kaynakSoketListesi != []:
            # Kablo sürükleme ve bağlantı
            for soket in self.kaynakSoketListesi:

                # Kullanıcının bir giriş soketini bir çıkış soketine bağlamasını önler, çünkü kabloyu çıkış soketinden sürükleyip
                # giriş soketine bağlaması gerekir.
                if soket.giris:
                    break

                self.kaynakSoket = soket
                # Bir kablo oluşturur ve kablonun bitiş noktasını fare pozisyonuna ayarlar
                soket.bagliKablo = Kablo([soket.rect.x + 8, soket.rect.y + 8], [self.xPos, self.yPos])
                soket.bagliKablo.ciz(EKRAN)
                # Bu break gereklidir, böylece bir seferde yalnızca bir bileşenden kablo sürükleyebilirsiniz.
                break

        # SON BAGLI KABLOYU OLUSTUR
        # Her oyun döngüsünde bir sprite grubuna eklenen ve çizilen son bağlı kablonun yeni bir örneğini oluşturur.
        # Ayrıca geçersiz kablo bağlantılarını kontrol eder ve önler.
        elif self.bitisSoketListesi != []:

            gecerliBaglanti = True

            # Kablonun aynı kapıya bağlı olup olmadığını kontrol eder.
            if self.bitisSoketListesi[0].kapi == self.kaynakSoket.kapi:
                gecerliBaglanti = False

            # Bir giriş soketinin zaten bir kabloya bağlı olup olmadığını kontrol eder. (Birden fazla giriş olamaz)
            elif self.bitisSoketListesi[0].bagli:
                gecerliBaglanti = False

            # Her ikisinin de giriş soketleri olup olmadığını kontrol eder. (Bir giriş diğerine bağlanamaz)
            elif self.bitisSoketListesi[0].giris and self.kaynakSoket.giris:
                gecerliBaglanti = False

            # Her ikisinin de çıkış soketleri olup olmadığını kontrol eder. (Bir çıkış diğerine bağlanamaz)
            elif (not self.bitisSoketListesi[0].giris) and (not self.kaynakSoket.giris):
                gecerliBaglanti = False

            # Kabloyu ve sokete bağlar
            elif gecerliBaglanti:
                # Kablo sınıfının yeni bir örneğini oluşturur
                kablo = Kablo([self.kaynakSoket.rect.x + 8, self.kaynakSoket.rect.y + 8], [self.xPos, self.yPos])
                self.kaynakSoket.cikisKablolari.append(kablo)
                self.kaynakSoket.bagli = True

                for bitisSoketi in self.bitisSoketListesi:
                    # Bu iki satır kabloları ilgili başlangıç ve bitiş soketlerine bağlar.
                    kablo.baslangicSoket = self.kaynakSoket
                    kablo.bitisSoket = bitisSoketi
                    # Bu gerekli çünkü bir çıkış soketi birden fazla kabloya sahip olabilir
                    bitisSoketi.girisKablo = self.kaynakSoket.cikisKablolari[0]
                    bitisSoketi.bagli = True
                    # Bu break gereklidir, böylece bir seferde yalnızca bir giriş kablosu oluşturabilirsiniz.
                    break

                for kablo in self.kaynakSoket.cikisKablolari:
                    tumKabloSpriteGrubu.add(kablo)

        # BILEŞENLERİ SÜRÜKLE VE BIRAK
        # Eğer kaynakSoketListesi ve bitisSoketListesi boşsa, kullanıcı yeni bir kablo oluşturmaya çalışmıyordur,
        # bu nedenle bileşeni sürükleyip bırakmasına izin verir.
        # Ayrıca, bileşen sürüklenirken kabloların soketlerin ucuna yapışmasını ve bileşenle birlikte hareket etmesini sağlar.
        else:
            # Mantık kapılarını sürükleyip bırakma + kabloların ve soketlerin ilgili bileşenle birlikte hareket etmesi
            for bilesen in self.tasimaListesi:
                # Bilgi menüsü sürüklenip bırakılamaz, bu hareket etmeyen bir düğmedir.
                if bilesen.isim == "menu":
                    break
                elif bilesen.isim == "cop" or bilesen.isim == "temizle":
                    break

                # Mantık kapısı bileşenini fare ile hareket ettirir
                bilesen.rect.x -= self.offsetX
                bilesen.rect.y -= self.offsetY

                if bilesen.isim == "anahtar":
                    # Çıkış soketini fare ile hareket ettirir
                    bilesen.cikis.rect.x -= self.offsetX
                    bilesen.cikis.rect.y -= self.offsetY

                    # Bileşenin çıkış soketine bağlı herhangi bir kabloyu bileşen sürüklendiğinde onunla birlikte hareket ettirir.
                    if bilesen.cikis.bagli:
                        for kablo in bilesen.cikis.cikisKablolari:
                            kablo.baslangic[0] -= self.offsetX
                            kablo.baslangic[1] -= self.offsetY

                elif bilesen.isim == "ampul":
                    # Giriş soketini fare ile hareket ettirir
                    bilesen.giris.rect.x -= self.offsetX
                    bilesen.giris.rect.y -= self.offsetY

                    # Bileşenin giriş soketlerine bağlı herhangi bir kabloyu bileşen sürüklendiğinde onunla birlikte hareket ettirir.
                    if bilesen.giris.bagli:
                        bilesen.giris.girisKablo.bitis[0] -= self.offsetX
                        bilesen.giris.girisKablo.bitis[1] -= self.offsetY

                else:
                    # Çıkış soketini fare ile hareket ettirir
                    bilesen.cikis.rect.x -= self.offsetX
                    bilesen.cikis.rect.y -= self.offsetY
                    # Giriş soketlerini fare ile hareket ettirir
                    for giris in bilesen.girisListesi:
                        giris.rect.x -= self.offsetX
                        giris.rect.y -= self.offsetY

                    # Bileşenin giriş soketlerine bağlı herhangi bir kabloyu bileşen sürüklendiğinde onunla birlikte hareket ettirir.
                    for girisSoketi in bilesen.girisListesi:
                        if girisSoketi.bagli:
                            girisSoketi.girisKablo.bitis[0] -= self.offsetX
                            girisSoketi.girisKablo.bitis[1] -= self.offsetY
                    # Bileşenin çıkış soketine bağlı herhangi bir kabloyu bileşen sürüklendiğinde onunla birlikte hareket ettirir.
                    if bilesen.cikis.bagli:
                        for kablo in bilesen.cikis.cikisKablolari:
                            kablo.baslangic[0] -= self.offsetX
                            kablo.baslangic[1] -= self.offsetY

                # Bu break gereklidir, böylece bir seferde yalnızca bir bileşen alabilirsiniz.
                break

        self.rect.x, self.rect.y = self.xPos, self.yPos


# YAN MENU SINIFI
# --------------------------------------------------------------------------------------------
# Ekranın sol tarafında bulunan tüm mantık kapısı bileşenlerini içeren yan menüyü temsil eder.
# Ayrıca yeni bileşen örneklerinin oluşturulmasından ve çizilmesinden sorumludur.
class YanMenu:
    tiklandi = False
    surukleme = False
    def __init__(self):
        self.kenarlik = 256

    def ornekOlustur(self):
        veKapisi = VEKapisi(VE_KAPISI_RESIM, "VEKapisi", 0, 180)
        veyaKapisi = VEYAKapisi(VEYA_KAPISI_RESIM, "VEYAKapisi", 128, 180)
        degilKapisi = DEGILKapisi(DEGIL_KAPISI_RESIM, "DEGILKapisi", 0, 280)
        veDegilKapisi = VEDEGILKapisi(VE_DEGIL_KAPISI_RESIM, "VEDEGILKapisi", 128, 280)
        veyaDegilKapisi = VEYADEGILKapisi(VEYA_DEGIL_KAPISI_RESIM, "VEYADEGILKapisi", 0, 380)
        ozelVeyaKapisi = OZELVEYAKapisi(OZELVEYA_KAPISI_RESIM, "OZELVEYAKapisi", 128, 380)
        xnorKapisi = XNORKapisi(XNOR_KAPISI_RESIM, "XNORKapisi", 128, 480)
        bufferKapisi = BUFFERKapisi(BUFFER_KAPISI_RESIM,"BUFFERKapisi", 0,480)
        anahtar = Anahtar(KAPALI_ANAHTAR_RESIM, 10, 580, "anahtar")
        ampul = Ampul(KAPALI_AMPOUL_RESIM, 15, 80, "ampul")

        bilesenListesi = [veKapisi, veyaKapisi, degilKapisi, veDegilKapisi, veyaDegilKapisi, ozelVeyaKapisi, anahtar, ampul, bufferKapisi, xnorKapisi]

        # Yeni oluşturulan bileşenleri ilgili sprite gruplarına ekler
        for bilesen in bilesenListesi:
            yanMenuSpriteGrubu.add(bilesen)
            tumBilesenSpriteGrubu.add(bilesen)

            if bilesen.isim == "anahtar":
                tumSoketSpriteGrubu.add(bilesen.cikis)
            elif bilesen.isim == "ampul":
                tumSoketSpriteGrubu.add(bilesen.giris)
            else:
                tumMantikKapilariListesi.append(bilesen)
                tumSoketSpriteGrubu.add(bilesen.cikis)
                # Giriş listesi NOT kapısı ve diğer kapıların soketlerinin aynı anda çizilmesi için gereklidir.
                # Çünkü NOT kapısı sadece bir giriş soketi gerektirirken diğerleri iki giriş soketi gerektirir.
                for giris in bilesen.girisListesi:
                    tumSoketSpriteGrubu.add(giris)

    # Bu, mantık kapılarının her oyun döngüsünde gereksiz yere oluşturulmasını engeller,
    # kullanıcı yan menüden bir bileşeni sürüklediğinde yeni örnekler oluşturulur.
    def tiklandigindaOrnekOlustur(self, bilesen, isim):
        orneklenenObje = None
        if isim == "menu":
            bilesen.tiklandi = True
        elif isim == "VEKapisi":
            veKapisi = VEKapisi(VE_KAPISI_RESIM, "VEKapisi", 0, 180)
            orneklenenObje = veKapisi
        elif isim == "VEYAKapisi":
            veyaKapisi = VEYAKapisi(VEYA_KAPISI_RESIM, "VEYAKapisi", 128, 180)
            orneklenenObje = veyaKapisi
        elif isim == "DEGILKapisi":
            degilKapisi = DEGILKapisi(DEGIL_KAPISI_RESIM, "DEGILKapisi", 0, 280)
            orneklenenObje = degilKapisi
        elif isim == "VEDEGILKapisi":
            veDegilKapisi = VEDEGILKapisi(VE_DEGIL_KAPISI_RESIM, "VEDEGILKapisi", 128, 280)
            orneklenenObje = veDegilKapisi
        elif isim == "VEYADEGILKapisi":
            veyaDegilKapisi = VEYADEGILKapisi(VEYA_DEGIL_KAPISI_RESIM, "VEYADEGILKapisi", 0, 380)
            orneklenenObje = veyaDegilKapisi
        elif isim == "OZELVEYAKapisi":
            ozelVeyaKapisi = OZELVEYAKapisi(OZELVEYA_KAPISI_RESIM, "OZELVEYAKapisi", 128, 380)
            orneklenenObje = ozelVeyaKapisi
        elif isim == "XNORKapisi":
            xnorKapisi = XNORKapisi(XNOR_KAPISI_RESIM, "XNORKapisi", 128, 480)
            orneklenenObje = xnorKapisi
        elif isim == "anahtar":
            anahtar = Anahtar(KAPALI_ANAHTAR_RESIM, 15, 580, "anahtar")
            orneklenenObje = anahtar
        elif isim == "ampul":
            ampul = Ampul(KAPALI_AMPOUL_RESIM, 15, 80, "ampul")
            orneklenenObje = ampul
        elif isim == "BUFFERKapisi":
            orneklenenObje = BUFFERKapisi(BUFFER_KAPISI_RESIM,"BUFFERKapisi", 0,480)
        # Yeni oluşturulan bileşeni ilgili sprite gruplarına ekler
        if orneklenenObje != None:
            yanMenuSpriteGrubu.add(orneklenenObje)
            tumBilesenSpriteGrubu.add(orneklenenObje)

            if orneklenenObje.isim == "anahtar":
                tumSoketSpriteGrubu.add(orneklenenObje.cikis)
            elif orneklenenObje.isim == "ampul":
                tumSoketSpriteGrubu.add(orneklenenObje.giris)
            else:
                tumMantikKapilariListesi.append(orneklenenObje)

                tumSoketSpriteGrubu.add(orneklenenObje.cikis)
                # Giriş listesi NOT kapısı ve diğer kapıların soketlerinin aynı anda çizilmesi için gereklidir.
                # Çünkü NOT kapısı sadece bir giriş soketi gerektirirken diğerleri iki giriş soketi gerektirir.
                for giris in orneklenenObje.girisListesi:
                    tumSoketSpriteGrubu.add(giris)

    def spriteCiz(self):
        # Tüm mantık kapılarını çizer
        yanMenuSpriteGrubu.draw(EKRAN)
        # Tüm soketleri çizer
        tumSoketSpriteGrubu.draw(EKRAN)
        # Tüm kabloları çizer
        for kablo in tumKabloSpriteGrubu:
            kablo.ciz(EKRAN)

        for bilesen in yanMenuSpriteGrubu:
            if bilesen.isim == "anahtar":
                bilesen.guncelle(ACIK_ANAHTAR_RESIM, KAPALI_ANAHTAR_RESIM)
            elif bilesen.isim == "ampul":
                bilesen.guncelle(ACIK_AMPOUL_RESIM, KAPALI_AMPOUL_RESIM)


# ANA FONKSIYON
# --------------------------------------------------------------------------------------------
# Bu, her oyun döngüsünde tekrarlanan ana oyun döngüsünü içerir
def main():
    calistir = True
    # YanMenu sınıfının bir örneğini oluşturur
    yanMenu = YanMenu()
    # FareImleci sınıfının bir örneğini oluşturur - kullanıcının faresini temsil eder
    fare = FareImleci()

    yanMenu.ornekOlustur()

    bilgiMenusu = BilgiMenusu(BILGI_MENU_RESIM, 15, 650)
    yanMenuSpriteGrubu.add(bilgiMenusu)
    copKutusu = CopKutusu(COP_KUTUSU_RESIM, 162, 561)
    temizle = Temizle(TEMIZLE_RESIM, 162, 661)
    yanMenuSpriteGrubu.add(copKutusu)
    yanMenuSpriteGrubu.add(temizle)
    # Ana oyun döngüsü
    while calistir:
        fare.bitisSoketListesi = []
        bilgiMenusu.tiklandi = False
        silinecekListe = []
        for olay in pygame.event.get():

            # Pygame'in kapatılıp kapatılmadığını kontrol eder
            if olay.type == pygame.QUIT:
                calistir = False

            # Fare düğmesine basılıp basılmadığını kontrol eder
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                yanMenu.tiklandi = True
                yanMenu.surukleme = True
                fare.bitisSoketListesi = []
                # Çakışan tüm sprite'ları tasimaListesi'ne ekler
                fare.tasimaListesi = pygame.sprite.spritecollide(fare, yanMenuSpriteGrubu, False)
                # Fare pozisyonuyla çakışan soket sprite'larını kontrol eder, eğer doğruysa kaynakSoketListesi'ne ekler
                fare.kaynakSoketListesi = pygame.sprite.spritecollide(fare, tumSoketSpriteGrubu, False)

                if fare.tasimaListesi != []:
                    # Anahtar tıklandığında açılır
                    if fare.tasimaListesi[0].isim == "anahtar":
                        fare.tasimaListesi[0].acik = not fare.tasimaListesi[0].acik
                    # Bilgi menüsü tıklandığında rengini değiştirir ve menüyü açar
                    elif fare.tasimaListesi[0].isim == "menu":
                        bilgiMenusu.resim = BILGI_MENU_HOVER_RESIM
                        bilgiMenusu.goster = not bilgiMenusu.goster
                    # Temizle düğmesine tıklanırsa tüm bileşenleri siler
                    elif fare.tasimaListesi[0].isim == "temizle":
                        temizle.temizle()

            # Fare düğmesinin bırakılıp bırakılmadığını kontrol eder
            elif olay.type == pygame.MOUSEBUTTONUP:
                # Kullanıcının bir soketten diğerine kablo bağlamasına izin verir
                # Kullanıcının şu anda bir kablo sürükleyip sürüklemediğini kontrol eder
                if fare.kaynakSoketListesi != []:
                    fare.bitisSoketListesi = pygame.sprite.spritecollide(fare, tumSoketSpriteGrubu, False)

                yanMenu.surukleme = False

                # Fare tıklaması bırakıldığında tasimaListesi boşaltılır
                fare.tasimaListesi = []
                fare.kaynakSoketListesi = []
                bilgiMenusu.resim = BILGI_MENU_RESIM

        # Ekranı beyaz renk ile doldurur
        EKRAN.fill((255, 255, 255))
        # Arka planı ekrana çizer
        EKRAN.blit(ARKAPLAN, (256, 0))

        if fare.tasimaListesi != []:
            # Yan menüdeki bileşenleri yeniden oluşturur.
            # Bileşenler sürüklendiğinde, orijinal yerinde yeni bir örnek belirir.
            if yanMenu.tiklandi:
                yanMenu.tiklandigindaOrnekOlustur(fare.tasimaListesi[0], fare.tasimaListesi[0].isim)
                # Bu, her mantık kapısından yalnızca BIR örneğin oluşturulmasını sağlar, bu da performans etkisini en aza indirir.
                yanMenu.tiklandi = False

        EKRAN.blit(LOGO_RESIM, (0, 0))

        # Mantık kapılarını, soketleri ve kabloları çizer.
        yanMenu.spriteCiz()

        # Fare nesnesinin pozisyonunu, sürüklenen mantık kapısı bileşenlerini ve ilgili soketlerini ve bağlı kablolarını günceller.
        fare.guncelle()

        # AKIM İLETIMI
        # Akımı kaynak soketten bitiş soketine kablolar aracılığıyla iletir.
        for kablo in tumKabloSpriteGrubu:
            if kablo.baslangicSoket.akim:
                kablo.bitisSoket.akim = True
                kablo.renk = (255, 0, 0)
            else:
                kablo.bitisSoket.akim = False
                kablo.renk = (0, 0, 0)

        for bilesen in tumMantikKapilariListesi:
            bilesen.mantikIslemi()

        # COP KUTUSU İLE BILEŞENLERI SILME
        # Çöp kutusu ile herhangi bir sürüklenebilir bileşenin çarpışmasını kontrol eder.
        # COP KUTUSU İLE BILEŞENLERI SILME
        # Çöp kutusu ile herhangi bir sürüklenebilir bileşenin çarpışmasını kontrol eder.
        silinecekListe = pygame.sprite.spritecollide(copKutusu, tumBilesenSpriteGrubu, False)
        if silinecekListe != []:
            silinecekBilesen = silinecekListe[0]
            # Bağlı kabloları önce, soketleri sonra, ardından bileşeni siler.
            if silinecekBilesen.isim == "anahtar":
                # Bağlı kabloları siler
                for cikisKablolari in silinecekBilesen.cikis.cikisKablolari:
                    cikisKablolari.kill()
                # Tüm soketleri siler
                silinecekBilesen.cikis.kill()

            elif silinecekBilesen.isim == "ampul":
                # Bağlı kabloları siler
                if silinecekBilesen.giris.girisKablo is not None:
                    silinecekBilesen.giris.girisKablo.kill()
                # Tüm soketleri siler
                silinecekBilesen.giris.kill()

            elif silinecekBilesen.isim == "DEGILKapisi":
                # Bağlı kabloları siler
                if silinecekBilesen.giris.girisKablo is not None:
                    silinecekBilesen.giris.girisKablo.kill()
                for cikisKablolari in silinecekBilesen.cikis.cikisKablolari:
                    cikisKablolari.kill()
                # Tüm soketleri siler
                silinecekBilesen.giris.kill()
                silinecekBilesen.cikis.kill()
            elif str(silinecekBilesen) == "<BUFFERKapisi Sprite(in 2 groups)>":
                # Bağlı kabloları siler
                if silinecekBilesen.giris.girisKablo is not None:
                    silinecekBilesen.giris.girisKablo.kill()
                for cikisKablolari in silinecekBilesen.cikis.cikisKablolari:
                    cikisKablolari.kill()
                # Tüm soketleri siler
                silinecekBilesen.giris.kill()
                silinecekBilesen.cikis.kill()
            else:
                print(str(silinecekBilesen))
                # Bağlı kabloları siler
                if silinecekBilesen.girisA.girisKablo is not None:
                    silinecekBilesen.girisA.girisKablo.kill()
                if silinecekBilesen.girisB.girisKablo is not None:
                    silinecekBilesen.girisB.girisKablo.kill()
                for cikisKablolari in silinecekBilesen.cikis.cikisKablolari:
                    cikisKablolari.kill()
                # Tüm soketleri siler
                silinecekBilesen.girisA.kill()
                silinecekBilesen.girisB.kill()
                silinecekBilesen.cikis.kill()
            # Gerçek bileşeni siler
            silinecekBilesen.kill()

        if bilgiMenusu.goster:
            EKRAN.blit(BILGI_MENU_EKRAN_RESIM, (150, 80))

        # Ekranı günceller
        pygame.display.flip()
        saat.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
