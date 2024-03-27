import os  
import requests  
from bs4 import BeautifulSoup  
from fake_useragent import UserAgent  
from urllib.parse import urljoin, urlparse  
from datetime import datetime  
import logging  
  
# 设置目标网站的URL  
TARGET_URL = 'http://example.com'  
# 设置图片保存目录  
IMAGE_DIR = 'downloaded_images'  
# 设置日志文件名  
LOG_FILE = 'crawler.log'  
  
# 配置日志记录  
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s')  
  
# 检查并创建图片保存目录  
if not os.path.exists(IMAGE_DIR):  
    os.makedirs(IMAGE_DIR)  
  
# 初始化User-Agent  
ua = UserAgent()  
  
# 解析robots.txt并检查是否可以爬取  
def can_crawl(target_url):  
    robots_url = f"{target_url}/robots.txt"  
    try:  
        response = requests.get(robots_url)  
        response.raise_for_status()  
        # 假设robots.txt格式正确，这里简化处理，实际中需要更复杂的解析  
        for line in response.text.split('\n'):  
            if line.strip().startswith('Disallow:'):  
                path = line.split(':')[1].strip('/')  
                if path == '*' or urlparse(target_url).path.startswith(path):  
                    return False  
        return True  
    except requests.RequestException:  
        # 如果无法获取robots.txt，则默认允许爬取  
        return True  
  
# 发送请求并获取响应  
def get_response(url, use_proxy=False, proxy=None):  
    headers = {  
        'User-Agent': ua.random  
    }  
    if use_proxy and proxy:  
        proxies = {  
            'http': proxy,  
            'https': proxy  
        }  
        return requests.get(url, headers=headers, proxies=proxies)  
    else:  
        return requests.get(url, headers=headers)  
  
# 从页面中提取图片链接  
def extract_image_links(url):  
    response = get_response(url)  
    response.raise_for_status()  
    soup = BeautifulSoup(response.content, 'html.parser')  
    image_links = []  
    for img in soup.find_all('img'):  
        src = img.get('src')  
        if src and not src.startswith('data:') and not src.startswith('javascript:'):  
            image_links.append(urljoin(url, src))  
    return image_links  
  
# 下载图片并保存到本地  
def download_image(image_url, directory):  
    try:  
        response = get_response(image_url)  
        response.raise_for_status()  
        content_type = response.headers.get('Content-Type')  
        if content_type and 'image' in content_type:  
            filename = os.path.join(directory, os.path.basename(urlparse(image_url).path))  
            with open(filename, 'wb') as file:  
                file.write(response.content)  
  
            # 获取当前时间  
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
  
            # 记录日志，包括日期、时间、图片名称、保存路径和原始链接  
            logging.info(f"{current_time} - Downloaded image '{os.path.basename(filename)}' to '{filename}' from '{image_url}'")  
            return filename  
        else:  
            logging.warning(f"Skipped non-image content: {image_url}")  
    except requests.RequestException as e:  
        # 记录失败的原因  
        logging.error(f"Failed to download image from '{image_url}': {e}")  
    return None
  
# 主函数  
def main():  
    start_time = datetime.now()  
      
    if can_crawl(TARGET_URL):  
        image_links = extract_image_links(TARGET_URL)  
        for image_link in image_links:  
            filename = download_image(image_link, IMAGE_DIR)  
            if filename:  
                logging.info(f"Saved {filename} to {IMAGE_DIR}")  
    else:  
        logging.info("Cannot crawl this website based on robots.txt.")  
      
    end_time = datetime.now()  
    logging.info(f"Batch image download completed. Total time taken: {end_time - start_time}")
  
if __name__ == '__main__':  
    main()