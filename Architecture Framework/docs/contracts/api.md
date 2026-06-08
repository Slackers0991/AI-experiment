# API Contracts (Mobile ↔ Backend)

<!-- ИНСТРУКЦИЯ ПО ЗАПОЛНЕНИЮ
Цель: Зафиксировать контракты взаимодействия с Backend API, правила маппинга DTO ↔ Domain и единую модель ошибок. Это источник правды для всех интеграций с внешними системами.

Когда заполнять: На Этапе 3.1 для каждой фичи, которая использует внешние API. Обновляется при изменении API или добавлении новых операций.

Исходные данные:
- OpenAPI/Swagger спецификация Backend API
- GraphQL schema (если используется)
- Документация внешних API
- Feature Spec (раздел "Источники данных")

Где брать:
- Backend команда (OpenAPI файлы, GraphQL schema)
- Документация внешних сервисов
- Postman коллекции
- Существующие интеграции (если есть)

Советы:
- Укажите конкретный источник правды (ссылка на файл, commit, версию schema)
- Операции должны быть сгруппированы по фичам для удобства навигации
- Правила маппинга DTO ↔ Domain критически важны — они определяют, как обрабатывать nullable поля, default значения
- Единая модель ошибок должна быть согласована с Error Model & UI Policy
- Golden samples должны быть реальными примерами ответов API (не выдуманными)
- Версионирование должно быть явным — как обрабатывать breaking changes
- Caching hints помогают определить стратегию кеширования в Feature Spec
-->

## 1. Источник правды
- GraphQL schema: <link/commit/artefact>
- OpenAPI: <link/commit/artefact>

## 2. Операции (по фичам)
### 2.1 <Feature>: <OperationName>
- request:
- response:
- pagination:
- caching hints:

## 3. DTO ↔ Domain: правила маппинга
- Nullable поля:
- Default значения:
- Отличие null vs пустой список:
- Версионирование:

## 4. Единая модель ошибок
### 4.1 Transport → Domain mapping
- 401/403 → AuthRequired
- no network → NetworkUnavailable
- timeout → Timeout
- 5xx → ServerError
- parse/unknown → Unknown

## 5. Golden samples
Список файлов в `docs/contracts/golden_samples/` и назначение каждого.
