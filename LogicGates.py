# MANTIK KAPISI MODÜLÜ
# --------------------------------------------------------------------------------------------
# Bu modül Soket sınıfını ve tüm farklı türler için mantık kapısı sınıflarını,
# ayrıca MantıkKapısı üst sınıfını içerir.
import pygame

pygame.init()


# SOKET SINIFI
# --------------------------------------------------------------------------------------------
# Soketleri temsil eder, bileşenlerin giriş ve çıkışlarını sağlar. Bu, bağlantıya izin verir.
# Her mantık kapısının giriş soketleri ve bir çıkış soketi vardır, her biri Kablo Sınıfı'nın
# bir nesnesine bağlanabilir.
class Soket(pygame.sprite.Sprite):
    def __init__(self, x, y, genislik, yukseklik, kapi, giris):
        super().__init__()
        self.image = pygame.Surface([genislik, yukseklik])
        self.image.fill([153, 204, 255])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.kapi = kapi
        self.giris = giris
        self.bagli = False

        self.girisKablo = None
        self.cikisKablolari = []
        self.akim = False


# MANTIK KAPISI SINIFI
# --------------------------------------------------------------------------------------------
# Tüm mantık kapısı türleri için üst sınıf.
# x ve y pozisyonunu, ayrıca giriş ve çıkış soketlerini tanımlar.
class MantikKapisi(pygame.sprite.Sprite):
    def __init__(self, resim, isim, x, y):
        # Sprite sınıfından miras alır
        pygame.sprite.Sprite.__init__(self)
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isim = isim
        print(self.isim)
        if self.isim == "DEGILKapisi" or self.isim == "BUFFERKapisi":
            self.giris = Soket(x, (y + 25), 15, 15, self, True)
            self.girisListesi = [self.giris]
        else:
            self.girisA = Soket(x, (y + 11), 15, 15, self, True)
            self.girisB = Soket(x, (y + 38), 15, 15, self, True)
            self.girisListesi = [self.girisA, self.girisB]
        
        self.cikis = Soket((x + 108), (y + 25), 15, 15, self, False)
    
    # POLIMORFIZM
    # Her mantık kapısı bu fonksiyonu kullanır ve kendi mantıksal fonksiyonuna uygun olarak değiştirir.
    # Varsayılan olarak OR kapısı mantığı seçilmiştir, çünkü en basit olanıdır ve mantık kapılarında akımın
    # serbestçe akışını göstermek için yararlıdır.
    def mantikIslemi(self):
        if self.girisA.akim or self.girisB.akim:
            self.cikis.akim = True
        else:
            self.cikis.akim = False


# KALITIM
# Her farklı mantık kapısı MantıkKapısı üst sınıfından miras alır
class VEKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)

    def mantikIslemi(self):
        if self.girisA.akim and self.girisB.akim:
            self.cikis.akim = True
        else:
            self.cikis.akim = False


class VEYAKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)
    
    def mantikIslemi(self):
        if self.girisA.akim or self.girisB.akim:
            self.cikis.akim = True
        else:
            self.cikis.akim = False


class DEGILKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)

    def mantikIslemi(self):
        if self.giris.akim:
            self.cikis.akim = False
        else:
            self.cikis.akim = True


class VEDEGILKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)
    
    def mantikIslemi(self):
        if not (self.girisA.akim and self.girisB.akim):
            self.cikis.akim = True
        else:
            self.cikis.akim = False


class VEYADEGILKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)
    
    def mantikIslemi(self):
        if not self.girisA.akim and not self.girisB.akim:
            self.cikis.akim = True
        else:
            self.cikis.akim = False


class OZELVEYAKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)
    
    def mantikIslemi(self):
        if (self.girisA.akim or self.girisB.akim) and (not self.girisA.akim or not self.girisB.akim):
            self.cikis.akim = True
        else:
            self.cikis.akim = False

# XNOR KAPISI SINIFI
# --------------------------------------------------------------------------------------------
# Özel VEYA DEĞİL (XNOR) kapısını temsil eder.
class XNORKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)
    
    def mantikIslemi(self):
        if self.girisA.akim == self.girisB.akim:
            self.cikis.akim = True
        else:
            self.cikis.akim = False

class BUFFERKapisi(MantikKapisi):
    def __init__(self, resim, isim, x, y):
        super().__init__(resim, isim, x, y)

    def mantikIslemi(self):

        self.cikis.akim=self.giris.akim



# ANAHTAR SINIFI
# --------------------------------------------------------------------------------------------
# Mantık devresine akım açan veya kapatan anahtarı temsil eder
class Anahtar(pygame.sprite.Sprite):
    def __init__(self, resim, x, y, isim):
        pygame.sprite.Sprite.__init__(self)
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isim = isim
        self.tiklandi = False

        self.acik = False

        self.cikis = Soket((x + 84), (y + 15), 15, 15, self, False)
    
    def guncelle(self, acikResim, kapaliResim):
        if self.acik:
            self.image = acikResim
            self.cikis.akim = True
        else:
            self.image = kapaliResim
            self.cikis.akim = False


# AMPUL SINIFI
# --------------------------------------------------------------------------------------------
# Farklı mantık kapısı bileşenlerini birbirine bağlayan kabloları temsil eder
class Ampul(pygame.sprite.Sprite):
    def __init__(self, resim, x, y, isim):
        pygame.sprite.Sprite.__init__(self)
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isim = isim

        self.giris = Soket((x + 31), (y + 56), 15, 15, self, True)
    
    def guncelle(self, acikResim, kapaliResim):
        if self.giris.akim:
            self.image = acikResim
        else:
            self.image = kapaliResim
