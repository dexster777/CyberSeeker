import requests
import time

def search_github():
    print("=== GIT SEARCH ENGINE ===")
    print("Search types: [1] Partial search: type ~ at the beginning of the name to activate. [2] Exact search: type § at the beginning of the name.")
    print("(to exit, type: exit)")
    
    while True:
        keyword = input("\nEnter the search name: ").strip()
        
        if not keyword:
            continue
        if keyword.lower() == 'exit':
            print("[*] Exiting program.")
            break
            
        # Correct API endpoints
        api_repo = "https://api.github.com/search/repositories"
        api_code = "https://api.github.com/search/code"
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        # 1. Search by project name
        print(f"[*] Looking for projects with the name: {keyword}...")
        try:
            res_repo = requests.get(api_repo, params={"q": keyword}, headers=headers)
            if res_repo.status_code == 200:
                data = res_repo.json()
                total = data.get("total_count", 0)
                print(f"[+] Projects found: {total}")
                
                if total > 0:
                    for idx, item in enumerate(data.get("items",)[:5], 1):
                        print(f"    {idx}. Project: {item['full_name']}")
                        print(f"       Author: {item['owner']['login']}")
                        print(f"       Description: {item['description']}")
            elif res_repo.status_code == 403:
                print("[-] Error 403: Unauthenticated request limit exceeded. Please wait a minute.")
            else:
                # FIXED: Correct string formatting syntax below
                print(f"[-] Server returned an error: {res_repo.status_code}")
        except Exception as e:
            print("[-] Connection error while searching for projects.")

        time.sleep(1)

        # 2. Search for text within code files
        print(f"[*] Searching for mentions of '{keyword}' within code files...")
        try:
            res_code = requests.get(api_code, params={"q": keyword}, headers=headers)
            if res_code.status_code == 200:
                data = res_code.json()
                total = data.get("total_count", 0)
                print(f"[+] Matches found in files: {total}")
                
                if total > 0:
                    for idx, item in enumerate(data.get("items",)[:5], 1):
                        print(f"    {idx}. File: {item['name']} (in project {item['repository']['full_name']})")
            elif res_code.status_code == 403:
                print("[-] Error 403: GitHub protection. Code search often requires a personal token.")
            else:
                print(f"[-] Server returned error: {res_code.status_code}")
        except Exception as e:
            print("[-] Connection error during code search.")

        time.sleep(1)

if __name__ == "__main__":
    search_github()
