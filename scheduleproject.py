import time
import smtplib #mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Windows arka planda çalıştırmak için
chrome_options = webdriver.ChromeOptions()
#chrome_options.headless = True
chrome_options.headless = False

#Warning hide yapmak için, sadece fatal hatalar gösterir
chrome_options.add_argument('--log-level=3')

#Arka planda çalışan ekran boyutları
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('C:\Windows\chromedriver', options=chrome_options)
driver.get('https://www.trendyol.com/butik/liste/1/kadin');
driver.maximize_window()

search_bar = driver.find_element_by_class_name("search-box")
search_bar.clear()

#Örnek ürün aramaları
#search_bar.send_keys("TWOAW20EL1313 Siyah")
search_bar.send_keys("04751303 Bej")
search_bar.send_keys(Keys.RETURN)

#Çıkan uyarı mesajını ekranın herhangi bir yerine tıklayarak linki tıklanabilir yapmak için
driver.find_element_by_xpath("//body").click()
productResult = driver.find_element_by_class_name("prdct-desc-cntnr-name").click()
#İki ekran yerine tek ekran kalması için
driver.close()

#Ürün detay ekranında işlem yapabilmek için
new_window = driver.window_handles[-1]
driver.switch_to.window(new_window)
wait = WebDriverWait(driver, 20)

#Ürün detayı ilk açıldığında seçili beden
print('Seçili beden: ' + driver.find_element_by_xpath("//div[@class='selected sp-itm']").text)
time.sleep(2)

#Örnek ürünler
#value = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='variants']//div[text()='38']")))
#value = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='variants']//div[text()='XS']")))
value = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='variants']//div[text()='S']")))
value.click()
print('Güncel beden: ' + value.text)
time.sleep(2)

#İstenilen bedeni seçtikten sonra stok durumuna göre butonlar değiştiği için buton kontrolü yapıyorum
button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='product-detail-app']/div/div[3]/div[1]/div[2]/div[5]/button")))
if button.text == 'Sepete Ekle':
    print('Ürün stokta var, ' + button.text + 'niyor')
else:
    print('Ürün ' + button.text)

#Eğer seçili ürün varsa Sepete Ekle butonu çıkıyor
if button.text == "Sepete Ekle":
    print("Mail gönderiliyor...")
    
    #Ürün stokta var ise satın alma işlemi kullanıcıya mail olarak bildiriliyor
    gmail_user = "shrgurel@gmail.com"
    gmail_pwd = "Shrgrl123."
    TO = 'shrgurel@gmail.com'
    SUBJECT = "Trendyol seçili ürün stoğu hakkında"
    TEXT = "Trendyol'da seçmiş olduğunuz ürünün stoğu güncellenmiştir. Talebiniz doğrultusunda satın alınacaktır."
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
            'From: %s' % gmail_user,
            'Subject: %s' % SUBJECT,
            '', TEXT])
    
    server.sendmail(gmail_user, [TO], BODY.encode('utf-8')) #Mailde Türkçe karakterler kullanabilmek için encode yaptım
    print ('Mail gönderildi!')

    #Sepete ekle
    addBasket = driver.find_element_by_class_name("add-to-basket-button-text").click()
    print('Sepete eklendi!')
    time.sleep(2)
    
    #Sepete ekledikten sonra sağ üstte dialog açılıyor. Buradan kontrol edebiliriz.
    #sip = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account-navigation-container']/div/div[2]/div/div/div[2]/a[2]"))).click()
    
    #Sepete git
    basket = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account-navigation-container']/div/div[2]/a/p"))).click()
    print('Sepet detayları görüntüleniyor...')
    time.sleep(2)
    
    #Sepeti onayla
    basketConfirm = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='pb-container']/aside/div/div[1]/a/span"))).click()
    print('Sepet onaylandı!')
    
    #Site kullanıcı giriş bilgileri
    mail_box = driver.find_element_by_id("login-email")
    mail_box.clear()
    mail_box.send_keys('se.her_22@hotmail.com')
    mail_box.submit()
    pass_box = driver.find_element_by_id("login-password-input")
    pass_box.clear()
    pass_box.send_keys('shrgrl123.')
    pass_box.submit()
    print('Kullanıcı girişi yapıldı!')

    #Belirtilen adres bilgisi işaretlenecek
    radioAddress = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='shippingAddress']/ul/li[5]/h3"))).click()
    print('Adres bilgisi işaretlendi!')
    time.sleep(2)
    
    #Kaydet ve devam et
    save = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='CheckoutAside']/section[5]/a"))).click()
    
    #Açılan ekranda pop-up çıktığı için sayfayı yenileyerek pop-up'u gizliyorum
    driver.refresh()
    
    #Kaydet ve devam et
    save = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='CheckoutAside']/section[5]/a"))).click()
    print('Bilgiler kaydedildi!')
    
    #Hangi kredi kartı ile ödeme yapılacağını bildirdim
    radioCard = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='creditCardPage']/div[1]/div[3]/div[2]/div/label/div[2]"))).click()
    print('Kredi kartı seçildi!')
    
    #Sözleşme onayı
    checkbox = driver.find_element_by_xpath("//*[@id='CheckoutAside']/section[3]/div[1]/label").click()
    print('Sözleşme kabul edildi!')
    
    #Ödeme işlemini tamamlıyorum
    #pay = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='CheckoutAside']/section[6]/a"))).click()
    print("Satın alma işlemi tamamlandı!")
    driver.close()
    
else:
    print("Ürün stoğu yenilendiğinde bilgilendirileceksiniz!")
    driver.close()
