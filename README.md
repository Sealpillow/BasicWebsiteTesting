# Pedro Shoes Media QA Automation

This script automates **verification and screenshot capture of images and videos** on Pedro Shoes’ website across multiple countries, pages, and device modes, producing a structured report.

---

## **1. Multi-Country & Multi-Page Asset Mapping**

* Defines expected **images and videos** via the `image_map` dictionary:

  * **Countries:** `sg`, `tw`, `at`
  * **Pages:** URL paths per country
  * **Device modes:** `desktop` and `mobile`

* Supports common **image formats** (`.jpg`, `.png`) and **video formats** (`.mp4`, `.webm`, `.mov`, `.m4v`).

---

## **2. Browser Setup**

* Uses **Selenium with ChromeDriver**, managed via `webdriver-manager`.
* Configurable for **desktop or mobile emulation** (iPhone, iPad, Android presets included).
* Blocks browser **notification prompts**.
* Suppresses unnecessary Chrome logs.
* Maximizes desktop window for consistent screenshots.

---

## **3. Page Load & Element Handling**

* Waits for **full page load** (`document.readyState == "complete"`).

* Automatically dismisses overlays and popups:

  * **Geo-IP modal**
  * **Cookie consent banner**
  * **Embedded chat widgets**

* Closes any **browser alerts** (e.g., permission prompts).

---

## **4. Screenshot Capture**

* Supports **images and videos**.

* Locates elements using **XPath**:

  * **Images:** `<img>` tags, `<source>` tags within `<picture>`
  * **Videos:** `<video>` tags and `<source>` within videos

* Scrolls each element into view before capture.

* Saves screenshots in structured folders:

```
screenshots/<mode>/<country>/<page-path>/<filename>.png
```

* **Video screenshots:** Captures a static image of the video element.

---

## **5. Reporting**

* Tracks **found** and **not found** files per page.

* Generates a text report (`screenshot_report.txt`) with:

  * Found files grouped by page
  * Not found files grouped by page

* Also prints the report to the console for immediate feedback.

---

## **6. Workflow Overview**

1. Iterate through device modes: `desktop` and `mobile`.
2. Loop through countries and page paths.
3. Navigate to URL, dismiss overlays and alerts.
4. Search for and capture screenshots of each **image or video**.
5. Record results into **found/not found** lists.
6. Save the **final report** to file and console.

---

## **7. Advantages**

* Handles **dynamic content** and slow-loading pages.
* Automatically removes popups, overlays, and chat widgets.
* Supports **both image and video screenshot capture**.
* Produces a **structured, easy-to-read report** for QA or monitoring.
* Works across multiple device modes without code changes.

---

## **8. Installation Requirements**

Before running the script, you'll need to install the required Python packages.

1. **Install dependencies:**

   Use `pip` to install the necessary packages:

   ```bash
   pip install selenium webdriver-manager pillow
   ```

   * **`selenium`:** The web automation library for controlling the browser.
   * **`webdriver-manager`:** Manages ChromeDriver versions automatically.
   * **`pillow`:** A Python Imaging Library for handling images.

2. **Optional:** Ensure you have a working version of **Google Chrome** installed, as the script uses ChromeDriver to interact with the browser.

---

## **9. DevTools Screenshot Warning**

```
⚠ Could not screenshot image/video: Message: unknown error: unhandled inspector error: {"code":-32000,"message":"Cannot take screenshot with 0 width."}
(Session info: chrome=...)
```

This warning occurs when Chrome closes the DevTools session before Selenium completes the screenshot.

**Common causes:**

* The browser is under heavy load.
* The tab navigates or refreshes while Selenium is still capturing the screenshot.
* ChromeDriver temporarily disconnects.
* The window closes immediately after your last commands (e.g., right after `driver.quit()`).

> **Note:** Despite the warning, the screenshot is usually captured correctly.

Sure! You can add a section in the README for the installation requirements. Here's how it would look:

