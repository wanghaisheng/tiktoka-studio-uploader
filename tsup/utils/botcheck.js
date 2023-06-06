// https://github.com/prescience-data/puppeteer-botcheck/blob/91437c4e1bfc17f4803af73ce490729f6d26568b/src/botcheck.ts#L115

import chalk from "chalk"
import { Page } from "puppeteer"

import * as Types from "./types"

/**
 * Enum list of available tests.
 * @type {enum}
 */
export const enum TAGS {
  AREYOURHEADLESS = "areyouheadless",
  BEHAVIOUR_MONITOR = "behaviour",
  DATADOME = "datadome",
  EXECUTION_MONITOR = "execution",
  F5NETWORK = "f5",
  FINGERPRINTJS = "fingerprintjs",
  PIXELSCAN = "pixelscan",
  RECAPTCHA = "recaptcha",
  SANNYSOFT = "sannysoft",
  WHITEOPS = "whiteops",
}

/**
 * @class BotCheck
 * @classdesc Wraps a Puppeteer page instance to execute tests against anti-bot vendor scripts
 */
export class BotCheck implements Types.BotCheck {
  /**
   * Provides the active page context.
   * @type {Page}
   */
  page: Page

  /**
   * Constructor
   *
   * @param {Page} page
   */
  constructor(page: Page) {
    this.page = page
  }

  /**
   * Returns the test for the selected tag.
   *
   * @param {TAGS} tag
   * @return {Promise<string>}
   */
  public async run(tag: string) {
    switch (tag) {
      case TAGS.AREYOURHEADLESS:
        return this.areYouHeadless()
      case TAGS.BEHAVIOUR_MONITOR:
        return this.behaviorMonitor()
      case TAGS.DATADOME:
        return this.datadome()
      case TAGS.EXECUTION_MONITOR:
        return this.isolatedWorld()
      case TAGS.F5NETWORK:
        return this.f5network()
      case TAGS.FINGERPRINTJS:
        return this.fingerprintJs()
      case TAGS.PIXELSCAN:
        return this.pixelscan()
      case TAGS.RECAPTCHA:
        return this.recaptcha()
      case TAGS.SANNYSOFT:
        return this.sannysoft()
      case TAGS.WHITEOPS:
        return this.whiteOps()
      default:
        throw new Error(`Invalid test selected.`)
    }
  }

  /**
   * Test your scripts execution output.
   *
   * @return {Promise<string>}
   */
  public async isolatedWorld(): Promise<string> {
    await this.page.goto(
      "https://prescience-data.github.io/execution-monitor.html",
      { waitUntil: "networkidle2" }
    )
    // Test abstracted getElementById
    await this.page.$("#result")
    // Add any other tests you need here...
    await this.page.evaluate(() => {
      // Test createElement execution
      let newDiv = document.createElement("div")
      let newContent = document.createTextNode(
        "Creating an element on the page."
      )
      newDiv.appendChild(newContent)
      // Test getElementById execution
      let currentDiv = document.getElementById("div1")
      document.body.insertBefore(newDiv, currentDiv)
    })
    await this.page.waitForTimeout(2000)
    const element = await this.page.$("#result")
    if (!element) {
      throw new Error(`Could not find final element.`)
    }
    return await this.page.evaluate((element) => element.textContent, element)
  }

  /**
   * Test your scripts behaviour output.
   *
   * @return {Promise<string>}
   */
  public async behaviorMonitor(): Promise<string> {
    await this.page.goto(
      "https://prescience-data.github.io/behavior-monitor.html",
      { waitUntil: "networkidle2" }
    )
    // Hover and click an element
    const resultElement = await this.page.$("#result")
    if (!resultElement) {
      throw new Error(`Could not find result element.`)
    }
    await resultElement.hover()
    await resultElement.click({ delay: 10 })
    await this.page.waitForTimeout(200)
    // Type string
    const inputElement = await this.page.$("input#test-input")
    if (!inputElement) {
      throw new Error(`Could not find input element.`)
    }
    await inputElement.click()
    await inputElement.type("Hello world...", { delay: 3 })
    //@ts-ignore
    await this.page._client.send("Input.synthesizeScrollGesture", {
      x: 0,
      y: 0,
      xDistance: 0,
      yDistance: -100,
    })
    await this.page.waitForTimeout(2500)
    const element = await this.page.$("#result")
    if (!element) {
      throw new Error(`Could not find final element.`)
    }
    return await this.page.evaluate((element) => element.textContent, element)
  }

  /**
   * Test F5/Shape deployment.
   *
   * @return {Promise<string>}
   */
  public async f5network(): Promise<string> {
    await this.page.goto("https://ib.bri.co.id/ib-bri", {
      waitUntil: "networkidle2",
      timeout: 5000,
    })
    await this.page.waitForTimeout(2000)
    const element = await this.page.$("form#loginForm")
    return this._makeResult(!!element)
  }

  /**
   * Test PixelScan page.
   *
   * @return {Promise<string>}
   */
  public async pixelscan(): Promise<string> {
    await this.page.goto("https://pixelscan.net", { waitUntil: "networkidle2" })
    await this.page.waitForTimeout(1000)
    const element = await this.page.$("span.consistency-status-text")
    if (!element) {
      throw new Error(`Could not find result element.`)
    }
    return await this.page.evaluate((element) => element.textContent, element)
  }

  /**
   * Run suite of SannySoft tests.
   *
   * @return {Promise<string>}
   */
  public async sannysoft(): Promise<string> {
    await this.page.goto("https://bot.sannysoft.com", {
      waitUntil: "networkidle2",
    })
    await this.page.waitForTimeout(5000)
    const output = await this.page.evaluate(() => {
      let results: any = []
      const tables = document.querySelectorAll("table")
      let rows: any
      let cols: any = []
      for (let i = 0; i < 3; i++) {
        if (tables[i]) {
          rows = tables[i].querySelectorAll("tr")

          rows.forEach((row: Element) => {
            cols = row.querySelectorAll("td")
            if (cols[0]) {
              results.push({
                name: cols[0]
                  ? cols[0].textContent.replace(/\s/g, " ").trim()
                  : null,
                result: cols[1]
                  ? cols[1].textContent
                      .replace(/\s/g, " ")
                      .replace(/  +/g, " ")
                      .replace(/['"]+/g, "")
                      .trim()
                  : null,
              })
            }
          })
        }
      }
      return results
    })

    let finalOutput: string[] = []
    if (!!output && output.length) {
      output.forEach(({ name, result }: any) => {
        result = JSON.stringify(result)
        if (result.includes("FAIL") || result.includes("WARN")) {
          finalOutput.push(chalk.bgRed(`🚫 ${name}:\n ${result}`))
        } else {
          finalOutput.push(chalk.green(`✅ ${name}:\n ${result}`))
        }
      })
    } else {
      finalOutput.push(`⚠ No data found on page.`)
    }
    return finalOutput.join(`\n\n`)
  }

  /**
   * Test your recaptcha score.
   *
   * @return {Promise<string>}
   */
  public async recaptcha(): Promise<string> {
    await this.page.goto(
      "https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html",
      { waitUntil: "networkidle2" }
    )
    await this.page.waitForTimeout(15000)
    const element = await this.page.$("#score")
    if (!element) {
      throw new Error(`Could not find score element.`)
    }
    let result: string = (
      await this.page.evaluate((element) => element.textContent, element)
    ).trim()

    return result.includes("0.3") ||
      result.includes("0.2") ||
      result.includes("0.1")
      ? chalk.bgRed(result)
      : chalk.green(result)
  }

  /**
   * Test original AreYouHeadless test by Antoine Vastel.
   *
   * @return {Promise<string>}
   */
  public async areYouHeadless(): Promise<string> {
    await this.page.goto("https://arh.antoinevastel.com/bots/areyouheadless", {
      waitUntil: "networkidle2",
    })
    await this.page.waitForTimeout(2000)
    await this.page.waitForSelector("#res")
    const element = await this.page.$("#res")
    if (!element) {
      throw new Error(`Could not find result element.`)
    }
    return await this.page.evaluate((element) => element.textContent, element)
  }

  /**
   * Test for FingerprintJS demo.
   *
   * @return {Promise<string>}
   */
  public async fingerprintJs(): Promise<string> {
    await this.page.goto("https://fingerprintjs.com/demo", {
      waitUntil: "networkidle2",
    })
    await this.page.waitForTimeout(5000)
    await this.page.waitForSelector("table.table-compact")
    const element = await this.page.$(
      "table.table-compact > tbody > tr:nth-child(4) > td.miriam"
    )
    if (!element) {
      throw new Error(`Could not find result table.`)
    }
    const text = await (await element.getProperty("textContent")).jsonValue()
    return this._makeResult(text === "NO")
  }

  /**
   * Interact with the DataDome homepage and test for captcha.
   *
   * @return {Promise<string>}
   */
  public async datadome(): Promise<string> {
    await this.page.goto("https://datadome.co", { waitUntil: "networkidle2" })
    await this.page.waitForTimeout(2000)
    const button = await this.page.$("#menu-item-18474")
    if (!button) {
      throw new Error("Could not find the button!")
    }
    await button.click({ delay: 10 })
    await this.page.waitForNavigation({ waitUntil: "networkidle2" })
    await this.page.waitForTimeout(500)
    const captcha = await this.page.$(
      `iframe[src^="https://geo.captcha-delivery.com/captcha/"]`
    )
    return this._makeResult(!captcha)
  }

  /**
   * Test for WhiteOps homepage.
   *
   * @return {Promise<string>}
   */
  public async whiteOps(): Promise<string> {
    await this.page.goto("https://www.whiteops.com", {
      waitUntil: "networkidle2",
    })
    await this.page.waitForTimeout(3000)
    const button = await this.page.$(
      'a[href="https://www.whiteops.com/company/about"]'
    )
    if (!button) {
      throw new Error("Could not find the button!")
    }
    await button.click({ delay: 8 })
    await this.page.waitForNavigation({ waitUntil: "networkidle2" })
    await this.page.waitForTimeout(500)
    const test = await this.page.$(
      `a[href="https://resources.whiteops.com/data-sheets/white-ops-company-overview"]`
    )
    return this._makeResult(!!test)
  }

  /**
   * Helper function to make chalked results strings.
   *
   * @param {boolean} result
   * @return {string}
   * @protected
   */
  protected _makeResult(result: boolean): string {
    return result ? chalk.green(`✅  Passed`) : chalk.bgRed(`🚫  Failed`)
  }
}

export default BotCheck
