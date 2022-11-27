Парсер хх

Парсер собирает вакансии с хх по запросам 
"авто тестировщик питон" 
"разработчик ios"

В поиске хх попадается очень много посторонних вакансий. 

Первая фильтрация - по заголовкам вакансий. Исключаются вакансии из выборки с помощью минус слов, 
которые находятся в файле /files/minus_lists.py в словарях с title в названии. 
При желании можно добавлять или удалять слова из списка. 

Вторая фильтрация - по содержанию. Так же, с помощью минус слов, которые находятся в файле /files/minus_lists.py
в словарях с context в названии, исключаются вакансии из выборки.

Третья фильтрация - удаление дублей. 
    Проверка заголовка+работодотель. Если совпали, то проверяется содержание. 
    Если содержание совпадает, то вакансия удаляется.

Четвертая фильтрация - по работодателю. Если вы не хотите, чтобы парсер откликнулся вашему нынешнему работодателю,
то лучше добавить работодателя в список минус слов с названием employer. 

Сортировка. 
**Сортировка 1** - по ЗП, от большей к меньшей. Затем удаление дублей.
    Этот результат выводится в файл hh_2022_salary.csv
**Сортировка 2** - По плюс словам в заголовке. Список плюс слов в файле /files/plus_lists.py
Сначала идут вакансии с первым плюс словом, далее со 2,3 и в конце записываются вакансии без ключевых слов в заголовке.
**Сортировка 3** - По плюс словам в описании вакансии. Список плюс слов в файле /files/plus_lists.py
Сначала идут вакансии с первым плюс словом, далее со 2,3 
и в конце записываются вакансии без ключевых слов в описании вакансии.

Перед запуском надо в файле tests/features/tester_python_web.feature установить вакансию и график работы.

Запуск из консоли