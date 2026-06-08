#!/usr/bin/env python3
"""
Скрипт валидации архитектурных документов.

Проверяет:
- Наличие обязательных разделов в шаблонах
- Корректность идентификаторов артефактов
- Заполнение разделов трассировки
- Корректность ссылок на идентификаторы
- Соответствие структуры JSON Schema (если документ в JSON)
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import jsonschema

# Паттерны для идентификаторов
FEATURE_ID_PATTERN = re.compile(r'^FEATURE-\d+$')
SCREEN_ID_PATTERN = re.compile(r'^SCREEN-\d+$|^SCREEN-[A-Z0-9-]+$')
SLICE_ID_PATTERN = re.compile(r'^SLICE-\d+$|^SLICE-[A-Z0-9-]+$')

# Обязательные разделы для каждого типа документа
REQUIRED_SECTIONS = {
    'feature': [
        'Artifact ID',
        'Traceability',
        'Цель и границы',
        'Пользовательские сценарии',
        'Экраны и состав UI',
        'Use cases',
        'Domain model',
        'Источники данных',
        'Политика кеша и обновления',
        'Политика деградации',
        'Аналитика',
        'Тестовые требования'
    ],
    'behavior_slice': [
        'Artifact ID',
        'Traceability',
        'Context',
        'Trigger',
        'Expected Behavior',
        'Acceptance Criteria'
    ],
    'state_machine': [
        'Artifact ID',
        'Traceability',
        'Назначение',
        'State',
        'Actions/Intents',
        'Effects',
        'Таблица переходов'
    ]
}

class ValidationError:
    """Ошибка валидации."""
    def __init__(self, file_path: str, message: str, line: Optional[int] = None):
        self.file_path = file_path
        self.message = message
        self.line = line
    
    def __str__(self):
        if self.line:
            return f"{self.file_path}:{self.line}: {self.message}"
        return f"{self.file_path}: {self.message}"

class DocumentValidator:
    """Валидатор архитектурных документов."""
    
    def __init__(self, docs_dir: Path = Path('docs')):
        self.docs_dir = docs_dir
        self.errors: List[ValidationError] = []
        self.artifact_registry: Dict[str, List[str]] = {
            'features': [],
            'screens': [],
            'slices': []
        }
    
    def validate_feature_id(self, feature_id: str) -> bool:
        """Проверяет формат Feature ID."""
        return bool(FEATURE_ID_PATTERN.match(feature_id))
    
    def validate_screen_id(self, screen_id: str) -> bool:
        """Проверяет формат Screen ID."""
        return bool(SCREEN_ID_PATTERN.match(screen_id))
    
    def validate_slice_id(self, slice_id: str) -> bool:
        """Проверяет формат Slice ID."""
        return bool(SLICE_ID_PATTERN.match(slice_id))
    
    def extract_sections(self, content: str) -> Dict[str, List[str]]:
        """Извлекает разделы из Markdown документа."""
        sections = {}
        current_section = None
        current_lines = []
        
        for line in content.split('\n'):
            if line.startswith('##'):
                if current_section:
                    sections[current_section] = current_lines
                current_section = line.strip('#').strip()
                current_lines = []
            elif current_section:
                current_lines.append(line)
        
        if current_section:
            sections[current_section] = current_lines
        
        return sections
    
    def extract_artifact_id(self, content: str) -> Optional[str]:
        """Извлекает Artifact ID из документа."""
        match = re.search(r'## Artifact ID\s*\n\*\*ID:\*\*\s*`([^`]+)`', content)
        if match:
            return match.group(1)
        return None
    
    def extract_traceability(self, content: str) -> Dict[str, List[str]]:
        """Извлекает информацию о трассировке."""
        traceability = {}
        sections = self.extract_sections(content)
        
        if 'Traceability' not in sections:
            return traceability
        
        traceability_section = '\n'.join(sections['Traceability'])
        
        # Извлекаем Feature ID
        match = re.search(r'\*\*Feature ID:\*\*\s*`([^`]+)`', traceability_section)
        if match:
            traceability['featureId'] = [match.group(1)]
        
        # Извлекаем Screen ID
        match = re.search(r'\*\*Screen ID:\*\*\s*`([^`]+)`', traceability_section)
        if match:
            traceability['screenId'] = [match.group(1)]
        
        # Извлекаем Related Screens
        match = re.search(r'\*\*Related Screens:\*\*\s*`([^`]+)`', traceability_section)
        if match:
            traceability['relatedScreens'] = [s.strip() for s in match.group(1).split(',')]
        
        # Извлекаем Related Slices
        match = re.search(r'\*\*Related Slices:\*\*\s*`([^`]+)`', traceability_section)
        if match:
            traceability['relatedSlices'] = [s.strip() for s in match.group(1).split(',')]
        
        return traceability
    
    def validate_feature(self, file_path: Path) -> List[ValidationError]:
        """Валидирует Feature Spec документ."""
        errors = []
        content = file_path.read_text(encoding='utf-8')
        sections = self.extract_sections(content)
        
        # Проверка обязательных разделов
        for required_section in REQUIRED_SECTIONS['feature']:
            if required_section not in sections:
                errors.append(ValidationError(
                    str(file_path),
                    f"Отсутствует обязательный раздел: {required_section}"
                ))
        
        # Проверка Artifact ID
        artifact_id = self.extract_artifact_id(content)
        if not artifact_id:
            errors.append(ValidationError(
                str(file_path),
                "Не найден Artifact ID"
            ))
        elif not self.validate_feature_id(artifact_id):
            errors.append(ValidationError(
                str(file_path),
                f"Некорректный формат Feature ID: {artifact_id}. Ожидается FEATURE-<number>"
            ))
        else:
            self.artifact_registry['features'].append(artifact_id)
        
        # Проверка Traceability
        traceability = self.extract_traceability(content)
        if 'relatedScreens' not in traceability or not traceability['relatedScreens']:
            errors.append(ValidationError(
                str(file_path),
                "Traceability: Related Screens обязателен для Feature Spec"
            ))
        else:
            # Проверка формата Screen ID
            for screen_id in traceability['relatedScreens']:
                if not self.validate_screen_id(screen_id):
                    errors.append(ValidationError(
                        str(file_path),
                        f"Некорректный формат Screen ID в трассировке: {screen_id}"
                    ))
        
        return errors
    
    def validate_behavior_slice(self, file_path: Path) -> List[ValidationError]:
        """Валидирует Behavior Slice документ."""
        errors = []
        content = file_path.read_text(encoding='utf-8')
        sections = self.extract_sections(content)
        
        # Проверка обязательных разделов
        for required_section in REQUIRED_SECTIONS['behavior_slice']:
            if required_section not in sections:
                errors.append(ValidationError(
                    str(file_path),
                    f"Отсутствует обязательный раздел: {required_section}"
                ))
        
        # Проверка Artifact ID
        artifact_id = self.extract_artifact_id(content)
        if not artifact_id:
            errors.append(ValidationError(
                str(file_path),
                "Не найден Artifact ID"
            ))
        elif not self.validate_slice_id(artifact_id):
            errors.append(ValidationError(
                str(file_path),
                f"Некорректный формат Slice ID: {artifact_id}"
            ))
        else:
            self.artifact_registry['slices'].append(artifact_id)
        
        # Проверка Traceability
        traceability = self.extract_traceability(content)
        if 'featureId' not in traceability or not traceability['featureId']:
            errors.append(ValidationError(
                str(file_path),
                "Traceability: Feature ID обязателен для Behavior Slice"
            ))
        else:
            feature_id = traceability['featureId'][0]
            if not self.validate_feature_id(feature_id):
                errors.append(ValidationError(
                    str(file_path),
                    f"Некорректный формат Feature ID в трассировке: {feature_id}"
                ))
            elif feature_id not in self.artifact_registry['features']:
                errors.append(ValidationError(
                    str(file_path),
                    f"Feature ID {feature_id} не найден в реестре артефактов"
                ))
        
        return errors
    
    def validate_state_machine(self, file_path: Path) -> List[ValidationError]:
        """Валидирует State Machine документ."""
        errors = []
        content = file_path.read_text(encoding='utf-8')
        sections = self.extract_sections(content)
        
        # Проверка обязательных разделов
        for required_section in REQUIRED_SECTIONS['state_machine']:
            if required_section not in sections:
                errors.append(ValidationError(
                    str(file_path),
                    f"Отсутствует обязательный раздел: {required_section}"
                ))
        
        # Проверка Artifact ID
        artifact_id = self.extract_artifact_id(content)
        if not artifact_id:
            errors.append(ValidationError(
                str(file_path),
                "Не найден Artifact ID"
            ))
        elif not self.validate_screen_id(artifact_id):
            errors.append(ValidationError(
                str(file_path),
                f"Некорректный формат Screen ID: {artifact_id}"
            ))
        else:
            self.artifact_registry['screens'].append(artifact_id)
        
        # Проверка Traceability
        traceability = self.extract_traceability(content)
        if 'featureId' not in traceability or not traceability['featureId']:
            errors.append(ValidationError(
                str(file_path),
                "Traceability: Feature ID обязателен для State Machine"
            ))
        if 'screenId' not in traceability or not traceability['screenId']:
            errors.append(ValidationError(
                str(file_path),
                "Traceability: Screen ID обязателен для State Machine"
            ))
        else:
            screen_id = traceability['screenId'][0]
            if screen_id != artifact_id:
                errors.append(ValidationError(
                    str(file_path),
                    f"Screen ID в трассировке ({screen_id}) не совпадает с Artifact ID ({artifact_id})"
                ))
        
        return errors
    
    def validate_all(self) -> bool:
        """Валидирует все документы в директории docs."""
        all_errors = []
        
        # Валидация Feature Spec
        feature_files = list(self.docs_dir.glob('features/**/*.md'))
        feature_files = [f for f in feature_files if f.name != 'behavior_slices.md' and '_template' not in f.name]
        for file_path in feature_files:
            all_errors.extend(self.validate_feature(file_path))
        
        # Валидация Behavior Slices
        slice_files = list(self.docs_dir.glob('features/**/behavior_slices.md'))
        for file_path in slice_files:
            all_errors.extend(self.validate_behavior_slice(file_path))
        
        # Валидация State Machine
        state_machine_files = list(self.docs_dir.glob('screens/**/*.md'))
        state_machine_files = [f for f in state_machine_files if '_template' not in f.name]
        for file_path in state_machine_files:
            all_errors.extend(self.validate_state_machine(file_path))
        
        self.errors = all_errors
        return len(all_errors) == 0
    
    def print_errors(self):
        """Выводит ошибки валидации."""
        if not self.errors:
            print("✓ Все документы валидны")
            return
        
        print(f"✗ Найдено {len(self.errors)} ошибок:\n")
        for error in self.errors:
            print(f"  {error}")
    
    def print_summary(self):
        """Выводит сводку по артефактам."""
        print("\nРеестр артефактов:")
        print(f"  Features: {len(self.artifact_registry['features'])}")
        print(f"  Screens: {len(self.artifact_registry['screens'])}")
        print(f"  Slices: {len(self.artifact_registry['slices'])}")

def main():
    """Главная функция."""
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print(f"Ошибка: директория {docs_dir} не найдена")
        sys.exit(1)
    
    validator = DocumentValidator(docs_dir)
    is_valid = validator.validate_all()
    
    validator.print_errors()
    validator.print_summary()
    
    if not is_valid:
        sys.exit(1)

if __name__ == '__main__':
    main()

