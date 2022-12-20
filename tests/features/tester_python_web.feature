Feature: tester_python_web
  schedule может принимать 3 значения
  удаленка, гибрид, удаленка+гибрид


  @tester_python_web
  Scenario: tester_python_web
    Given Open browser base_url keyword=тестировщик schedule=удаленка step 1
    When click Button_Всё_верно step 2
    When determinate total_pages to store step 3
    When pages with list vacancy processing step 4
    When sort salary and delete doubles step 5
    When sort for plus words title save to sort_plus_title_hh_2022 step 6

    When sort for plus words description vacancy step 7
