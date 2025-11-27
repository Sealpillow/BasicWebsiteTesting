from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# pip install selenium webdriver-manager pillow

# ------------------------------------------------------------
# IMAGE + VIDEO MAPS
# ------------------------------------------------------------
image_map = {
    "sg": {
        "/": {
            "desktop": [
                "3_toppromobanner_pw_salestext_1_sgmy.jpg",
                "3_toppromobanner_pm_salestext_1_sgmy.jpg"
            ],
            "mobile": [
                "3_toppromobanner_pw_salestext_1_sgmy_mobile.jpg",
                "3_toppromobanner_pm_salestext_1_sgmy_mobile.jpg"
            ]
        },
        "/new/new-in/women-new-arrivals": {
            "desktop": ["PW4-95940013-2_SILVER.jpg"],
            "mobile": ["PW4-95940013-2_SILVER.jpg"]
        },
        "/thejournal/the-art-of-living/the-art-of-perspective-season-that-remembers.html": {
            "desktop": ["story-a1.mp4"],
            "mobile": ["story-a1-mobile.mp4"]
        }
    },
    "tw": {
        "/": {
            "desktop": [
                "3_toppromobanner_pw_salestext_1_tw_cn.jpg",
                "3_toppromobanner_pm_salestext_1_tw_cn.jpg"
            ],
            "mobile": [
                "3_toppromobanner_pw_salestext_1_tw_cn_mobile.jpg",
                "3_toppromobanner_pm_salestext_1_tw_cn_mobile.jpg"
            ]
        }
    },
    "at": {
        "/": {
            "desktop": [
                "3_toppromobanner_pw_salestext_1_en.jpg",
                "3_toppromobanner_pm_salestext_1_en.jpg"
            ],
            "mobile": [
                "3_toppromobanner_pm_salestext_1_en_mobile.jpg",
                "3_toppromobanner_pm_salestext_1_en_mobile.jpg"
            ]
        }
    }
}

# Supported video extensions
video_ext = (".mp4", ".webm", ".mov", ".m4v")

# ------------------------------------------------------------
# SAFE FOLDER NAME
# ------------------------------------------------------------
def safe_folder_name(url_path):
    return ["homepage"] if url_path == "/" else url_path.strip("/").split("/")

# ------------------------------------------------------------
# DISMISS OVERLAYS
# ------------------------------------------------------------
def dismiss_overlays(driver):
    # Geo-IP modal
    for modal in driver.find_elements(By.CSS_SELECTOR, ".geo_ip-body"):
        try:
            modal.find_element(By.CSS_SELECTOR, ".geo_ip-link").click()
        except:
            driver.execute_script("arguments[0].style.display='none';", modal)

    # Cookie banner
    for banner in driver.find_elements(By.CSS_SELECTOR, ".sticky_cookie-content"):
        try:
            banner.find_element(By.CSS_SELECTOR, "[test-cookie-close], .closePopup").click()
        except:
            driver.execute_script("arguments[0].style.display='none';", banner)

    # Chat widget
    for chat in driver.find_elements(By.ID, "embeddedMessagingConversationButton"):
        driver.execute_script("arguments[0].style.display='none';", chat)

# ------------------------------------------------------------
# DISMISS ALERT (browser permission)
# ------------------------------------------------------------
def dismiss_alert(driver):
    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        pass

# ------------------------------------------------------------
# CREATE DRIVER
# ------------------------------------------------------------
def create_driver(mode):
    options = webdriver.ChromeOptions()

    # Block notification permission prompt
    options.add_experimental_option(
        "prefs",
        {"profile.default_content_setting_values.notifications": 2}
    )
    # posible device name: 
    devices = [
        # iPhones
        "iPhone SE",       # small
        "iPhone X",        # medium
        "iPhone 12 Pro",   # large/pro

        # iPads (tablets)
        "iPad",            # standard
        "iPad Mini",       # small tablet
        "iPad Pro",        # large tablet

        # Android phones
        "Pixel 2",         # small/older
        "Pixel 4",         # mid-size/modern
        "Galaxy S5"        # popular default Android
    ]
    if mode == "mobile":
        options.add_experimental_option("mobileEmulation", {"deviceName": devices[1]})

    # Hide Chrome logs
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(ChromeDriverManager().install())
    service.log_path = "chromedriver.log"

    driver = webdriver.Chrome(options=options, service=service)

    if mode == "desktop":
        driver.maximize_window()

    return driver

# ------------------------------------------------------------
# WAIT FOR FULL PAGE LOAD
# ------------------------------------------------------------
def wait_for_full_page(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# ------------------------------------------------------------
# SCROLL + FULL-PAGE SCREENSHOT
# ------------------------------------------------------------
def screenshot_element_full(driver, element, save_path):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.5)
        driver.save_screenshot(save_path)
    except Exception as e:
        print("❌ Video screenshot failed:", e)

# ------------------------------------------------------------
# MAIN TEST LOGIC
# ------------------------------------------------------------
def run_test(driver, mode):
    wait = WebDriverWait(driver, 10)
    report = {"found": {}, "not_found": {}}

    for country, pages in image_map.items():
        print(f"\n=== COUNTRY: {country.upper()} ({mode}) ===")

        for path, file_sets in pages.items():
            file_list = file_sets.get(mode, [])
            if not file_list:
                continue

            url = f"https://www.pedroshoes.com/{country}{path}"
            folder_list = safe_folder_name(path)
            save_dir = os.path.join("screenshots", mode, country, *folder_list)
            os.makedirs(save_dir, exist_ok=True)

            driver.get(url)
            wait_for_full_page(driver)
            dismiss_overlays(driver)
            dismiss_alert(driver)

            for filename in file_list:
                key = f"{country}{path}"

                # Image search
                xpath_img = (
                    f"//img[contains(@src, '{filename}')]"
                    f" | //img[contains(@data-src, '{filename}')]"
                    f" | //source[contains(@srcset, '{filename}')]"
                )

                # Video search
                xpath_video = (
                    f"//video[contains(@src, '{filename}')]"
                    f" | //video/source[contains(@src, '{filename}')]"
                )

                matches_img = driver.find_elements(By.XPATH, xpath_img)
                matches_video = driver.find_elements(By.XPATH, xpath_video)

                # IMAGE FOUND
                if matches_img:
                    report["found"].setdefault(key, []).append(filename)

                    for i, img in enumerate(matches_img, start=1):
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", img)
                            time.sleep(0.4)
                            # if tracking multiple instance
                            # save_path = os.path.join(save_dir, f'{filename.rsplit(".", 1)[0]}_{i}.jpg')

                            # if one instance
                            save_path = os.path.join(save_dir, f"{filename}")
                            img.screenshot(save_path)
                        except Exception as e:
                            print(f"⚠ Could not screenshot image {filename}: {e}")

                # VIDEO FOUND
                elif matches_video:
                    report["found"].setdefault(key, []).append(filename)

                    for i, vid in enumerate(matches_video, start=1):
                        # if tracking multiple instance
                        # save_path = os.path.join(save_dir, f'{filename.rsplit(".", 1)[0]}_{i}.jpg')

                        # if one instance
                        save_path = os.path.join(save_dir, f'{filename.rsplit(".", 1)[0]}.jpg')
                        screenshot_element_full(driver, vid, save_path)

                # NOT FOUND
                else:
                    report["not_found"].setdefault(key, []).append(filename)

    return report

# ------------------------------------------------------------
# RUN BOTH MODES
# ------------------------------------------------------------
final_report = {}

for mode in ["desktop", "mobile"]:
    print(f"\n### STARTING {mode.upper()} ###")
    driver = create_driver(mode)
    report = run_test(driver, mode)
    driver.quit()
    final_report[mode] = report

# ------------------------------------------------------------
# PRINT + SAVE REPORT
# ------------------------------------------------------------
print("\n========= FINAL REPORT =========")
with open("screenshot_report.txt", "w", encoding="utf-8") as f:

    for mode, data in final_report.items():
        # Write the mode header (e.g., DESKTOP, MOBILE)
        header = f"\n===== {mode.upper()} =====\n"
        print(header)
        f.write(header)

        # Handle found files
        print("\n--- FOUND ---")
        f.write("\n--- FOUND ---\n")
        for page, files in data["found"].items():
            f.write(f"  {page}:\n")
            print(f"  {page}:")
            for idx, file in enumerate(files, 1):
                file_line = f"    {idx}. {file}"
                print(file_line)
                f.write(file_line + "\n")

        # Handle not found files
        print("\n--- NOT FOUND ---")
        f.write("\n--- NOT FOUND ---\n")
        for page, files in data["not_found"].items():
            f.write(f"  {page}:\n")
            print(f"  {page}:")
            for idx, file in enumerate(files, 1):
                file_line = f"    {idx}. {file}"
                print(file_line)
                f.write(file_line + "\n")


print("\nAll tests completed. Report saved as screenshot_report.txt")
