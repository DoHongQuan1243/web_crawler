import requests
from bs4 import BeautifulSoup

# URL của trang web chứa thông tin lỗ hổng bảo mật
url = 'https://security.snyk.io/package/npm/jquery/3.4.1'

# Gửi yêu cầu GET để tải nội dung trang web
response = requests.get(url)

# Kiểm tra mã trạng thái của yêu cầu
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    vulnerability_elements = soup.find_all(class_='vue--table__tbody')
   
    for vulnerability in vulnerability_elements:
        #Lấy các thông tin trong phần tử vulnerability
        vulnerability_name = vulnerability.find_all('a',class_='vue--anchor')
        vulnerable_version = vulnerability.find_all('div',class_='vulnerable-versions')
        details = vulnerability.find_all('div', class_='vulns-table__description')
            



        for x,y,z in zip(vulnerability_name,vulnerable_version,details):
            print("[+]Vulnerability:",x.text.strip())
        
            print("[+]Vulnerable Version:",y.text.strip())
          
            
            details_text = z.text.strip()
            upgrade = details_text.split("How", 1)[0].strip()
            upgrade_index = details_text.index("Upgrade")
            upgrade_message = details_text[upgrade_index:].strip()
            print("[+] Details: ",  upgrade)
            print("[+] Upgrade Message:", upgrade_message)

                        
        
          
            print("\n----------\n")

else:
    print("Yêu cầu không thành công. Mã trạng thái:", response.status_code)
