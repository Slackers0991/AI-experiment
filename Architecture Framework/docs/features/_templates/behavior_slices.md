# Behavior Slices — <FeatureName>

## Artifact ID
**Format:** `SLICE-<number>` или `SLICE-<descriptive-name>` (например, `SLICE-001` или `SLICE-LOAD-HOME`)  
**ID:** `SLICE-<number>`

## JSON Schema
Для валидации структуры документа используйте JSON Schema: [`docs/schemas/behavior_slice.schema.json`](../../schemas/behavior_slice.schema.json)

## Traceability
**Обязательно заполнить все поля трассировки для связи с другими артефактами.**

- **Feature ID:** `FEATURE-<id>` (обязательно)
- **Screen ID:** `SCREEN-<id>` (если slice относится к конкретному экрану)
- **Related Slices:** `SLICE-<id>` (список связанных slices, если есть зависимости)
- **API Contract IDs:** `<operation-name>` (список операций API, используемых в slice)

<!-- ИНСТРУКЦИЯ ПО ЗАПОЛНЕНИЮ
Цель: Разбить фичу на минимальные вертикальные срезы поведения для управляемой разработки. Behavior Slice — идеальная единица работы для ИИ и разработчиков.

Когда заполнять: После создания Feature Spec и State Machine (если требуется) на Этапе 4.1. Обновляется при изменении плана разработки.

Исходные данные:
- Feature Spec (все разделы)
- Screen State Machine (если есть)
- User Stories из Feature Spec
- Приоритеты фичи

Где брать:
- Feature Spec (этап 2.1)
- Screen State Machine (этап 2.2, если создан)
- Product Backlog (приоритеты)
- Обсуждения с командой о порядке разработки

Советы:
- **Обязательно заполните раздел Traceability** — укажите Feature ID и другие связанные идентификаторы
- **Заполните Implementation Hints** — это поможет ИИ сгенерировать корректный код с правильной структурой
- Каждый slice должен быть минимальным и завершённым — его можно реализовать и протестировать независимо
- Context должен описывать предусловия явно (например, "пользователь авторизован", "данные закешированы")
- Trigger должен быть конкретным событием (например, "пользователь открыл экран", "pull-to-refresh")
- Expected Behavior должно быть наблюдаемым и проверяемым
- State Coverage должно ссылаться на конкретные состояния из State Machine
- Degradation Rules должны быть явными — что показываем при ошибке, что скрываем
- Out of Scope критически важен — явно укажите, что НЕ входит в этот slice
- Acceptance Criteria должны быть в формате Given/When/Then и проверяемыми тестами
- Implementation Hints должны быть конкретными — укажите точные имена классов и расположение файлов
- Используйте идентификаторы в Related Artifacts (из раздела Traceability)
- Упорядочивайте slices по приоритету (P0, P1, P2)
- Slice ID может быть простым номером (SLICE-001) или описательным (SLICE-LOAD-HOME)
-->

Этот документ фиксирует **минимальные вертикали поведения**, используемые для планирования разработки и работы с ИИ.
Slices выводятся из Feature Spec и State Machine.

---

## Slice <SLICE-ID>
**Slice ID:** `<SLICE-ID>` (например, `SLICE-001` или `SLICE-LOAD-HOME`)  
Priority: P0 / P1 / P2

### Context
Предусловия:
- ...

### Trigger
Событие, инициирующее поведение:
- ...

### Expected Behavior
Что система должна сделать:
- ...

### State Coverage
Какие состояния/переходы покрываются:
- ...

### Degradation Rules
Как ведём себя при ошибках/частичной доступности:
- ...

### Out of Scope
Что **не** входит в этот slice:
- ...

### Acceptance Criteria (Given / When / Then)
- Given ...
- When ...
- Then ...

### Implementation Hints
**Укажите детали реализации для генерации кода ИИ.**

#### File Structure
Расположение файлов по слоям:
- Domain: `features/<feature>/domain/usecases/<UseCaseName>.kt` (или `.swift`, `.ts`)
- Data: `features/<feature>/data/repositories/<RepositoryName>Impl.kt`
- Presentation: `features/<feature>/presentation/<ScreenName>ViewModel.kt`
- UI: `features/<feature>/ui/<ScreenName>Screen.kt`

#### Class/Function Names
- Use Case: `<UseCaseName>` (например, `LoadHomeContentUseCase`)
- Repository interface: `<RepositoryName>` (например, `HomeRepository`)
- Repository implementation: `<RepositoryName>Impl`
- ViewModel: `<ScreenName>ViewModel`
- State: `<ScreenName>State`
- UI Component: `<ScreenName>Screen`

#### Dependencies
Зависимости от других модулей:
- Core modules: `core:network`, `core:cache`
- Other features: `features:<feature-name>:api` (если есть публичный API)
- External libraries: `retrofit`, `coroutines` (примеры)

#### Test Structure
Структура тестов:
- Use Case test: `features/<feature>/domain/usecases/<UseCaseName>Test.kt`
- Repository test: `features/<feature>/data/repositories/<RepositoryName>ImplTest.kt`
- ViewModel test: `features/<feature>/presentation/<ScreenName>ViewModelTest.kt`
- UI test: `features/<feature>/ui/<ScreenName>ScreenTest.kt`

### Related Artifacts
**Используйте идентификаторы из раздела Traceability выше.**

- Feature Spec: `FEATURE-<id>` (указан в Traceability)
- State Machine: `SCREEN-<id>` (если применимо, указан в Traceability)
- API Contract: `<operation-name>` (указан в Traceability)
