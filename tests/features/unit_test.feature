Feature: unit_test_1



#  @unit
  Scenario: unit_test_1
    When check def choose_selector step 1
    When check def pass_for_one_list_vacancies_page 1, тестировщик, step 2
    When check def title_filter step 3
    When check def delete_doubles step 4


#  @unit
  Scenario: unit_test_delete_doubles
#  Сортировка словаря из файла dict_vacancy.py
#    When check def dict_sorting step 5
#  Проверка функции delete_doubles. Берется словарь из файла dict_vacancy.py
    When check def delete_doubles step 6


#  @unit
  Scenario: unit_test_sort_plus_word_in_title
    When check def_sort_for_plus_words_title file_name step 1


  @unit
  Scenario: unit_test_sort_for_plus_words_in_content
    When check sort_for_plus_words_in_content step 1