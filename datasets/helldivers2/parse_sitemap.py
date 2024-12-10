import xml.etree.ElementTree as ET

def get_urls_from_local_sitemap(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    urls = []
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(url.text)

    return urls

sitemap_file = "sitemap-helldivers_en-NS_0-0.xml"
urls = get_urls_from_local_sitemap(sitemap_file)

with open('urls_to_download.txt', 'w') as f:
    for url in urls:
        f.write(f"{url}\n")

print(f"Extracted {len(urls)} URLs and saved to urls_to_download.txt")