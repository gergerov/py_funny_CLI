import typing as tp


class ExceptionArgumentQuantity(Exception):
    pass


class KeyWord(object):

    def __init__(self, keyword: str) -> None:
        self.keyword: str = keyword
        self.position: int = -1

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.keyword}'

    @property
    def template(self) -> str:
        return self.keyword

    @property
    def short_template(self) -> str:
        return self.keyword


class CmdName(KeyWord):
    def __init__(self, keyword: str, description: str) -> None:
        super().__init__(keyword)
        self.description = description


class CmdOpt(KeyWord):
    # TODO проверка значения на тип, если тип указан
    # TODO лист возможных значений, как например 
    # опция 'Фон' может быть 'вкл' или 'выкл'
    # порт может быть только в диапазоне от 1000 до 65...
    # TODO регулярное выражение, как например для IP адреса или email-а
    
    def __init__(
            self, 
            keyword: str, 
            position: int,
            type: tp.Type,
            keyword_short: str=None, 
            starttag: str='', 
            equatetag: str='=',
            default: tp.Any=None
        ) -> None:
        super().__init__(keyword)
        if keyword_short is None:
            self.keyword_short: str = keyword
        else:
            self.keyword_short: str = keyword_short
        self.starttag: str = starttag
        self.equatetag: str = equatetag
        self.position = position
        self.type = type

    @property
    def len(self) -> int:
        return len(self.starttag) + len(self.keyword) + len(self.equatetag)
    
    @property
    def len_short(self) -> int:
        return len(self.starttag) + len(self.keyword_short) + len(self.equatetag)

    @property
    def template(self) -> str:
        return f'{self.starttag}{self.keyword}{self.equatetag}'
    
    @property
    def template_short(self) -> str:
        return f'{self.starttag}{self.keyword_short}{self.equatetag}'
    
    def get(self, text: str) -> dict:
        if text[:self.len].upper() == self.template.upper():
            return self.type(text[self.len:])
        elif text[:self.len_short].upper() == self.template_short.upper():      
            return self.type(text[self.len_short:])
        else:
            raise Exception('Использовать get только после метода its_me!')

    def its_me(self, text: str) -> bool:
        if text[:self.len].upper() == self.template.upper():
            return True
        elif text[:self.len_short].upper() == self.template_short.upper():      
            return True
        else:
            return False
    
    def its_me_by_position(self, position):
        return self.position == position
        
    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.starttag}{self.keyword}({self.keyword_short}){self.equatetag}...'


class CmdSequence(tp.List[CmdName | CmdOpt]):
    """
        Команда [Аргументы] [(key=value)]
    """
    def __init__(self, list: tp.List, *args, **kwargs):
        for item in list:
            if issubclass(item.__class__, KeyWord):
                self.append(item)
            else:
                raise Exception(f'{self.__class__.__name__} должен быть экзмепляром-потомка {KeyWord} ') 
        self.sort(key=lambda item: item.position, reverse=False)

    def __repr__(self) -> str:
        res = '['
        for item in self:
            res += "'" + str(item) + "', "
        res += ']'
        return res

    def help(self) -> str:
        str = ''
        for item in self:
            if isinstance(item, CmdName):
                str += f'\n\tКоманда: {item.keyword}'
                str += f'\n\tОписание: {item.description}'
            if isinstance(item, CmdOpt):
                str += f'\n\tОпция №{item.position}: {item.starttag}{item.keyword}'
                if item.keyword_short is not None:
                    str += f' (кратко {item.keyword_short})'
                    str += f'{item.equatetag}<значение> ({item.type})'
        str += '\n' + '-'*100
        return str 

    def parse(self, text: str) -> dict:
        words = text.split(' ')
        named = '=' in text
        command = words[0]
        options = {}

        words.remove(command)

        if named:
            for word in words:
                for item in self:
                    if isinstance(item, CmdOpt):
                        if item.its_me(word):
                            options[item.keyword] = item.get(word)

        else:
            for index, word in enumerate(words):
                for item in self:
                    if isinstance(item, CmdOpt):
                        if item.its_me_by_position(index):
                            options[item.keyword] = item.type(word)

        if len(options) != len(self) - 1:
            raise ExceptionArgumentQuantity(f'Должно быть опций: {len(self) - 1}. Определено : {len(options)} (Команда: {text})')

        result = {}
        result['name'] = command
        result['opt'] = options

        return result
