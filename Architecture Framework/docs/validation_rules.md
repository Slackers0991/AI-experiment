# Правила валидации архитектурных документов

Описание правил валидации структуры и трассировки архитектурных документов.

## Назначение

Правила валидации обеспечивают:
- **Корректность структуры** документов
- **Полноту трассировки** между артефактами
- **Соблюдение форматов** идентификаторов
- **Консистентность** связей между документами

## Использование скрипта валидации

### Локальная проверка

```bash
python scripts/validate_docs.py
```

### Интеграция в CI

Скрипт должен выполняться в CI pipeline перед merge. Пример для GitHub Actions:

```yaml
- name: Validate documentation
  run: python scripts/validate_docs.py
```

## Правила валидации

### 1. Обязательные разделы

Каждый тип документа должен содержать обязательные разделы:

#### Feature Spec
- ✅ `Artifact ID` — идентификатор фичи
- ✅ `Traceability` — раздел трассировки
- ✅ `Цель и границы`
- ✅ `Пользовательские сценарии`
- ✅ `Экраны и состав UI`
- ✅ `Use cases`
- ✅ `Domain model`
- ✅ `Источники данных`
- ✅ `Политика кеша и обновления`
- ✅ `Политика деградации`
- ✅ `Аналитика`
- ✅ `Тестовые требования`

#### Behavior Slice
- ✅ `Artifact ID` — идентификатор slice
- ✅ `Traceability` — раздел трассировки
- ✅ `Context` — предусловия
- ✅ `Trigger` — событие
- ✅ `Expected Behavior` — ожидаемое поведение
- ✅ `Acceptance Criteria` — критерии приёмки

#### State Machine
- ✅ `Artifact ID` — идентификатор экрана
- ✅ `Traceability` — раздел трассировки
- ✅ `Назначение`
- ✅ `State` — состояния
- ✅ `Actions/Intents` — действия
- ✅ `Effects` — побочные эффекты
- ✅ `Таблица переходов`

### 2. Форматы идентификаторов

#### Feature ID
- **Формат:** `FEATURE-<number>`
- **Примеры:** `FEATURE-001`, `FEATURE-002`
- **Паттерн:** `^FEATURE-\d+$`

#### Screen ID
- **Формат:** `SCREEN-<number>` или `SCREEN-<name>`
- **Примеры:** `SCREEN-001`, `SCREEN-HOME`, `SCREEN-LOGIN`
- **Паттерн:** `^SCREEN-\d+$|^SCREEN-[A-Z0-9-]+$`

#### Slice ID
- **Формат:** `SLICE-<number>` или `SLICE-<descriptive-name>`
- **Примеры:** `SLICE-001`, `SLICE-LOAD-HOME`, `SLICE-SUBMIT-LOGIN`
- **Паттерн:** `^SLICE-\d+$|^SLICE-[A-Z0-9-]+$`

### 3. Обязательные поля трассировки

#### Feature Spec
- ✅ `Related Screens` — список всех экранов фичи (обязательно)
- ⚪ `Related Features` — связанные фичи (опционально)
- ⚪ `Related Use Cases` — список use cases (опционально)
- ⚪ `Related API Contracts` — список операций API (опционально)

#### Behavior Slice
- ✅ `Feature ID` — идентификатор фичи (обязательно)
- ⚪ `Screen ID` — идентификатор экрана (если применимо)
- ⚪ `Related Slices` — связанные slices (опционально)
- ⚪ `API Contract IDs` — операции API (опционально)

#### State Machine
- ✅ `Feature ID` — идентификатор фичи (обязательно)
- ✅ `Screen ID` — идентификатор экрана (обязательно, должен совпадать с Artifact ID)
- ⚪ `Related Use Cases` — список use cases (опционально)

### 4. Правила ссылок

#### Валидность ссылок
- Все идентификаторы, указанные в трассировке, должны существовать в реестре артефактов
- Feature ID в Behavior Slice должен существовать в реестре
- Screen ID в State Machine должен совпадать с Artifact ID

#### Формат ссылок
- Используйте идентификаторы в формате, указанном в разделе "Форматы идентификаторов"
- Не используйте текстовые ссылки вместо идентификаторов
- Все ссылки должны быть явными и проверяемыми

### 5. Соответствие JSON Schema

Если документ представлен в формате JSON, он должен соответствовать соответствующей JSON Schema:

- Feature Spec → [`docs/schemas/feature.schema.json`](schemas/feature.schema.json)
- Behavior Slice → [`docs/schemas/behavior_slice.schema.json`](schemas/behavior_slice.schema.json)
- State Machine → [`docs/schemas/state_machine.schema.json`](schemas/state_machine.schema.json)

## Примеры ошибок валидации

### Ошибка 1: Отсутствует обязательный раздел

```
docs/features/auth.md: Отсутствует обязательный раздел: Traceability
```

**Решение:** Добавьте раздел `## Traceability` в документ.

### Ошибка 2: Некорректный формат идентификатора

```
docs/features/auth.md: Некорректный формат Feature ID: FEATURE-AUTH. Ожидается FEATURE-<number>
```

**Решение:** Измените идентификатор на формат `FEATURE-001`.

### Ошибка 3: Незаполненное обязательное поле трассировки

```
docs/features/auth/behavior_slices.md: Traceability: Feature ID обязателен для Behavior Slice
```

**Решение:** Добавьте `Feature ID` в раздел Traceability.

### Ошибка 4: Некорректная ссылка

```
docs/features/auth/behavior_slices.md: Feature ID FEATURE-999 не найден в реестре артефактов
```

**Решение:** Укажите существующий Feature ID или создайте соответствующий Feature Spec.

### Ошибка 5: Несовпадение Screen ID

```
docs/screens/login_state_machine.md: Screen ID в трассировке (SCREEN-002) не совпадает с Artifact ID (SCREEN-001)
```

**Решение:** Убедитесь, что Screen ID в трассировке совпадает с Artifact ID.

## Автоматическая проверка

### Локально перед коммитом

```bash
# Проверка всех документов
python scripts/validate_docs.py

# Если есть ошибки, исправьте их перед коммитом
```

### В CI pipeline

Скрипт валидации должен выполняться автоматически при каждом PR и блокировать merge при наличии ошибок.

## Интеграция с качеством

Валидация документов является частью Quality Gates (см. [`docs/quality/quality_gates.md`](quality/quality_gates.md)) и должна:
- ✅ Выполняться автоматически в CI
- ✅ Блокировать merge при ошибках
- ✅ Быть быстрой (не замедлять разработку)
- ✅ Выдавать понятные сообщения об ошибках

## Связанные документы

- [Traceability System](_meta/traceability.md) — описание системы трассировки
- [Artifact Registry](_meta/artifacts.md) — реестр артефактов
- [Quality Gates](quality/quality_gates.md) — настройки проверок качества

