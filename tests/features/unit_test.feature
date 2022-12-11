Feature: unit_test_1



#  @unit
  Scenario: unit_test_1
    When check def choose_selector step 1
    When check def pass_for_one_list_vacancies_page 1, тестировщик, step 2
    When check def title_filter step 3
    When check def delete_doubles step 4


  @unit
  Scenario: unit_test_delete_doubles
    When check def delete_doubles step 4