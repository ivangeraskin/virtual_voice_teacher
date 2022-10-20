Репозиторий сервиса "Виртуальный преподаватель ораторского искусства". 

В папке src/tg код телеграм бота, в src/ml - ML часть проекта. Каждый компонент станет микросервисом, который будет отвечать за свою часть работы.

В папке notebooks - эксперименты и наработки. Для каждого эксперимента создаем папку вида AB-N-feature_name, где AB - инициалы автора, N - номер эксперимента автора (1, 2, 3..), а feature_name - краткое имя эксперимента.
  
Предпочтительнее отправлять merge request, а не делать пуш в main. И в main стоит отправлять только то, что действительно потребуется в проде. Если выполненный эксперимент не является источником для чего-либо важного в main, то лучше оставим код эксперимента в ветке, без merge request в main.
