# Artifact Registry

Реестр всех артефактов проекта с их идентификаторами и связями.

## Назначение

Этот документ служит центральным реестром всех архитектурных артефактов проекта. Он помогает:
- Отслеживать все созданные артефакты
- Понимать связи между артефактами
- Избегать дублирования идентификаторов
- Обеспечивать трассируемость требований

## Форматы идентификаторов

- **Feature:** `FEATURE-<number>` (например, `FEATURE-001`)
- **Screen:** `SCREEN-<number>` или `SCREEN-<name>` (например, `SCREEN-001` или `SCREEN-HOME`)
- **Behavior Slice:** `SLICE-<number>` или `SLICE-<descriptive-name>` (например, `SLICE-001` или `SLICE-LOAD-HOME`)

## Реестр артефактов

### Features

| ID | Название | Файл | Описание |
|---|---|---|---|
| `FEATURE-001` | Пример: Авторизация | `docs/features/auth.md` | Фича для входа и регистрации пользователей |

### Screens

| ID | Название | Feature ID | Файл | Описание |
|---|---|---|---|---|
| `SCREEN-001` | Login Screen | `FEATURE-001` | `docs/screens/login_state_machine.md` | Экран входа в приложение |

### Behavior Slices

| ID | Название | Feature ID | Screen ID | Файл | Описание |
|---|---|---|---|---|---|
| `SLICE-001` | Load Login Form | `FEATURE-001` | `SCREEN-001` | `docs/features/auth/behavior_slices.md` | Загрузка формы входа |

## Примеры связей между артефактами

### Пример 1: Feature → Screens → Slices

```
FEATURE-001 (Авторизация)
  ├── SCREEN-001 (Login Screen)
  │   ├── SLICE-001 (Load Login Form)
  │   └── SLICE-002 (Submit Login)
  └── SCREEN-002 (Registration Screen)
      └── SLICE-003 (Submit Registration)
```

### Пример 2: Traceability в Feature Spec

**Feature Spec (FEATURE-001):**
- Related Screens: `SCREEN-001`, `SCREEN-002`
- Related Use Cases: `AuthenticateUser`, `RegisterUser`
- Related API Contracts: `POST /auth/login`, `POST /auth/register`

### Пример 3: Traceability в Behavior Slice

**Behavior Slice (SLICE-001):**
- Feature ID: `FEATURE-001`
- Screen ID: `SCREEN-001`
- Related Slices: `SLICE-002` (зависит от загрузки формы)
- API Contract IDs: `POST /auth/login`

### Пример 4: Traceability в State Machine

**State Machine (SCREEN-001):**
- Feature ID: `FEATURE-001`
- Screen ID: `SCREEN-001`
- Related Use Cases: `AuthenticateUser`

## Правила ведения реестра

1. **При создании нового артефакта:**
   - Создайте запись в соответствующей таблице
   - Укажите все связи с другими артефактами
   - Обновите раздел "Примеры связей" при необходимости

2. **При удалении артефакта:**
   - Отметьте запись как удалённую (не удаляйте полностью)
   - Проверьте и обновите связи в других артефактах

3. **При изменении связей:**
   - Обновите соответствующие разделы Traceability в артефактах
   - Обновите этот реестр

## Проверка трассируемости

Для проверки полноты трассировки используйте скрипт валидации (см. `docs/validation_rules.md`), который проверяет:
- Наличие всех идентификаторов в реестре
- Корректность ссылок между артефактами
- Заполнение обязательных полей трассировки

