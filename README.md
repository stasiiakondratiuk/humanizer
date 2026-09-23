# Humanizer (RU / UK / EN / DE)

Skill для Claude Code, который убирает признаки AI-генерации из текста и делает его живым — на четырёх языках с автоопределением: **русском, украинском, английском, немецком**. Заточен под маркетинговый и социальный текст: лендинги, посты (Instagram / Threads / Telegram), сообщения лидам, офферы, письма, описания продуктов и услуг, статьи. Вплетает маркетинговые приёмы (конкретика с цифрами, «ты»-язык, живой хук) и банк живых человеческих фраз для каждого языка.

## Установка

```bash
# положить папку humanizer в ~/.claude/skills/
```

## Использование

В Claude Code:

```
/humanizer

[вставьте ваш текст на RU / UK / EN]
```

Или просто попросите:

```
Очеловечь этот текст: [текст]
Олюдни цей текст: [текст]
Make this sound human: [text]
Schreib das menschlicher: [Text]
```

Язык определяется автоматически, ответ выдаётся на языке оригинала.

## Что внутри

- **Форматы и регистр** — правит по-разному для лендинга, поста, DM, оффера и статьи (чем короче формат, тем беспощаднее).
- **Универсальные жёсткие запреты** — негативные параллелизмы, правило трёх, тире-паузы, риторические вопросы, эмодзи в заголовках.
- **Маркетинговые приёмы** — конкретика с цифрами, тест «сказал бы человек вслух», «ты»-язык, живой хук, один CTA.
- **Голос и душа** + **Калибровка** — как вернуть живую интонацию, но не сломать смысл и не выдумать фактов.

### 🇷🇺 Русский
Канцелярит (отглагольные существительные, родительные цепочки, пассив, copula avoidance), AI-словарь, вода, **маркетинговый и инфобизнес-штамп** (мёртвые клише, инфобиз-пафос, фейковая срочность), CTA и живая подача.

### 🇺🇦 Українська
Все те же + **окремий движок русизмів і кальок** (велика таблиця виправлень), активні дієприкметники, живі маркери української — **фемінітиви, кличний відмінок, ґ, апостроф**.

### 🇬🇧 English
AI vocabulary, copula avoidance, participial padding, hedging, sycophancy + **corporate / LinkedIn / marketing slop** (business-speak clichés, brochure tone, broetry hooks).

### 🇩🇪 Deutsch
**Nominalstil / Beamtendeutsch → Verbalstil** (главный маркёр: Funktionsverbgefüge и пассив → живые глаголы и активный залог), KI-Vokabular (eintauchen, ganzheitlich, nahtlos, maßgeschneidert), флоскели и Fazit-штампы, «kann/könnte»-хеджинг, денглиш-баззворды, немецкие маркетинговые клише + **Modalpartikeln** (doch/mal/halt/einfach) как маркер живой речи.

Каждая секция — с таблицами замен, банком живых фраз и примерами «до/после» в домене маркетинга.

## Структура

```
SKILL.md            маршрутизатор + общая логика (форматы, запреты, маркетинг, голос, калибровка)
references/ru.md    русские паттерны + живые фразы + пример
references/uk.md    украинские паттерны (движок русизмов) + живые фразы + пример
references/en.md    английские паттерны + живые фразы + пример
references/de.md    немецкие паттерны (Nominalstil→Verbalstil) + живые фразы + пример
evals/              тест-кейсы «до/после» на 4 языка + раннер
```

`SKILL.md` определяет язык и подгружает нужный `references/*.md` — прогрессивная загрузка, а не один тяжёлый файл.

## Evals

`evals/cases.jsonl` — 36 кейсов (9 RU / 9 UK / 9 EN / 9 DE) с маркерами `banned` (должны исчезнуть) и `keep` (факты должны остаться). Раннер на чистом stdlib:

```bash
cd evals
python check.py --validate     # структура набора
python check.py --selftest      # эталоны сами чисты (36/36)
python check.py --id ru-03 --text "ваш вывод скилла"
```

Подробности — в [`evals/README.md`](evals/README.md).

## Лицензия

MIT.

## Credits

Самостоятельная четырёхъязычная переработка (RU/UK/EN/DE) с собственным движком русизмов для украинского, движком Nominalstil→Verbalstil для немецкого и заточкой под маркетинговый текст. Идея очистки текста от AI-маркеров восходит к проекту [blader/humanizer](https://github.com/blader/humanizer) (MIT). Списки маркеров сверялись с [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) и [Wikipedia: Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) (CC BY-SA); немецкие маркеры и Nominalstil-примеры — по материалам [eology](https://www.eology.de/news/merkmale-von-chatgpt-typischen-texten-beim-ai-roundtable), [ContentConsultants](https://www.contentconsultants.de/ki-texte-erkennen-warum-man-texte-besser-selbst-schreibt/) и [WORTLIGA](https://wortliga.de/glossar/nominalstil/). Маркетинговые приёмы — по обзорам [Unbounce](https://unbounce.com/copywriting/conversion-copywriting/) и [Growth Method](https://growthmethod.com/conversion-copywriting/).
