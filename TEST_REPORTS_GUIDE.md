# Test Reports Visualization Guide

## Allure Report

**Allure Report** - это мощный инструмент для визуализации результатов тестирования с красивыми графиками и историей.

### 📊 Что показывает Allure:

- ✅ **Dashboard** - общая статистика, тренды успеха/неудачи
- 📈 **Timeline** - как долго выполнялись тесты
- 🐛 **Failures** - детали падения тестов
- 📑 **Test Cases** - все тесты с маркировкой по категориям
- 🏷️ **Features & Stories** - организация тестов по функциональности
- 📊 **Trends** - исторические графики

### 🚀 Как использовать:

#### **Локально:**
```bash
# Запустить тесты с генерацией Allure отчета
cd /path/to/Plan-Your-Study
pytest tests/ --alluredir=allure-results

# Установить Allure commandline
npm install -g allure-commandline

# Сгенерировать HTML отчет
allure generate allure-results -o allure-report --clean

# Открыть отчет в браузере
allure open allure-report
```

#### **В GitHub Actions:**
Отчеты автоматически генерируются и загружаются как artifacts:
1. Зайди на вкладку **Actions** в GitHub репозитории
2. Выбери последний запуск пайплайна
3. Скачай artifacts:
   - `test-reports-python-3.x` - Allure + Coverage отчеты
   - `playwright-report` - E2E тесты

### 📋 Категории тестов (маркеры):

```python
@pytest.mark.critical    # Критичные функции (auth, assignments)
@pytest.mark.auth        # Тесты аутентификации
@pytest.mark.courses     # Тесты курсов
@pytest.mark.assignments # Тесты заданий
@pytest.mark.subtasks    # Тесты подзадач
@pytest.mark.progress    # Тесты прогресса
@pytest.mark.integration # Integration тесты
@pytest.mark.unit        # Unit тесты
```

### 🔍 Интерпретация результатов:

| Метрика | Описание |
|---------|---------|
| Pass Rate | % успешных тестов (должен быть ≥95%) |
| Duration | Среднее время выполнения теста |
| Flaky | Нестабильные тесты (иногда падают) |
| Skipped | Пропущенные тесты |

### 📈 Тренды:

- **Green Line** ↑ - все тесты проходят
- **Red Spike** ↓ - произошла ошибка, нужно исправить

### 💡 Best Practices:

1. Проверяй отчеты после каждого Push
2. Ищи flaky тесты и fix их
3. Отслеживай trends - если Pass Rate падает, это тревога
4. Используй маркеры для быстрого поиска нужных тестов

### 🔗 Полезные команды:

```bash
# Запустить только критичные тесты
pytest -m critical

# Запустить только auth тесты
pytest -m auth

# Запустить только integration тесты
pytest -m integration

# Исключить медленные тесты
pytest -m "not slow"
```

---

## Coverage Report

**Coverage** показывает какой процент кода покрыт тестами.

- Требование: **≥80%** (установлено в пайплайне)
- Доступен в: `htmlcov/index.html` в artifacts

---

## Playwright Report

Для **E2E тестов** Playwright генерирует свой красивый отчет с:
- ✅ Скриншотами каждого шага
- 📹 Видео записью теста (если упал)
- ⏱️ Временем выполнения каждого шага
- 🔍 Трассировкой браузера

Доступен в artifacts: `playwright-report/index.html`
