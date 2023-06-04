import requests
from bs4 import BeautifulSoup
import re
import argparse
#urls = input("[*] url: ")
def scan_target(urls):
   
   print("[*] Scanning target...")
   #urls = 'https://www.adafruit.com/'
   # Fetch the web page content
   response = requests.get(urls)
   if response.status_code == 200:
      html_content = response.text

   # Define the regular expression pattern to match linked JavaScript resources
   pattern = r'<script.*?src=["\'](.*?)["\'].*?>'

   # Find all matches using regex
   matches = re.findall(pattern, response.text)
   libraries = []
   print("[*] Finished")
   print("[*] Found JS Component(s): ")

   for y in matches:
   
      url = urls + y
      if y[:8] == "https://":
         responset = requests.get(y)
      else:
         responset = requests.get(url)
      #responset = requests.get(url)
      html_contents = responset.text

      patternt = r"\/\*\!\s*(.*?)\s*\|"

      matchess =  re.findall(patternt, html_contents)

      for x in matchess:      
         print("[-]  ", x)
         libraries.append(x)
       
   print("\n===================================================")

   regex_pattern = r"(\w+).*?(\d+\.\d+\.\d+).*?"

   for z in libraries:
      matchesss = re.findall(regex_pattern, z )

      for match in matchesss:
         print("-Tên tệp:", match[0].lower())
         print("-Phiên bản:", match[1])
         
      for matchs in matchesss:
         url = f"https://security.snyk.io/package/npm/{matchs[0].lower()}/{matchs[1]}"
         print("[*]",url)
         print("")
   
      response = requests.get(url)
      # Sử dụng BeautifulSoup để phân tích cú pháp HTML
      soup = BeautifulSoup(response.text, 'html.parser')
      
      # Lấy các phần tử có class "vulnerability-details"
      vulnerability_elements = soup.find_all(class_='vue--table__tbody')   
      try:  
         for vulnerability in vulnerability_elements:
         # Lấy các thông tin trong phần tử vulnerability
               vulnerability_name = vulnerability.find_all('a',class_='vue--anchor')
               vulnerable_version = vulnerability.find_all('div',class_='vulnerable-versions')
               details = vulnerability.find_all('div', class_='vulns-table__description')
            

         # In ra thông tin
               for x,y,z in zip(vulnerability_name,vulnerable_version,details):
                  print("[+] Vulnerability:",x.text.strip())
                  print("[+] Vulnerable Version:",y.text.strip())  

                  details_text = z.text.strip()
                  detail = details_text.split("How", )[0].strip()
                  upgrade_index = details_text.index("Upgrade")
                  upgrade_message = details_text[upgrade_index:].strip()            
                  print("[+] Detail: ", detail)
                  print("[+] Recommendation:", upgrade_message)

                  print("\n\n")
      
         print("----------")
      except:
         print('[*] No vulerability found!')
   
      
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("-u", "--url", type=str, help="Target URL")

    args = parser.parse_args()
    url = args.url
    if url:
        scan_target(url)
    else:
        print("[-] No URL specified. Use -u or --url option to specify the target URL.")    
