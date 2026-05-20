const fs = require("fs");
const puppeteer = require("puppeteer");

const START_PAGE = 1;
const END_PAGE = 54;
const NOT_SPECIFIED = "Не указано";

const allTeachers = [];
const result = [];

function escapeCsv(value) {
  return `"${String(value).replaceAll('"', '""')}"`;
}

async function main() {
  const browser = await puppeteer.launch({
    headless: false,
  });

  const page = await browser.newPage();

  for (let pageNumber = START_PAGE; pageNumber <= END_PAGE; pageNumber++) {
    const url = `https://atlas.herzen.spb.ru/teachers?page=${pageNumber}`;

    console.log(`Парсим страницу ${pageNumber}`);

    await page.goto(url, {
      waitUntil: "networkidle2",
    });

    const teachers = await page.evaluate(() => {
      const links = document.querySelectorAll("a.text-blue-600");

      return Array.from(links).map((link) => {
        return {
          name: link.textContent.trim(),
          link: link.href,
        };
      });
    });

    allTeachers.push(...teachers);
  }

  console.log(`Найдено преподавателей: ${allTeachers.length}`);

  for (const teacher of allTeachers) {
    console.log(`Парсим профиль: ${teacher.name}`);

    try {
      await page.goto(teacher.link, {
        waitUntil: "networkidle2",
      });

      const contactData = await page.evaluate(() => {
        const teacherInfo = document.querySelector(
          "div.flex.flex-col.p-4.px-2.lg\\:px-2",
        );

        if (!teacherInfo) {
          return {
            phone: "Не указано",
            email: "Не указано",
          };
        }

        const phoneBlock = teacherInfo.querySelector(
          "div.flex.lg\\:space-x-2.items-center.text-blue-400.py-1.lg\\:pl-2.rounded-lg.cursor-pointer.mb-1",
        );

        const emailBlock = teacherInfo.querySelector(
          "div.flex.items-center.text-blue-400.py-1.rounded-lg.cursor-pointer.mb-1",
        );

        const getTextOrDefault = (block) => {
          const text = block?.querySelector("h1.text-m")?.textContent.trim();
          return text || "Не указано";
        };

        return {
          phone: getTextOrDefault(phoneBlock),
          email: getTextOrDefault(emailBlock),
        };
      });

      result.push({
        name: teacher.name,
        email: contactData.email,
        phone: contactData.phone,
        link: teacher.link,
      });
    } catch (error) {
      result.push({
        name: teacher.name,
        email: NOT_SPECIFIED,
        phone: NOT_SPECIFIED,
        link: teacher.link,
      });

      console.log(`Ошибка при парсинге профиля: ${teacher.link}`);
    }
  }

  const fieldnames = ["name", "email", "phone", "link"];
  const header = fieldnames.join(";");
  const rows = result.map((teacher) => {
    return fieldnames.map((field) => escapeCsv(teacher[field])).join(";");
  });

  const csv = [header, ...rows].join("\n");

  fs.writeFileSync("puppeteer.csv", csv, "utf-8");

  await browser.close();

  console.log("CSV-файл создан: puppeteer.csv");
  console.log(`Всего записано строк: ${result.length}`);
}

main();
