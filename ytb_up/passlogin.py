
async function login(localPage: Page, credentials: Credentials) {
    await localPage.goto(uploadURL)

    await changeLoginPageLangIfNeeded(localPage)

    const emailInputSelector = 'input[type="email"]'
    await localPage.waitForSelector(emailInputSelector)

    await localPage.type(emailInputSelector, credentials.email, { delay: 50 })
    await localPage.keyboard.press('Enter')

    // check if 2fa code was sent to phone
    await localPage.waitForNavigation()
    await localPage.waitForTimeout(1000)
    const googleAppAuthSelector = 'samp'
    const isOnGoogleAppAuthPage = await localPage.evaluate(
        (authCodeSelector) => document.querySelector(authCodeSelector) !== null,
        googleAppAuthSelector
    )

    if (isOnGoogleAppAuthPage) {
        const codeElement = await localPage.$('samp')
        const code = (await codeElement?.getProperty('textContent'))?.toString().replace('JSHandle:', '')
        code && console.log('Press ' + code + ' on your phone to login')
    }
    // password isnt required in the case that a code was sent via google auth
    else {
        const passwordInputSelector = 'input[type="password"]:not([aria-hidden="true"])'
        await localPage.waitForSelector(passwordInputSelector)
        await localPage.waitForTimeout(3000)
        await localPage.type(passwordInputSelector, credentials.pass, { delay: 50 })
    
        await localPage.keyboard.press('Enter')
    }

    try {
        await localPage.waitForNavigation()
        await localPage.waitForTimeout(1000)

        // check if sms code was sent
        const smsAuthSelector = '#idvPin'
        const isOnSmsAuthPage = await localPage.evaluate(
            (smsAuthSelector) => document.querySelector(smsAuthSelector) !== null,
            smsAuthSelector
        )
        if (isOnSmsAuthPage) {
            const code = await prompt('Enter the code that was sent to you via SMS: ')
            await localPage.type(smsAuthSelector, code)
            await localPage.keyboard.press('Enter')
        }
    } catch (error: any) {
        const recaptchaInputSelector = 'input[aria-label="Type the text you hear or see"]'

        const isOnRecaptchaPage = await localPage.evaluate(
            (recaptchaInputSelector) => document.querySelector(recaptchaInputSelector) !== null,
            recaptchaInputSelector
        )

        if (isOnRecaptchaPage) {
            throw new Error('Recaptcha found')
        }

        throw new Error(error)
    }
    //create channel if not already created.
    try {
        await localPage.click('#create-channel-button');
        await localPage.waitForTimeout(3000);
    } catch (error) {
        console.log('Channel already exists or there was an error creating the channel.');
    }
    try {
        const uploadPopupSelector = 'ytcp-uploads-dialog'
        await localPage.waitForSelector(uploadPopupSelector, { timeout: 70000 })
    } catch (error) {
        if (credentials.recoveryemail) await securityBypass(localPage, credentials.recoveryemail)
    }

    const cookiesObject = await localPage.cookies()
    await fs.mkdirSync(cookiesDirPath, { recursive: true })
    // Write cookies to temp file to be used in other profile pages
    await fs.writeFile(cookiesFilePath, JSON.stringify(cookiesObject), function (err) {
        if (err) {
            console.log('The file could not be written.', err)
        }
        console.log('Session has been successfully saved')
    })
}

// Login bypass with recovery email
async function securityBypass(localPage: Page, recoveryemail: string) {
    try {
        const confirmRecoveryXPath = "//*[normalize-space(text())='Confirm your recovery email']"
        await localPage.waitForXPath(confirmRecoveryXPath)

        const confirmRecoveryBtn = await localPage.$x(confirmRecoveryXPath)
        await localPage.evaluate((el: any) => el.click(), confirmRecoveryBtn[0])
    } catch (error) {
        console.error(error)
    }

    await localPage.waitForNavigation({
        waitUntil: 'networkidle0'
    })
    const enterRecoveryXPath = "//*[normalize-space(text())='Enter recovery email address']"
    await localPage.waitForXPath(enterRecoveryXPath)
    await localPage.waitForTimeout(5000)
    await localPage.focus('input[type="email"]')
    await localPage.waitForTimeout(3000)
    await localPage.type('input[type="email"]', recoveryemail, { delay: 100 })
    await localPage.keyboard.press('Enter')
    await localPage.waitForNavigation({
        waitUntil: 'networkidle0'
    })
    const uploadPopupSelector = 'ytcp-uploads-dialog'
    await localPage.waitForSelector(uploadPopupSelector, { timeout: 60000 })
}





    Go to your Google Security settings and note down your recovery email and delete recovery phone from your google settings
    Go to your Youtube settings and Setup your upload defaults Settings:
