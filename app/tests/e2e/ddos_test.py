import requests
import json
import concurrent.futures
import time

# GANTI KE ENDPOINT CONSUME
# URL = "http://127.0.0.1:8000/api/v1/validate/quota/consume" 
TOTAL_REQUESTS = 20 
CONCURRENT_THREADS = 20

url = "http://localhost:8000/api/v1/otp/resend/email"

payload = json.dumps({
  "user_id": "02a9ad54-30a8-40b2-88d6-208e6978d3b4"
})
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

def send_request(request_id):
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, data=payload, timeout=5)
        elapsed = time.time() - start_time
        
        # Cek status code
        if response.status_code == 200:
            print(f"Req-{request_id}: Success (200) - {elapsed:.2f}s")
            return "success"
        elif response.status_code == 429:
            print(f"Req-{request_id}: RATE LIMITED (429) - {elapsed:.2f}s")
            return "limited"
        else:
            print(f"Req-{request_id}: {response.status_code} - {response.text[:50]}...")
            return "error"
            
    except Exception as e:
        print(f"Req-{request_id}: Failed - {str(e)}")
        return "failed"

def run_ddos():
    print(f"Memulai Load Test ke {url}")
    print(f"Total Request: {TOTAL_REQUESTS} | Thread: {CONCURRENT_THREADS}\n")
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        futures = [executor.submit(send_request, i) for i in range(1, TOTAL_REQUESTS + 1)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    print("\n--- REKAP HASIL ---")
    print(f"Lolos (200): {results.count('success')}")
    print(f"Kena Limit (429): {results.count('limited')}")
    print(f"Error Lain: {results.count('error')}")
    print(f"Gagal Koneksi: {results.count('failed')}")

if __name__ == "__main__":
    run_ddos()