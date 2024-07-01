
class ort:
    def __init__(self,doc_numb ,p_name ,c_name):
        super().__init__()
        self.doc_numb =doc_numb
        self.p_name =p_name
        self.c_name =c_name

    def __repr__(self):
        return f"Номер документа {self.doc_numb} ,продавец {self.p_name},покупаетль {self.c_name}"
    def __eq__(self, other):
        if not isinstance(other ,ort):
            raise ValueError("Can't compare")
        return self.doc_numb==other.doc_numb and self.p_name==other.p_name and self.c_name==other.c_name


    def __setattr__(self, key, value):
        if key == 'doc_numb':
            if type(value) is not int:
                raise ValueError("Doc n must be float)")

        return super().__setattr__(key, value)


class b:
    result = 5

    def gr(func):
        def wrapper(re):
            res = 4
            func(re)
            return res

        return wrapper

    @gr
    def second(re):
        return type(re)





ort1 =ort(100 ,"Попов" ,'Бангонда')
ort2 =ort(101 ,"Попив" ,'Бангонда')


b.second()



