#  Pedro Shoes Media QA Automation**

This script automates **verification and screenshot capture of images and videos** on Pedro Shoes’ website across multiple countries, pages, and device modes, producing a detailed report.

---

## **1. Multi-Country & Multi-Page Asset Mapping**

* Uses the `image_map` dictionary to define expected **images and videos** for:

  * Countries: `sg`, `tw`, `at`
  * Pages (URL paths)
  * Device modes: `desktop` and `mobile`
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
* Dismisses overlays and popups:

  * **Geo-IP modal**
  * **Cookie consent banner**
  * **Embedded chat widgets**
* Closes any **browser alerts**.

---

## **4. Screenshot Capture**

* Supports **images and videos**.
* Finds elements using **XPath**:

  * Images: `<img>` tags and `<source>` elements in `<picture>` tags.
  * Videos: `<video>` tags and `<source>` inside videos.
* Scrolls element into view before capture.
* Saves screenshots in structured folders:

```
screenshots/<mode>/<country>/<page-path>/<filename>
```

---

## **5. Reporting**

* Tracks **found** and **not found** files.
* Generates a text report (`screenshot_report.txt`) with:

  * Found files grouped by page
  * Not found files grouped by page
* Prints the report to the console for immediate feedback.

---

## **6. Workflow**

1. Iterate through device modes: `desktop` and `mobile`.
2. Loop through countries and page paths.
3. Navigate to URL, dismiss overlays and alerts.
4. Search for and capture screenshots of each image/video.
5. Record results into **found/not found** lists.
6. Save the **final report** to file and console.

---

## **7. Advantages**

* Handles **dynamic content** and slow-loading pages.
* Automatically removes popups and chat widgets.
* Supports **image and video screenshot capture**.
* Produces a **structured, easy-to-read report** for QA or monitoring.
* Works across multiple device modes without changing the code.

---

I can also create a **visual workflow diagram** showing the process from `page load → overlay removal → screenshot → reporting`, which makes it easier for a team to understand at a glance.

Do you want me to make that diagram next?
