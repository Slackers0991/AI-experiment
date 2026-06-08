# Implementation Hints Template

Шаблон с примерами заполнения раздела Implementation Hints для Behavior Slices.

## Назначение

Implementation Hints помогают ИИ:
- Генерировать код с правильной структурой файлов
- Использовать корректные имена классов и функций
- Соблюдать архитектурные границы
- Создавать тесты в правильных местах

## Примеры заполнения

### Пример 1: Простой slice загрузки данных

```markdown
### Implementation Hints

#### File Structure
- Domain: `features/home/domain/usecases/LoadHomeContentUseCase.kt`
- Data: `features/home/data/repositories/HomeRepositoryImpl.kt`
- Presentation: `features/home/presentation/HomeViewModel.kt`
- UI: `features/home/ui/HomeScreen.kt`

#### Class/Function Names
- Use Case: `LoadHomeContentUseCase`
- Repository interface: `HomeRepository`
- Repository implementation: `HomeRepositoryImpl`
- ViewModel: `HomeViewModel`
- State: `HomeState`
- UI Component: `HomeScreen`

#### Dependencies
- Core modules: `core:network`, `core:cache`
- External libraries: `retrofit`, `kotlinx-coroutines-core`

#### Test Structure
- Use Case test: `features/home/domain/usecases/LoadHomeContentUseCaseTest.kt`
- Repository test: `features/home/data/repositories/HomeRepositoryImplTest.kt`
- ViewModel test: `features/home/presentation/HomeViewModelTest.kt`
- UI test: `features/home/ui/HomeScreenTest.kt`
```

### Пример 2: Slice с зависимостью от другой фичи

```markdown
### Implementation Hints

#### File Structure
- Domain: `features/orders/domain/usecases/CreateOrderUseCase.kt`
- Data: `features/orders/data/repositories/OrderRepositoryImpl.kt`
- Presentation: `features/orders/presentation/OrderViewModel.kt`
- UI: `features/orders/ui/OrderScreen.kt`

#### Class/Function Names
- Use Case: `CreateOrderUseCase`
- Repository interface: `OrderRepository`
- Repository implementation: `OrderRepositoryImpl`
- ViewModel: `OrderViewModel`
- State: `OrderState`
- UI Component: `OrderScreen`

#### Dependencies
- Core modules: `core:network`, `core:cache`
- Other features: `features:auth:api` (для проверки авторизации)
- External libraries: `retrofit`, `kotlinx-coroutines-core`

#### Test Structure
- Use Case test: `features/orders/domain/usecases/CreateOrderUseCaseTest.kt`
- Repository test: `features/orders/data/repositories/OrderRepositoryImplTest.kt`
- ViewModel test: `features/orders/presentation/OrderViewModelTest.kt`
- UI test: `features/orders/ui/OrderScreenTest.kt`
```

### Пример 3: iOS (Swift) пример

```markdown
### Implementation Hints

#### File Structure
- Domain: `Features/Home/Domain/UseCases/LoadHomeContentUseCase.swift`
- Data: `Features/Home/Data/Repositories/HomeRepositoryImpl.swift`
- Presentation: `Features/Home/Presentation/HomeViewModel.swift`
- UI: `Features/Home/UI/HomeScreen.swift`

#### Class/Function Names
- Use Case: `LoadHomeContentUseCase`
- Repository protocol: `HomeRepository`
- Repository implementation: `HomeRepositoryImpl`
- ViewModel: `HomeViewModel`
- State: `HomeState`
- UI Component: `HomeScreen`

#### Dependencies
- Core modules: `CoreNetwork`, `CoreCache`
- External libraries: `Alamofire`, `Combine`

#### Test Structure
- Use Case test: `Features/Home/Domain/UseCases/LoadHomeContentUseCaseTests.swift`
- Repository test: `Features/Home/Data/Repositories/HomeRepositoryImplTests.swift`
- ViewModel test: `Features/Home/Presentation/HomeViewModelTests.swift`
- UI test: `Features/Home/UI/HomeScreenTests.swift`
```

## Правила заполнения

### File Structure
- Указывайте полные пути относительно корня проекта
- Используйте структуру директорий из `module-boundaries.md`
- Учитывайте платформу (Kotlin/Swift/TypeScript)

### Class/Function Names
- Используйте соглашения именования платформы (PascalCase для классов, camelCase для функций)
- Имена должны быть понятными и отражать назначение
- Следуйте паттернам из архитектуры проекта

### Dependencies
- Указывайте только реальные зависимости, которые будут использоваться
- Разделяйте core modules, other features и external libraries
- Используйте формат, принятый в проекте (Gradle/SwiftPM/npm)

### Test Structure
- Тесты должны находиться в тех же директориях, что и код
- Используйте суффиксы `Test` или `Tests` в зависимости от платформы
- Структура тестов должна повторять структуру кода

## Интеграция с ИИ

При генерации кода ИИ использует Implementation Hints для:
1. **Создания файлов** в правильных местах
2. **Именования классов** согласно указанным именам
3. **Добавления зависимостей** в правильные модули
4. **Создания тестов** в соответствующих директориях

Это обеспечивает соответствие сгенерированного кода архитектуре проекта.

