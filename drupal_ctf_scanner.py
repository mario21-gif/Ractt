import requests
from bs4 import BeautifulSoup
import re

# List of sensitive files and directories to check
sensitive_paths = [
    "core/install.php", "core/authorize.php", "core/rebuild.php", "core/modules/statistics/statistics.php",
    "core/modules/system/tests/https.php", "core/modules/system/tests/http.php", "core/install.php",
    "core/rebuild.php", "modules/statistics/statistics.php", "modules/system/tests/https.php",
    "autoload.php", "composer.json", "composer.lock", ".git", ".svn", ".DS_Store", ".well-known",
    "CHANGELOG.txt", "INSTALL.txt", "LICENSE.txt", "MAINTAINERS.txt", "README.txt", "UPGRADE.txt",
    "phpinfo.php", ".htaccess", "robots.txt", "web.config", ".env", ".htpasswd",
    "includes", "misc", "modules", "profiles", "scripts", "sites", "themes"
]

# Common misconfigured headers
security_headers = [
    "X-Content-Type-Options", "X-Frame-Options", "X-XSS-Protection",
    "Content-Security-Policy", "Strict-Transport-Security"
]


def scan_website(url):
    print("
[DRUPAL VULNERABILITY SCAN]")
    drupal_vulns = {
        "Drupalgeddon 2 (SA-CORE-2018-002)": "/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax",
        "Drupalgeddon 3 (SA-CORE-2018-004)": "/user/password?name[%23post_render][]=system&name[%23markup]=phpinfo()&name[%23type]=markup",
        "RESTful Web Services (SA-CORE-2019-003)": "/node?_=node&_format=json",
        "CVE-2019-6342 (RCE)": "/node/1?_format=hal_json",
        "Services Module (RCE)": "/rest?services=endpoint",
        "Views Module (SQL Injection)": "/views/ajax",
        "Entity Reference Module (SQL Injection)": "/entityreference/autocomplete",
        "CVE-2018-7600 (RCE)": "/user/login?_format=json",
        "CVE-2019-6340 (RCE)": "/node/1?_format=hal_json",
        "SA-CORE-2020-002 (DoS)": "/core/misc/drupal.js?v=8.8.5",
        "PHP Module Code Execution (SA-CORE-2014-005)": "/?q=user/password&name[0;update users set name]=admin",
        "Open Redirect (SA-CORE-2018-004)": "/user/logout?destination=https://example.com",
        "Form API Injection (SA-CORE-2018-006)": "/user/register?element_parents=account/mail/#value&_wrapper_format=drupal_ajax",
        "CVE-2020-13671 (Authenticated RCE)": "/user/login?_format=json",
        "SA-CORE-2019-002 (File Upload Bypass)": "/user/register?element_parents=account/mail/#value",
        "SA-CORE-2014-003 (SQL Injection)": "/?q=node&destination=node",
        "SA-CORE-2016-004 (Access Bypass)": "/admin/structure/views/view/",
        "SA-CORE-2016-005 (Information Disclosure)": "/core/install.php?profile=testing&langcode=en",
        "SA-CORE-2018-005 (Data Injection)": "/?q=user/password&name[0;update users set name]=admin",
        "SA-CORE-2017-002 (CSRF Token Bypass)": "/user/login?_format=json"
    }

    for vuln_name, vuln_path in drupal_vulns.items():
        vuln_url = f"{url.rstrip('/')}/{vuln_path}"
        try:
            vuln_response = requests.get(vuln_url)
            if vuln_response.status_code == 200:
                print(f"[+] Vulnerable to {vuln_name}: {vuln_url}")
            else:
                print(f"[-] Not vulnerable to {vuln_name}")
        except requests.RequestException as e:
            print(f"[ERROR] Unable to check {vuln_name}: {str(e)}")

    print(f"[INFO] Scanning website: {url}")

    try:
        response = requests.get(url)
        headers = response.headers

        # Check for security headers
        print("\n[SECURITY HEADERS]")
        for header in security_headers:
            if header in headers:
                print(f"[+] {header} is present")
            else:
                print(f"[-] {header} is missing")

        # Check for sensitive files
        print("\n[SENSITIVE FILES]")
        for path in sensitive_paths:
            full_url = f"{url.rstrip('/')}/{path}"
            try:
                file_response = requests.get(full_url)
                if file_response.status_code == 200:
                    print(f"[+] Accessible: {full_url}")
                else:
                    print(f"[-] Not found: {full_url}")
            except requests.RequestException as e:
                print(f"[ERROR] Unable to check {full_url}: {str(e)}")

        # Check for directory listing
        print("\n[DIRECTORY LISTING]")
        if "Index of" in response.text:
            print("[!] Directory listing is enabled.")
        else:
            print("[+] Directory listing is disabled.")

    except requests.RequestException as e:
        print(f"[ERROR] Failed to scan {url}: {str(e)}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("Enter the target URL (e.g., http://example.com): ")
    scan_website(target_url)
