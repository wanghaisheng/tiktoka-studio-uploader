import { Page } from "playwright";

class Botcheck {
  page: Page;

  /**
   * Must pass in a valid Puppeteer page instance
   * @param page
   */

  constructor(page: Page) {
    this.page = page;
  }

  /**
   * Simple goto and wait function used to load each test
   * @param url
   * @param delay
   * @returns {Promise<*>}
   */
  async goto(url: string, delay?: number = 2000) {
    return new Promise(async (resolve, reject) => {
      try {
        if (url) {
          await this.page.goto(url, { waitUntil: "networkidle" });
          await this.page.waitForTimeout(delay);
          resolve();
        } else {
          reject("No url provided");
        }
      } catch (err) {
        reject(err);
      }
    });
  }

  /**
   *
   * Methods for running tests
   *
   */

  async isolatedWorld() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto(
          "https://prescience-data.github.io/execution-monitor.html",
          200
        );

        // Test abstracted getElementById
        await this.page.$("#result");

        // Add any other tests you need here...

        await this.page.evaluate(() => {
          // Test createElement execution
          let newDiv = document.createElement("div");
          let newContent = document.createTextNode(
            "Creating an element on the page."
          );
          newDiv.appendChild(newContent);
          // Test getElementById execution
          let currentDiv = document.getElementById("div1");
          document.body.insertBefore(newDiv, currentDiv);
        });

        await this.page.waitForTimeout(2000);

        const element = await this.page.$("#result");
        let output = await (
          await element.getProperty("textContent")
        ).jsonValue();

        console.log("IsolatedWorld", output);

        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async behaviorMonitor() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto(
          "https://prescience-data.github.io/behavior-monitor.html",
          200
        );

        // Hover and click an element
        const resultElement = await this.page.$("#result");
        if (!resultElement) throw new Error("Failed to find #result");

        await resultElement.hover();
        await resultElement.click({ delay: 10 });

        await this.page.waitForTimeout(200);

        // Type string

        const inputElement = await this.page.$("input#test-input");
        if (!inputElement) throw new Error("Failed to find input#test-input");

        await inputElement.click();
        await inputElement.type("Hello world...", { delay: 3 });

        await this.page._client.send("Input.synthesizeScrollGesture", {
          x: 0,
          y: 0,
          xDistance: 0,
          yDistance: -100,
        });

        await this.page.waitFor(2500);

        const element = await this.page.$("#result");
        let output = await (
          await element.getProperty("textContent")
        ).jsonValue();

        console.log("BehaviorMonitor", output);

        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async f5network() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("https://ib.bri.co.id/ib-bri", 2000);

        const element = await this.page.$("form#loginForm");
        let output = element ? "Passed" : "Failed";

        console.log("F5 Network", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async pixelscan() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("https://pixelscan.net", 3000);

        const element = await this.page.$("span.consistency-status-text");
        let output = await (
          await element.getProperty("textContent")
        ).jsonValue();

        console.log("PixelScan", "Browser Fingerprint: " + output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async sannysoft() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("https://bot.sannysoft.com", 5000);

        const output = await this.page.evaluate(() => {
          return new Promise(async (resolve, reject) => {
            let results = [];

            const tables = document.querySelectorAll("table");
            let rows;
            let cols;

            for (let i = 0; i < 2; i++) {
              if (tables[i]) {
                rows = tables[i].querySelectorAll("tr");

                rows.forEach((row) => {
                  cols = row.querySelectorAll("td");
                  results.push({
                    name: cols[0] ? cols[0] : null,
                    result: cols[1] ? cols[1] : null,
                  });
                });
              }
            }

            resolve(results);
          });
        });

        console.log("Sannysoft", output);

        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async recaptcha() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto(
          "https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html",
          15000
        );

        const element = await this.page.$("#score");

        let output = await this.page.evaluate(
          (element) => element.textContent,
          element
        );

        console.log("Recaptcha Score", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async hellobot() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("http://anonymity.space/hellobot.php", 3000);

        await this.page.waitForSelector("#result");
        const element = await this.page.$("#result");

        let output = await (
          await element.getProperty("textContent")
        ).jsonValue();

        console.log("HelloBot", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async areyouheadless() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto(
          "https://arh.antoinevastel.com/bots/areyouheadless",
          2000
        );

        await this.page.waitForSelector("#res");
        const element = await this.page.$("#res");

        let output = await (
          await element.getProperty("textContent")
        ).jsonValue();

        console.log("AreYouHeadless", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async fingerprintjs() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("https://fingerprintjs.com/demo", 5000);

        await this.page.waitForSelector("table.table-compact");
        const element = await this.page.$(
          "table.table-compact > tbody > tr:nth-child(4) > td.miriam"
        );

        let text = await (await element.getProperty("textContent")).jsonValue();
        let output = text === "NO" ? "Passed" : "Failed";

        console.log("FingerprintJS", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async datadome() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("https://datadome.co", 2000);

        const button = await this.page.$("#menu-item-18474");

        if (button) {
          await button.click({ delay: 10 });
          await this.page.waitForNavigation({ waitUntil: "networkidle2" });
          await this.page.waitFor(500);
        } else {
          console.log("Could not find the button!");
        }

        let captcha = await this.page.$(
          'iframe[src^="https://geo.captcha-delivery.com/captcha/"]'
        );
        let output = captcha ? "Failed" : "Passed";

        console.log("Datadome", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }

  async whiteops() {
    return new Promise(async (resolve, reject) => {
      try {
        await this.goto("https://www.whiteops.com", 3000);

        const button = await this.page.$(
          'a[href="https://www.whiteops.com/company/about"]'
        );

        if (button) {
          await button.click({ delay: 8 });
          await this.page.waitForNavigation({ waitUntil: "networkidle2" });
          await this.page.waitFor(500);
        } else {
          console.log("Could not find the button!");
        }

        let test = await this.page.$(
          'a[href="https://resources.whiteops.com/data-sheets/white-ops-company-overview"]'
        );
        let output = test ? "Passed" : "Failed";

        console.log("Whiteops", output);
        resolve(output);
      } catch (err) {
        reject(err);
      }
    });
  }
}

module.exports = Botcheck;
