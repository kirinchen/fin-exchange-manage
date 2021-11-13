import { Builder, By } from "selenium-webdriver";

export function showTotal(first: number, second: number): number {
  const total: number = first + second;
  console.log(`Theaaaa total is: ${total}`);
  return total;
}


let a = async () => {
  let driver = await new Builder().forBrowser('chrome').build();

  const web = 'https://store.line.me/stickershop/product/1149795/?ref=Desktop';//填寫你想要前往的網站
  driver.get(web)//透國這個driver打開網頁
  let em = await driver.findElement(By.css(".MdCMN09DetailView"));

  console.log("em:" + em);

};

a();

showTotal(100, 200);

console.log(`aaaa`);