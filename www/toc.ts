import VERSIONS from "../../versions.json" with { type: "json" };

type RawTableOfContents = Record<
  string,
  {
    label: string;
    content: Record<string, RawTableOfContentsEntry>;
  }
>;

interface RawTableOfContentsEntry {
  title: string;
  link?: string;
  pages?: [string, string, string?][];
}

const toc: RawTableOfContents = {
  latest: {
    label: VERSIONS[0],
    content: {
      introduction: {
        title: "Введение",
        pages: [
          /* ["advantages-of-use", "Преимущества использования"],
          ["special-offer", "Специальное предложение"], */
          [
            "fertility-determination",
            "Кому может потребоваться определение плодородия почвы и исследования грунтов",
          ],
          ["how-to-order", "Как заказать анализ"],
        ],
      },
      "getting-started": {
        title: "Начало работы",
        pages: [
          ["inspection-need", "Когда может потребоваться обследование"],
          [
            "sample-requirements",
            "Какие требования к отбору, транспортировке и хранению образцов",
          ],
        ],
      },
      concepts: {
        title: "Как работает РостХ",
        pages: [
          [
            "result-format",
            "В каком виде будет представлен результат исследования",
          ],
          ["data-usage", "Что делать с полученными данными"],
        ],
      },
      legal: {
        title: "Правовая информация",
        pages: [
          ["terms-of-service", "Условия использования сервиса"],
          [
            "processing-and-protection-of-personal-data",
            "Обработка и защита персональных данных",
          ],
          [
            "information-on-tariffs-and-payment-methods",
            "Информация о тарифах и способах оплаты",
          ],
          ["refund-policy", "Политика возврата средств"],
        ],
      },
    },
  },
};

export default toc;
