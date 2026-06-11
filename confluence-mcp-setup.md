# Настройка Confluence MCP для Claude Code

Интеграция позволяет Claude Code читать, искать и создавать страницы в Confluence напрямую из чата.

---

## Шаг 1 — Получить API токен Atlassian

1. Перейти на https://id.atlassian.com/manage-profile/security/api-tokens
2. Нажать **Create API token**
3. Дать название, например `claude-code`
4. Скопировать токен и сохранить — он показывается только один раз

---

## Шаг 2 — Установить Python (если нет)

Проверить:
```bash
python --version
```

Если не установлен — скачать с https://python.org/downloads (добавить в PATH при установке).

---

## Шаг 3 — Установить uv

```bash
pip install uv
```

Проверить:
```bash
python -m uv --version
```

---

## Шаг 4 — Установить mcp-atlassian

```bash
python -m uv tool install mcp-atlassian
```

Проверить — должен появиться файл:
```
C:\Users\<username>\.local\bin\mcp-atlassian.exe
```

---

## Шаг 5 — Добавить MCP сервер в Claude Code

Открыть файл `C:\Users\<username>\.claude.json` в любом редакторе и добавить секцию `mcpServers` перед полем `oauthAccount`:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "mcp-atlassian",
      "args": [],
      "env": {
        "CONFLUENCE_URL": "https://<subdomain>.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your-email@company.com",
        "CONFLUENCE_API_TOKEN": "your-token-here"
      }
    }
  },
  "oauthAccount": { ... }
}
```

Подставить:
- `<subdomain>` — название компании в Atlassian (обычно совпадает с доменом email)
- `your-email@company.com` — рабочий email
- `your-token-here` — токен из шага 1

---

## Шаг 6 — Проверить подключение

Выполнить в терминале (подставить свои данные):

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -u "your-email@company.com:your-token-here" \
  "https://<subdomain>.atlassian.net/wiki/rest/api/space?limit=1"
```

Ожидаемый ответ: `200`

---

## Шаг 7 — Перезапустить Claude Code

Закрыть и открыть заново. После перезапуска MCP сервер `atlassian` будет доступен автоматически.

---

## Проверка работы

В чате с Claude написать:
- `список пространств в Confluence`
- `найди страницы по теме "onboarding"`
- `прочитай страницу "Home" из пространства DEV`

---

## Возможности mcp-atlassian

| Действие | Пример запроса |
|---|---|
| Поиск страниц | "найди страницы про деплой" |
| Чтение страницы | "открой страницу X" |
| Создание страницы | "создай страницу Y в пространстве Z" |
| Редактирование | "обнови страницу X, добавь раздел..." |
| Список пространств | "покажи все пространства" |
| Комментарии | "добавь комментарий к странице X" |

---

## Устранение проблем

**`mcp-atlassian` не найден после установки**

Добавить `C:\Users\<username>\.local\bin` в переменную PATH:
- Win + R → `sysdm.cpl` → Дополнительно → Переменные среды → Path → Изменить → Добавить путь

**HTTP 401 при проверке**

Токен неверный или устарел. Сгенерировать новый на https://id.atlassian.com/manage-profile/security/api-tokens

**HTTP 404 при проверке**

Неверный subdomain. Проверить URL своего Confluence в браузере — subdomain это часть между `https://` и `.atlassian.net`.

**MCP сервер не появляется в Claude Code**

Проверить что JSON в `.claude.json` валиден (нет лишних запятых, скобки закрыты). Перезапустить Claude Code.
