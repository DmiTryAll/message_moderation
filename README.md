# Message Moderation

## Tables

### ignored_message

| Tags | Column |
| :--: | :----: |
| PK+  |   id   |
|  NN  |  text  |

### skiped_message

| Tags | Column |
| :--: | :----: |
|  PK  |   id   |

### Designation

- PK - primary key
- \+ - autoincrement
- NN - not null

## Start

```bash
pip install poetry
poetry install
make postgres
make run
```
