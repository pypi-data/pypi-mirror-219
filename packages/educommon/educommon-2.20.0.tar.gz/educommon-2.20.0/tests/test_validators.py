# coding: utf-8
u"""Unit-тесты для валидаторов простых полей модели Django."""
from __future__ import absolute_import

from unittest import TestCase

from django.core.exceptions import ValidationError

from educommon.django.db.validators.simple import doc_type_validator
from educommon.django.db.validators.simple import inn10_validator
from educommon.django.db.validators.simple import inn12_validator
from educommon.django.db.validators.simple import inn_validator
from educommon.django.db.validators.simple import is_doc_type_valid
from educommon.django.db.validators.simple import is_inn10_valid
from educommon.django.db.validators.simple import is_inn12_valid
from educommon.django.db.validators.simple import is_inn_valid
from educommon.django.db.validators.simple import is_snils_valid
from educommon.django.db.validators.simple import snils_validator


class SnilsValidatorTestCase(TestCase):

    """Тесты для валидатора СНИЛС."""

    def test_valid_snils(self):
        """Проверка правильности обработки корректных СНИЛС."""
        valid_snils_list = (
            u'000-000-111 00',  # < 001-001-998
            u'111-223-555 88',  # sum < 100
            u'211-223-655 00',  # sum == 100
            u'211-223-656 00',  # sum == 101
            u'231-223-655 15',  # sum > 101, mod < 100
            u'871-223-654 00',  # sum > 101, mod == 100
        )

        for snils in valid_snils_list:
            snils_validator(snils)
            self.assertTrue(is_snils_valid(snils), snils)

    def test_invalid_snils(self):
        """Проверка правильности обработки некорректных СНИЛС."""
        valid_snils_list = (
            u'00000011100',
            u'daskjbn',
            u'111-223-555 81',
            u'211-223-655 01',
            u'211-223-656 01',
            u'231-223-655 11',
            u'871-223-654 01',
        )

        for snils in valid_snils_list:
            self.assertRaises(ValidationError, snils_validator, snils)
            self.assertFalse(is_snils_valid(snils), snils)


class InnValidatorTestCase(TestCase):

    """Тесты для валидаторов ИНН."""

    def test_valid_inn(self):
        """Проверка правильности обработки корректных ИНН."""
        valid_inn_list = (
            '1655148257',  # БАРС Груп
            '7707083893',  # Сбербанк
            '7830002293',  # ИНН ЮЛ из Википедии
            '500100732259',  # ИНН ФЛ из Википедии
        )

        for inn in valid_inn_list:
            inn_validator(inn)
            self.assertTrue(is_inn_valid(inn))
            if len(inn) == 10:
                inn10_validator(inn)
                self.assertTrue(is_inn10_valid(inn))
            else:
                inn12_validator(inn)
                self.assertTrue(is_inn12_valid(inn))

    def test_invalid_snils(self):
        """Проверка правильности обработки некорректных ИНН."""
        invalid_inn_list = (
            '1655148256',
            '7707083892',
            '7830002292',
            '500100732258',
        )

        for inn in invalid_inn_list:
            self.assertRaises(ValidationError, inn_validator, inn)
            self.assertFalse(is_inn_valid(inn))
            if len(inn) == 10:
                self.assertRaises(ValidationError, inn10_validator, inn)
                self.assertFalse(is_inn10_valid(inn))
            else:
                self.assertRaises(ValidationError, inn_validator, inn)
                self.assertFalse(is_inn12_valid(inn))


class DocumentTypeValidatorTestCase(TestCase):
    """Тесты для валидатора тип документа."""

    def test_valid_snils(self):
        """Проверка правильности обработки корректных типов документа."""
        valid_doc_type_list = (
            u'Свидетельство о рождении',
            u'Паспорт гражданина РФ',
            u'Другой документ, удостоверяющий личность',
            u'Временное удостоверение личности гражданина РФ',
            u'Паспорт иностранного гражданина',
            u'Загранпаспорт гражданина РФ',
            u'Военный билет',
            u'Дипломатический паспорт гражданина Российской Федерации',
            u'Паспорт гражданина СССР',
            u'Паспорт Минморфлота',
            u'Паспорт моряка',
            u'Разрешение на временное проживание в Российской Федерации',
            u'Свидетельство о рассмотрении ходатайства о признании беженцем '
            u'на территории Российской Федерации',
            u'Свидетельство о рождении, выданное уполномоченным органом '
            u'иностранного государства',
            u'Справка об освобождении из места лишения свободы',
            u'Удостоверение личности лица, признанного беженцем',
            u'Удостоверение личности офицера',
            u'Удостоверение личности военнослужащего РФ',
            u'Временное удостоверение, выданное взамен военного билета',
            u'Удостоверение личности лица без гражданства в РФ',
            u'Удостоверение личности отдельных категорий лиц, находящихся '
            u'на территории РФ, подавших заявление о признании гражданами '
            u'РФ или о приеме в гражданство РФ',
            u'Удостоверение личности лица, ходатайствующего о признании '
            u'беженцем на территории РФ',
            u'Удостоверение личности лица, получившего временное убежище '
            u'на территории РФ',
            u'Вид на жительство в Российской Федерации',
            u'Свидетельство о предоставлении временного убежища на '
            u'территории Российской Федерации',
            u'а',
            u'абв',  # одно слово
            u'абв абв',  # один пробел
            u'абв, абв',  # запятая
            u'абв абв абв',  # три слова
            u'абв, абв, абв',  # три слова через запятую
            u'АБВ',
            u'АБВ АБВ',
            u'АБВ, АБВ',
            u'АБВ АБВ АБВ',
            u'АБВ, АБВ, АБВ',
        )

        for doc_type in valid_doc_type_list:
            doc_type_validator(doc_type)
            self.assertTrue(is_doc_type_valid(doc_type), doc_type)

    def test_invalid_doc_type(self):
        """Проверка правильности обработки некорректных типов документа."""
        invalid_doc_type_list = (
            u'00000011100',  # цифры
            u'daskjbn',  # латиница нижний регистр
            u'DASKJBN',  # латиница верхний регистр
            u'!*%',  # недопустимые символы
            u'абв  абв',  # два пробела
            u' абв абв',  # пробел в начале
            u'абв абв абв ',  # пробел в конце
            u'абв , абв',  # пробел до запятой
        )

        for doc_type in invalid_doc_type_list:
            self.assertRaises(ValidationError, doc_type_validator, doc_type)
            self.assertFalse(is_doc_type_valid(doc_type), doc_type)
