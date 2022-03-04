import lief
from pathlib import Path

from core.AppLoader import AppLoader
from core.data.AppFileType import AppFileType
from core.Constants import BASE_PROTO_CLASS, BASE_PROTO_CLASS_PRETTY


"""
Usage:

lief_wrapper = LIEFWrapper()
lief_wrapper.load(Path('some.dex'), bin_type=AppFileType.DEX)
lief_wrapper = lief_wrapper.analyse()

strings = lief_wrapper.strings()
lief_wrapper.test_extends_class_methods_list(base_class='Lcom/example/app/MyClass;')
"""


class LIEFWrapper(AppLoader):
    """
    LIEF не видит полей классов (возможно, это проблема только Python Binding'а, в C++ либе вроде все есть)
    """
    lief_dex_file = None

    def analyse(self):
        # odex: lief.OAT.parse(self.path)
        """
        Запускаем анализ DEX-файла
        """

        if self.bin_type == AppFileType.DEX:
            self.lief_dex_file = lief.DEX.parse(self.path)

        return self

    def strings(self):
        """
        Вытаскиваем строки из DEX-файла
        """
        if self.lief_dex_file.strings:
            return [s for s in self.lief_dex_file.strings]
        
        return []

    def test_extends_class_methods_list(self, base_class: str = BASE_PROTO_CLASS):
        """
        Берет класс base_class
        Проверяет, расширяется ли base_class через BASE_PROTO_CLASS_PRETTY
        Если да, выводим все методы класса base_class
        """
        if self.lief_dex_file.has_class(base_class):
            lief_dex_class = self.lief_dex_file.get_class(base_class)

            if lief_dex_class.parent.pretty_name == BASE_PROTO_CLASS_PRETTY:
                for method in lief_dex_class.methods:
                    print(method)


