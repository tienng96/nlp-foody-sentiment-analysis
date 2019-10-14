const puppeteer = require('puppeteer');
const fs        = require('fs');
const process   = require('process');
// let URL = 'https://www.foody.vn/ho-chi-minh/tuktuk-thai-bistro-le-thanh-ton';
// let URL = process.argv[0];

async function scrollHeight(
    page,
    scrollDelay = 5000
){
    let height_page ;
    height_page = await page.evaluate('document.body.scrollHeight');
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)');
    await page.waitFor(scrollDelay);
}
(async() => {
    let URL = 'https://www.foody.vn/';
    const browser = await puppeteer.launch({headless: true,executablePath: '/usr/bin/google-chrome'});
    const page = await browser.newPage();
    await page.setViewport({
        width: 1080,
        height: 1920
    })
    await page.goto(URL,{waitUntil:'domcontentloaded',timeout: 30000});
    
})