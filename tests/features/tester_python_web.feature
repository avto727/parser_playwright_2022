Feature: tester_python_web
  schedule может принимать 3 значения
  удаленка, гибрид, удаленка+гибрид


  @tester_python_web
  Scenario: tester_python_web
    Given Open browser base_url keyword=тестировщик schedule=удаленка
    # Close modal window confirm city
    When click Button_Всё_верно step 1
    When determinate total_pages to store
    When pages processing
    When sort salary and delete doubles
    When save results in hh_2022_salary

#    When sort for plus words
#    When save results in hh_2022_plus_words
