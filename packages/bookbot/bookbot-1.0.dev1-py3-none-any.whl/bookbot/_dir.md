面向开发者的目录介绍 :: `bookbot/src/bookbot/`
======

目录结构
------

```
bookbot/
+---cli/
+---gui/
+---book/
+---bot/
+---storage/
+---__init__.py
```

### 子目录

- `cli/` ：基于 [textual](https://textual.textualize.io/) 的命令行界面支持
- `gui/` ：基于 [fastapi](https://fastapi.tiangolo.com) 的图形用户界面支持
- `book/` ：数据模型，提供 `Book` 类
- `bot/` ：爬虫
- `storage/` ：存储后端

### 文件

+ `__init__.py`
