Feature: tester_python_web
  schedule может принимать 3 значения
  удаленка, гибрид, удаленка+гибрид


  @tester_python_web
  Scenario: tester_python_web
    Given Open browser base_url keyword=тестировщик schedule=удаленка
    When click Button_Всё_верно step 1
    When determinate total_pages to store
    When pages processing
    When sort salary and delete doubles
    When save results vacancy_no_doubles in hh_2022_salary

    When sort for plus words title save to sort_plus_title_hh_2022

    When sort for plus words description vacancy
    When save results vacancy_sort_title_plus in hh_2022_plus_words_description
