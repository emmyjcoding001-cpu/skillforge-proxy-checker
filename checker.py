import requests
import time
from concurrent.futures import ThreadPoolExecutor

# SkillForge Community Tool - Simple Proxy Health Checker
# Open-source for Contributor role

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 10

def check_proxy(proxy):
    """Check a single proxy"""
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        start = time.time()
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        latency = round((time.time() - start) * 1000)
        
        if r.status_code == 200:
            return f"[OK] {proxy} | {latency}ms | IP: {r.json().get('origin')}"
        else:
            return f"[FAIL] {proxy} | Status: {r.status_code}"
    except Exception as e:
        return f"[FAIL] {proxy} | Error: {str(e)[:50]}"

def main():
    print("SkillForge Proxy Checker - Loading proxies.txt...")
    try:
        with open("proxies.txt", "r") as f:
            proxy_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("proxies.txt not found. Create it with proxies like ip:port")
        return

    print(f"Testing {len(proxy_list)} proxies...\n")
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_proxy, proxy_list)
        for res in results:
            print(res)

if __name__ == "__main__":
    main()