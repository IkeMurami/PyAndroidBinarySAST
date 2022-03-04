from pathlib import Path

from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis.analysis import Analysis
from androguard.core.analysis.analysis import ClassAnalysis

from androguard.misc import AnalyzeAPK

from androguard.decompiler.decompiler import DecompilerJADX

from core.AppLoader import AppLoader
from core.Constants import BASE_PROTO_CLASS


"""
Usage: 

androguard_wrapper = AndroGuardWrapper()
androguard_wrapper.load(Path('some.apk'))
androguard_wrapper = androguard_wrapper.analyse()

# Java/Kotlin:
# package my.example.package
# 
# import my.example.package.ParentClass
# 
# class MyClass extends ParentClass { ... }

class_analysis = androguard_wrapper.classAnalysis(base_class='Lmy/example/package/ParentClass;')
extend_classes_names = androguard_wrapper.extendClassNameList(class_analysis)
"""


class AndroGuardWrapper(AppLoader):
    """
    В терминах AndroGuard, '...Analysis' – объект, который предоставляет информацию об объекте и интерфейсы для получения более подробной информации обо всех элементах внутри 
    AndroGuard не может получить информацию о статических полях классов
    """
    apk_info = None
    dex_info_list = None
    apk_analysis = None

    def analyse(self):
        self.apk_info, self.dex_info_list, self.apk_analysis = AnalyzeAPK(self.path)

        return self

    def classAnalysis(self, base_class: str = BASE_PROTO_CLASS):
        """
        Получает Analysis-объект по имени класса (в Smali-нотации)
        """
        return self.apk_analysis.get_class_analysis(base_class)

    def extendClassList(self, class_analysis):
        """
        Находит все классы, которые расширяют класс, который обернут в Analysis-объект 'class_analysis'
        """

        res = list()

        if class_analysis:
            for classXref in class_analysis.get_xref_from():
                if classXref.extends == class_analysis.name:
                    res.append(classXref)
        else:
            print(f'Class not found :(')

        return res

    def extendClassNameList(self, class_analysis):
        """
        Все то же, что и `extendClassList(self, class_analysis)`, но вытаскивает имена классов
        """

        return [klass.name for klass in self.extendClassList(class_analysis)]

    def test_jadx(self):
        """
        Это базовый пример использования JADX через AndroGuard, но особо не тестил качество декомпиляции
        """
        apk_info = APK(self.path)
        d = DalvikVMFormat(apk_info)
        dx = Analysis(d)

        decompler = DecompilerJADX(d, dx)

        d.set_decompiler(decompler)
        d.set_vmanalysis(dx)

        klass = d.get_class(BASE_PROTO_CLASS)
        ...