# Система трассировки артефактов

Описание системы трассировки между архитектурными артефактами через идентификаторы.

## Назначение

Система трассировки позволяет:
- **Связать артефакты** между собой через явные идентификаторы
- **Отслеживать зависимости** между фичами, экранами и slices
- **Обеспечить полноту** проектирования (все связи явны)
- **Упростить работу с ИИ** — ИИ видит явные связи и не додумывает их

## Форматы идентификаторов

### Feature ID
- **Формат:** `FEATURE-<number>`
- **Примеры:** `FEATURE-001`, `FEATURE-002`
- **Где используется:** В начале Feature Spec

### Screen ID
- **Формат:** `SCREEN-<number>` или `SCREEN-<name>`
- **Примеры:** `SCREEN-001`, `SCREEN-HOME`, `SCREEN-LOGIN`
- **Где используется:** В начале State Machine

### Slice ID
- **Формат:** `SLICE-<number>` или `SLICE-<descriptive-name>`
- **Примеры:** `SLICE-001`, `SLICE-LOAD-HOME`, `SLICE-SUBMIT-LOGIN`
- **Где используется:** В каждом Behavior Slice

## Разделы трассировки в шаблонах

### Feature Spec

**Обязательные поля:**
- `Related Screens` — список всех экранов фичи
- `Related Use Cases` — список use cases из раздела 4
- `Related API Contracts` — список операций API

**Опциональные поля:**
- `Related Features` — если фича зависит от других фич

**Пример:**
```markdown
## Traceability
- **Related Features:** `FEATURE-002` (зависит от авторизации)
- **Related Screens:** `SCREEN-001`, `SCREEN-002`
- **Related Use Cases:** `LoadHomeContent`, `RefreshHomeContent`
- **Related API Contracts:** `GET /home`, `GET /home/refresh`
```

### Behavior Slice

**Обязательные поля:**
- `Feature ID` — к какой фиче относится slice
- `API Contract IDs` — какие операции API используются

**Опциональные поля:**
- `Screen ID` — если slice относится к конкретному экрану
- `Related Slices` — если есть зависимости от других slices

**Пример:**
```markdown
## Traceability
- **Feature ID:** `FEATURE-001` (обязательно)
- **Screen ID:** `SCREEN-001` (если применимо)
- **Related Slices:** `SLICE-002` (зависит от загрузки формы)
- **API Contract IDs:** `POST /auth/login`
```

### State Machine

**Обязательные поля:**
- `Feature ID` — к какой фиче относится экран
- `Screen ID` — идентификатор экрана (должен совпадать с Artifact ID)

**Опциональные поля:**
- `Related Use Cases` — список use cases, реализуемых на экране

**Пример:**
```markdown
## Traceability
- **Feature ID:** `FEATURE-001` (обязательно)
- **Screen ID:** `SCREEN-001` (обязательно)
- **Related Use Cases:** `AuthenticateUser`
```

## Примеры заполнения

### Пример 1: Простая фича с одним экраном

**Feature Spec (FEATURE-001):**
```markdown
## Artifact ID
**ID:** `FEATURE-001`

## Traceability
- **Related Screens:** `SCREEN-001`
- **Related Use Cases:** `AuthenticateUser`
- **Related API Contracts:** `POST /auth/login`
```

**State Machine (SCREEN-001):**
```markdown
## Artifact ID
**ID:** `SCREEN-001`

## Traceability
- **Feature ID:** `FEATURE-001`
- **Screen ID:** `SCREEN-001`
- **Related Use Cases:** `AuthenticateUser`
```

**Behavior Slice (SLICE-001):**
```markdown
## Slice SLICE-001
**Slice ID:** `SLICE-001`

## Traceability
- **Feature ID:** `FEATURE-001`
- **Screen ID:** `SCREEN-001`
- **API Contract IDs:** `POST /auth/login`
```

### Пример 2: Фича с несколькими экранами и зависимостями

**Feature Spec (FEATURE-002):**
```markdown
## Artifact ID
**ID:** `FEATURE-002`

## Traceability
- **Related Features:** `FEATURE-001` (требует авторизации)
- **Related Screens:** `SCREEN-002`, `SCREEN-003`
- **Related Use Cases:** `LoadHomeContent`, `RefreshHomeContent`, `NavigateToDetail`
- **Related API Contracts:** `GET /home`, `GET /home/refresh`, `GET /item/{id}`
```

**Behavior Slice (SLICE-002):**
```markdown
## Slice SLICE-002
**Slice ID:** `SLICE-002`

## Traceability
- **Feature ID:** `FEATURE-002`
- **Screen ID:** `SCREEN-002`
- **Related Slices:** `SLICE-003` (зависит от загрузки контента)
- **API Contract IDs:** `GET /home`, `GET /home/refresh`
```

## Правила заполнения

### Обязательные правила

1. **Все идентификаторы должны быть уникальными** в рамках проекта
2. **Feature ID обязателен** во всех Behavior Slices и State Machines
3. **Screen ID в State Machine** должен совпадать с Artifact ID
4. **Все ссылки должны быть валидными** — идентификаторы должны существовать в реестре

### Рекомендации

1. **Используйте описательные имена** для Slice ID, когда это помогает пониманию (например, `SLICE-LOAD-HOME`)
2. **Обновляйте реестр артефактов** при создании новых артефактов
3. **Проверяйте трассировку** перед коммитом (используйте скрипт валидации)

## Проверка трассировки

### Автоматическая проверка

Используйте скрипт валидации (`scripts/validate_docs.py`), который проверяет:
- Наличие обязательных полей трассировки
- Корректность формата идентификаторов
- Существование ссылок на другие артефакты
- Соответствие идентификаторов в реестре

### Ручная проверка

Перед коммитом убедитесь:
1. Все обязательные поля трассировки заполнены
2. Идентификаторы соответствуют формату
3. Все ссылки на другие артефакты валидны
4. Реестр артефактов обновлён

## Интеграция с ИИ

Система трассировки помогает ИИ:
- **Видеть явные связи** между артефактами
- **Не додумывать зависимости** — все связи указаны явно
- **Генерировать корректный код** — понимает контекст через идентификаторы
- **Соблюдать архитектурные границы** — видит, к какой фиче относится код

## Связанные документы

- [Artifact Registry](artifacts.md) — реестр всех артефактов
- [Validation Rules](../validation_rules.md) — правила валидации документов
- [Quality Gates](../quality/quality_gates.md) — проверки качества

