По дефолту запускается на browserstack

Дефолт запускается по команде `pytest`

Возможные варианты запуска:
```bash
pytest --context=bstack
pytest --context=local_real
pytest --context=local_emulator
```

Для локального appium требуется запуск сервера с командой: `appium --base-path /wd/hub`
