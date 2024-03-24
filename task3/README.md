# Описание решения

## Схема API

### Получение списка АЗС

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "AZS info",
    "version": "1.0.0"
  },
  "paths": {
    "/": {
      "get": {
        "operationId": "listAZS",
        "summary": "List AZS",
        "parameters": [
          {
            "name": "page",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "minimum": 1,
              "description": "Page number",
              "default": 1,
              "title": "Page"
            },
            "description": "Page number"
          },
          {
            "name": "size",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "maximum": 100,
              "minimum": 1,
              "default": 25,
              "title": "Size"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200 response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AZSList"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "AZSPrice": {
        "properties": {
          "name": {
            "type": "string",
            "title": "Name"
          },
          "price": {
            "type": "string",
            "title": "Price"
          },
          "currency": {
            "type": "string",
            "title": "Currency"
          },
          "image": {
            "type": "string",
            "title": "Image link"
          }
        }
      },
      "AZS": {
        "properties": {
          "id": {
            "type": "integer",
            "title": "Id"
          },
          "lat": {
            "type": "number",
            "title": "latitude" 
          },
          "lng": {
            "type": "number",
            "title": "longitude" 
          },
          "number": {
            "type": "string",
            "title": "Number"
          },
          "address": {
            "type": "string",
            "title": "Address"
          },
          "images_list": {
             "items": {
              "type": "string"
            },
            "type": "array",
            "title": "Images"
          },
          "additional_list": {
             "items": {
              "type": "string"
            },
            "type": "array",
            "title": "AdditionalServices"
          },
          "prices_list": {
             "items": {
              "$ref": "#/components/schemas/AZSPrice"
            },
            "type": "array",
            "title": "Prices"
          }
        },
        "type": "object",
        "title": "AZS"
      },
      "AZSList": {
        "properties": {
          "items": {
            "items": {
              "$ref": "#/components/schemas/AZS"
            },
            "type": "array",
            "title": "Items"
          },
          "total": {
            "type": "integer",
            "minimum": 0.0,
            "title": "Total"
          },
          "page": {
            "type": "integer",
            "minimum": 1.0,
            "title": "Page"
          },
          "size": {
            "type": "integer",
            "minimum": 1.0,
            "title": "Size"
          },
          "pages": {
            "type": "integer",
            "minimum": 0.0,
            "title": "Pages"
          }
        },
        "type": "object",
        "required": [
          "items",
          "total",
          "page",
          "size",
          "pages"
        ],
        "title": "AZSList"
      }
    }
  }
}
```

#### Notes:
1) Возможны два варианта реализации хранения и отображения цен: 
  - строка (как сейчас) - в этом случае получится сохранить максимальное соответствие исходным данным, однако, вся дальнейшая обработка перекладывается на Клиента
  - int - сохранение данных потребует дополнительной обработки на нашей стороне, но облегчит работу Клиентам
2) В основе реализованной спецификации лежит предположение о том, что API должно быть открытым. В случае необходимости аутентификации рекомендуется использовать: 
    - JWT-token - для Клиентов-пользователей при необходимости получать дополнительные данные 
    - Token-Based - для Клиентов-серверов (в случае работы сервер-сервер)


### Общая схема работы сервера

#### Django-based решение
Для реализации данного приложения предполагается использование DRF. 
Данные предполагается хранить в PostgreSQL.
Также, необходимы будут celery и rabbitMQ/redis (один на выбор). Выбор последнего опирается на уже имеющийся стек и способность сотрудников поддерживать тот или иной вариант. 

Решение предполагает использование DRF для реализации API описанного выше и связки celery+брокер для фоновых задач по обновлению данных. 
Для реализации обновления данных необходимо понимание временных ограничений. Предположительно, обновление данных по АЗС предполагается раз в сутки, в минимальные часы загрузки (чаще всего это полночь), обновление цен - раз в час. 

При необходимости поддержания более актуальных данных возможно увеличение частоты сбора данных с источников. Однако, надо понимать пропускную способность самого источника.
Также, имеет смысл поднять вопрос о реализации механизма webhook, для исключения частых запросов к Источнику. 

Плюсом данного решения будет встроенная в Django административная панель, позволяющая выполнить все указанные задачи и не требующая дополнительной разработки (front-end разработчиков)

Минусом является ресурсоемкость решения: приложение потребует больше вычислительных ресурсов в сравнении с альтернативными решениями, что особенно будет заметно при масштабировании. 


#### FastAPI-based решение

Данное решение аналогично предыдущему использует базу данных PostgreSQL и имеет такие же настройки для фоновых задач. 
Однако в качестве основного фреймворка для разработки предполагается использовать FastAPI, а для реализации фоновых задач рекомендуется rocketry.

Плюсом в сравнении с предыдущим решением будет меньшая потребность в ресурсах, а значит более легкая масштабируемость. 

Минусом является необходимость дополнительной разработки административной панели.
