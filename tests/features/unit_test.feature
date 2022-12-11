Feature: unit_test_1
  schedule может принимать 3 значения
  удаленка, гибрид, удаленка+гибрид


  @unit
  Scenario: unit_test_1
    When check def choose_selector step 1
    When check def pass_for_one_list_vacancies_page 1, тестировщик, step 2
    When check def title_filter step 3
#    When pages with list vacancy processing step 4
#    When sort salary and delete doubles step 5
#    When sort for plus words title save to sort_plus_title_hh_2022 step 6
#    When sort for plus words description vacancy step 7
