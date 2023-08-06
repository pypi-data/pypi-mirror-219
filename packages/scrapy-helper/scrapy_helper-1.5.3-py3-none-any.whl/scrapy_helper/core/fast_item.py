import scrapy


class FastItem(scrapy.Item):
    def __getitem__(self, key):
        return self._values.get(key, None)

    def __setitem__(self, key, value):
        self._values[key] = value

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

    def set(self, fields):
        """
        用来动态添加自定义属性
        """
        for field in fields:
            self.__setattr__(field, scrapy.Field())
            self.fields[field] = scrapy.Field()
