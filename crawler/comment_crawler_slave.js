const puppeteer = require('puppeteer');
const fs        = require('fs');
const process   = require('process');
// let URL = 'https://www.foody.vn/ho-chi-minh/tuktuk-thai-bistro-le-thanh-ton';
let URL = process.argv[2];

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
    try{
        // let URL = 'https://www.foody.vn/nam-dinh/panda-chan-am-thuc-nhat'
        const browser = await puppeteer.launch({headless: true,executablePath: '/usr/bin/google-chrome',
        args: [
            '--start-maximized',
        ],});
        const page = await browser.newPage();
        await page.setViewport({
            width: 1080,
            height: 1920
        })
        await page.goto(URL,{waitUntil:'domcontentloaded',timeout: 30000});
        // link_url = 'a[href="https://foody.vn/ha-noi/com-ga-ba-hong-shop-online"]'
        // await page.click(link_url);
        await scrollHeight(page);
        console.log("Scrolled");
        try{
            i = 0;
            while(i < 10){
                await page.click('a[ng-click="LoadMore()"]');
                i = i + 1;
                console.log(i);
            }
        }catch(error){
            console.log(error)
        }
        console.log("Clicked");
        const data_extractor = await page.evaluate(function() {
            comments = (function() {
                var ref;
                ref = document.querySelectorAll('span[ng-bind-html]');
                ref_score = document.getElementsByClassName('review-points ng-scope');
                result_score = [];
                for (i = 0, len = ref_score.length; i < len; i++){
                    result_score.push(ref_score[i].innerText);
                }
                results = [];
                count_score = 0;
                for (i = 0, len = ref.length; i < len; i++) {      
                    if(ref[i].className == 'ng-binding'){
                        var comment_uer = ref[i].innerText;
                        var score_uer = result_score[count_score];
                        results.push({comment:comment_uer, score:score_uer});
                        count_score += 1;
                    }
                }
                return results;
            })();
            data = {
                url: window.location.href,
                comment: comments
            };
            return data;
        });
        // path_comment = '../data/raw_data/crawl_comments_foody.json'
        fs.writeFileSync(process.argv[3] + '.json', JSON.stringify(data_extractor, void 0,2));
        browser.close()
    } catch (error) {
        console.log("Errors:" + error)
    }

})();